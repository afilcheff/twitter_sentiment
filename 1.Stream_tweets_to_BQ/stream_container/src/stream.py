import os
import datetime
import json
import time

import credentials

from textblob import TextBlob

import tweepy
from google.cloud import bigquery
from tweepy.streaming import StreamListener

#Config
table_id = "<projectID>.<dataset>.<table>"
 
auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=False)

# Construct a BigQuery client object.
client = bigquery.Client()

# Define the list of terms to listen to
lst_hashtags = ["#btc", "#eth", "#bitcoin", "#ethereum"]

# Function that calculates sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

# Function that writes tweets directly to Big Query
def write_to_bq(data):
    try:
        if data["lang"] == "en":
            row_to_insert = [
                {u"text": data["text"], u"user_id": data["user_id"], u"id": data["id"], u"posted_at": data["created_at"], u"sentiment": data["sentiment"]}
            ]
            errors = client.insert_rows_json(table_id, row_to_insert)
            if errors == []:
                print("new rows have been added.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))
    except Exception as e:
        raise

# Method to format a tweet from tweepy
def reformat_tweet(tweet):
    x = tweet

    processed_doc = {
        "id": x["id"],
        "lang": x["lang"],
        "retweeted_id": x["retweeted_status"]["id"] if "retweeted_status" in x else None,
        "favorite_count": x["favorite_count"] if "favorite_count" in x else 0,
        "retweet_count": x["retweet_count"] if "retweet_count" in x else 0,
        "coordinates_latitude": x["coordinates"]["coordinates"][0] if x["coordinates"] else 0,
        "coordinates_longitude": x["coordinates"]["coordinates"][0] if x["coordinates"] else 0,
        "place": x["place"]["country_code"] if x["place"] else None,
        "user_id": x["user"]["id"],
        "created_at": time.mktime(time.strptime(x["created_at"], "%a %b %d %H:%M:%S +0000 %Y"))
    }

    if x["entities"]["hashtags"]:
        processed_doc["hashtags"] = [{"text": y["text"], "startindex": y["indices"][0]} for y in
                                     x["entities"]["hashtags"]]
    else:
        processed_doc["hashtags"] = []

    if x["entities"]["user_mentions"]:
        processed_doc["usermentions"] = [{"screen_name": y["screen_name"], "startindex": y["indices"][0]} for y in
                                         x["entities"]["user_mentions"]]
    else:
        processed_doc["usermentions"] = []

    if "extended_tweet" in x:
        processed_doc["text"] = x["extended_tweet"]["full_text"]
    elif "full_text" in x:
        processed_doc["text"] = x["full_text"]
    else:
        processed_doc["text"] = x["text"]

    processed_doc["sentiment"] = analyze_sentiment(processed_doc["text"])

    return processed_doc

# Custom listener class
class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just pushes tweets to pubsub
    """

    def __init__(self):
        super(StdOutListener, self).__init__()
        self._counter = 0

    def on_status(self, data):
        write_to_bq(reformat_tweet(data._json))
        self._counter += 1
        return True

    def on_error(self, status):
        if status == 420:
            print("rate limit active")
            return True


# Start listening
l = StdOutListener()
stream = tweepy.Stream(auth, l, tweet_mode='extended')
stream.filter(track=lst_hashtags)