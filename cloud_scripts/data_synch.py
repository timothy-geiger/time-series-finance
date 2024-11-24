import os
from dotenv import load_dotenv
import pandas as pd

from ibm_boto3 import client
from ibm_botocore.client import Config
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# Load environment variables from .env file
load_dotenv(override=True)

# IBM Cloud Object Storage configuration
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_IAM_SERVICE_ID = os.getenv("COS_IAM_SERVICE_ID")
COS_ENDPOINT = os.getenv("COS_ENDPOINT")
COS_BUCKET = os.getenv("COS_BUCKET")
COS_CSV_FILE_NAME = os.getenv("COS_CSV_FILE_NAME")

# Load configuration from environment variables
INFLUXDB_V2_URL = os.getenv("INFLUXDB_V2_URL")
INFLUXDB_V2_TOKEN = os.getenv("INFLUXDB_V2_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")


# Function to download file from IBM Cloud Object Storage
def download_from_cos(local_file_name):

    cos = client(
        service_name='s3',
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_IAM_SERVICE_ID,
        config=Config(signature_version='oauth'),
        endpoint_url=COS_ENDPOINT)

    try:
        cos.download_file(
            Bucket=COS_BUCKET, Key=COS_CSV_FILE_NAME, Filename=local_file_name)

    except Exception as e:
        print(f"Unable to download file: {e}")
        exit(1)


# Function to upload data to InfluxDB
def upload_to_influxdb(local_file_name):
    client = InfluxDBClient(
        url=INFLUXDB_V2_URL, token=INFLUXDB_V2_TOKEN, org=INFLUXDB_ORG)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    try:
        df = pd.read_csv(local_file_name, skiprows=3)
        df["_time"] = pd.to_datetime(df["_time"])
        print(INFLUXDB_BUCKET)

        points = []

        for _, row in df.iterrows():
            point = (
                Point("coindesk5")
                .tag("code", row["code"])
                .tag("crypto", row["crypto"])
                .tag("description", row["description"])
                .tag("symbol", row["symbol"])
                .field("price", float(row["_value"]))
                .time(row["_time"])
            )

            points.append(point)

        # Batch write all points to InfluxDB
        write_api.write(
            bucket=INFLUXDB_BUCKET,
            org=INFLUXDB_ORG,
            record=points)

    except Exception as e:
        print(f"Error uploading data to InfluxDB: {e}")

    finally:
        write_api.flush()
        client.close()


# Main function
if __name__ == "__main__":

    # Step 1: Download the data from IBM COS
    download_from_cos(
        local_file_name="local_data.csv",
    )

    # Step 2: Upload the data to InfluxDB
    upload_to_influxdb(
        local_file_name="local_data.csv"
    )
