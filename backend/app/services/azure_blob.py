import datetime
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions, ContentSettings
from ..config import settings

class AzureBlobService:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )
        self.container_client = self.blob_service_client.get_container_client(
            settings.CONTAINER_NAME
        )

    def upload_blob(self, blob_name: str, data: bytes, content_type: str, expiry_mins: int, original_filename: str):
        blob_client = self.container_client.get_blob_client(blob_name)
        
        # Calculate expiry timestamp
        expiry_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiry_mins)
        
        metadata = {
            "expiry": expiry_time.isoformat(),
            "original_name": original_filename
        }
        
        blob_client.upload_blob(
            data, 
            overwrite=True, 
            content_settings=ContentSettings(content_type=content_type),
            metadata=metadata
        )
        return blob_name

    def get_blob_metadata(self, blob_name: str):
        blob_client = self.container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            return None
        return blob_client.get_blob_properties().metadata

    def generate_sas_url(self, blob_name: str, expiry_mins: int = 15):
        # Fetch metadata to get the original filename
        metadata = self.get_blob_metadata(blob_name)
        original_name = metadata.get("original_name", blob_name) if metadata else blob_name

        # SAS URL for the actual file download, valid for a short time
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=settings.CONTAINER_NAME,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiry_mins),
            content_disposition=f'attachment; filename="{original_name}"'
        )
        
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{settings.CONTAINER_NAME}/{blob_name}?{sas_token}"

azure_service = AzureBlobService()
