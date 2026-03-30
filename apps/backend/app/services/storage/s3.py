import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.effective_aws_access_key,
            aws_secret_access_key=settings.effective_aws_secret_key,
            region_name=settings.S3_REGION,
            endpoint_url=settings.effective_s3_endpoint,
            config=Config(signature_version="s3v4")
        )

    def generate_presigned_upload_url(self, bucket: str, key: str, expiration: int = 3600):
        return self.s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration
        )

    def get_object_metadata(self, bucket: str, key: str):
        """Fetches actual object metadata from S3 using a HEAD request."""
        try:
            response = self.s3_client.head_object(Bucket=bucket, Key=key)
            return {
                "size_bytes": response.get("ContentLength"),
                "content_type": response.get("ContentType"),
                "etag": response.get("ETag")
            }
        except ClientError:
            return None

storage_service = StorageService()
