import boto3
from app.config import Config
from uuid import uuid4
from botocore.client import Config as BotoConfig

class ObjectStorage:
    def __init__(self):
        config = {
            'aws_access_key_id': Config.OBJECT_STORAGE_KEY_ID,
            'aws_secret_access_key': Config.OBJECT_STORAGE_SECRET_ACCESS_KEY,
            'endpoint_url': Config.OBJECT_STORAGE_ENDPOINT_URL,
            'config': BotoConfig(signature_version="s3v4")
        }

        self.storage_client = boto3.client('s3', **config)

    def create_presigned_url(self, operation, bucket, key, expiration = 3600):
        response = self.storage_client.generate_presigned_url(
            ClientMethod= operation,
            Params= {
                'Bucket': bucket,
                'Key': key,
            },
            ExpiresIn= expiration,
        )
        return response