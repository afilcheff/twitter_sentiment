# Notes

Before building the container, make sure to:
1. Have all the relevant APIs enabled and Google IAM configured
1. Acquire Twitter Developer API credentials and fill them out in src/credentials.py
2. Create Pub/Sub topic and input the projectID and topic in src/stream.py

The container can be built and ran locally (you need a Google auth service file and to add os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json" in stream.py)
or can be deployed on a Google Cloud VM through Google Container Registry

To do so:
1. Install Google Cloud SDK and configure for your project
2. Configure Docker to use the gcloud command-line tool to authenticate requests to Container Registry via gcloud auth configure-docker
3. Build the image by running : docker build -t gcr.io/"projectID"/twitter-stream:v1 . (the . indicates that there is a dockerfile to build from)
4. Push the image to Container Registry by running: docker push gcr.io/"projectID"/twitter-stream:v1
5. From Container registry choose the relevant image and choose "Deploy to GCE". When setting up the VM configure "Identity and API access" for the relevant service account, enable HTTP and HTTPS traffic

Container Registry quickstart: https://cloud.google.com/container-registry/docs/quickstart