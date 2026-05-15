import datetime
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from ..config import settings

class AzureBlobService:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )
        self.container_client = self.blob_service_client.get_container_client(
            settings.CONTAINER_NAME
        )

    def upload_blob(self, file_name: str, data: bytes, content_type: str, expiry_mins: int):
        blob_client = self.container_client.get_blob_client(file_name)
        
        # Calculate expiry timestamp
        expiry_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiry_mins)
        
        metadata = {
            "expiry": expiry_time.isoformat(),
            "original_name": file_name
        }
        
        blob_client.upload_blob(
            data, 
            overwrite=True, 
            content_settings={"content_type": content_type},
            metadata=metadata
        )
        return file_name

    def get_blob_metadata(self, blob_name: str):
        blob_client = self.container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            return None
        return blob_client.get_blob_properties().metadata

    def generate_sas_url(self, blob_name: str, expiry_mins: int = 15):
        # SAS URL for the actual file download, valid for a short time
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=settings.CONTAINER_NAME,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiry_mins)
        )
        
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{settings.CONTAINER_NAME}/{blob_name}?{sas_token}"

azure_service = AzureBlobService()
