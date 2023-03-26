import os
import base64
import json
from google.cloud import bigquery
from google.oauth2 import service_account

def lambda_handler(event, context):
    # Load GCP service account key from environment variable
    gcp_credentials_base64 = os.environ['GCP_CREDENTIALS_BASE64']
    gcp_credentials_json = base64.b64decode(gcp_credentials_base64).decode("utf-8")
    gcp_credentials = json.loads(gcp_credentials_json)
    credentials = service_account.Credentials.from_service_account_info(gcp_credentials)

    # Create a BigQuery client
    client = bigquery.Client(credentials=credentials, project=gcp_credentials['project_id'])

    # Get BigQuery table reference
    dataset_id = os.environ['BQ_DATASET_ID']
    table_id = os.environ['BQ_TABLE_ID']
    table_ref = client.dataset(dataset_id).table(table_id)

    # Process the DynamoDB Stream event
    for record in event['Records']:
        if record['eventName'] in ['INSERT', 'MODIFY']:
            # Extract the new image (the updated item)
            new_image = record['dynamodb']['NewImage']

            # Convert the new image from DynamoDB to BigQuery format
            row = {k: convert_value(v) for k, v in new_image.items()}

            # Insert the row into the BigQuery table
            errors = client.insert_rows_json(table_ref, [row])
            if errors:
                print(f"Error inserting row into BigQuery: {errors}")
            else:
                print(f"Inserted row into BigQuery: {row}")

def convert_value(value):
    """Convert a DynamoDB value to a Python value."""
    for type, val in value.items():
        if type == "S":
            return val
        if type == "N":
            return float(val)
        if type == "B":
            return base64.b64decode(val)
        # Handle other types as needed

