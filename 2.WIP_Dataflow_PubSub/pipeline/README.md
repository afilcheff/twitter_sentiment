# Notes

Before deploying the pipeline make sure to:
1. Have all the relevant APIs enabled and Google IAM configured
2. Have a Cloud Storage bucket created where Dataflow stores files
3. Create a Pub/Sub subscription ready
4. Create a BigQuery dataset and table with the following schema:
"id:NUMERIC,text:STRING,user_id:NUMERIC,posted_at:TIMESTAMP,sentiment:STRING"
5.  Create a service account
6. In pipeline.py set credentials, Pub/Sub subscription and BQ table

To deploy the pipeline run the following:

python pipeline.py  \
    --streaming \
    --runner DataflowRunner \
    --project "PROJECT_ID" \
    --region "DATAFLOW_REGION" \
    --temp_location gs://"STORAGE_BUCKET"/tmp \
    --job_name dataflow-custom-pipeline-v1 \
    --max_num_workers 2
