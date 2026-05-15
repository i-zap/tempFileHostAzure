import secrets
import io
import base64
import qrcode
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..services.azure_blob import azure_service
from ..config import settings

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    expiry_mins: int = Form(settings.DEFAULT_EXPIRY_MINS)
):
    if expiry_mins > settings.MAX_EXPIRY_MINS:
        raise HTTPException(status_code=400, detail="Maximum expiry exceeded")
    
    # Generate secure random ID
    file_id = secrets.token_urlsafe(12)
    
    # Read file content
    content = await file.read()
    
    # Upload to Azure
    # We keep the original extension if possible
    ext = file.filename.split('.')[-1] if '.' in file.filename else ''
    blob_name = f"{file_id}.{ext}" if ext else file_id
    
    azure_service.upload_blob(
        blob_name, 
        content, 
        file.content_type, 
        expiry_mins
    )
    
    # Generate share link
    # BASE_URL is expected to include protocol (e.g., http://3.108.190.168)
    base_url = settings.BASE_URL.rstrip('/')
    share_url = f"{base_url}/d/{blob_name}"
    
    # Generate QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(share_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    qr_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    return {
        "file_id": blob_name,
        "share_url": share_url,
        "qr_code": f"data:image/png;base64,{qr_base64}",
        "expiry_mins": expiry_mins
    }
