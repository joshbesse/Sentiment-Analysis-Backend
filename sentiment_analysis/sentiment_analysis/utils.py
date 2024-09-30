import boto3
import os 
import logging

logger = logging.getLogger(__name__)

def download_file_from_s3(s3_key, local_file_path):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_S3_REGION_NAME')
    )
    try:
        s3.download_file(os.getenv('AWS_STORAGE_BUCKET_NAME'), s3_key, local_file_path)
        logger.info(f"Downloaded {s3_key} to {local_file_path}")
    except Exception as e:
        logger.error(f"Error downloading {s3_key} from S3: {e}")
        raise 