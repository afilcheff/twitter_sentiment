# twitter_sentiment
## Task

Create a streaming pipeline that ingests real-time tweets for a given hashtag(s), estimates sentiment of the tweets and stores results in Google Big Query.
Connect results to a data visualisation tool for analytic purposes.


## 1. First iteration
1. Create a VM in Google Compute Engine that streams tweets in real time, estimates sentiment via TextBlob (https://textblob.readthedocs.io/en/dev/) and feeds results directly to Big Query.
2. Use Google Data Studio for visualisation

## Work in Progress
1. Create a VM in Google Compute Engine that streams tweets in real time, estimates sentiment via TextBlob (https://textblob.readthedocs.io/en/dev/) and feeds results to Google Pub/Sub.
2. Use Dataflow (Apache Beam) to perform extraction and staging in BQ. Dataflow is the managed version of Apache Beam, providing a scallable serverless platform for parallel big data transformations.
3. Use Google Data Studio for visualisation




## References:


https://towardsdatascience.com/game-of-thrones-twitter-sentiment-with-keras-apache-beam-bigquery-and-pubsub-382a770f6583
https://medium.com/codex/a-dataflow-journey-from-pubsub-to-bigquery-68eb3270c93
https://textblob.readthedocs.io/en/dev/

https://cloud.google.com/bigquery/streaming-data-into-bigquery
https://cloud.google.com/pubsub/docs/pubsub-dataflow#python
https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python
https://cloud.google.com/container-registry/docs/quickstart