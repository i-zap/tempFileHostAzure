from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import upload, download
from .config import settings

app = FastAPI(title="temp-share API", version="1.0.0")

# CORS configuration for Vercel and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Vercel domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(download.router, prefix="/api", tags=["download"])

@app.get("/")
async def root():
    return {"message": "temp-share API is running", "docs": "/docs"}
