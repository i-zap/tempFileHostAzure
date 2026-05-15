import datetime
from fastapi import APIRouter, HTTPException
from ..services.azure_blob import azure_service

router = APIRouter()

@router.get("/download/{blob_name}")
async def get_download_link(blob_name: str):
    metadata = azure_service.get_blob_metadata(blob_name)
    
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found or expired")
    
    expiry_str = metadata.get("expiry")
    if not expiry_str:
        raise HTTPException(status_code=404, detail="File metadata corrupt")
    
    expiry_time = datetime.datetime.fromisoformat(expiry_str)
    if datetime.datetime.now(datetime.timezone.utc) > expiry_time:
        raise HTTPException(status_code=410, detail="File has expired")
    
    sas_url = azure_service.generate_sas_url(blob_name)
    
    return {
        "sas_url": sas_url,
        "filename": metadata.get("original_name", blob_name),
        "expires_at": expiry_str
    }
