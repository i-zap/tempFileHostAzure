# temp-share Monolithic Deployment Guide

## 1. Architecture Overview
- **Nginx**: Serves static HTML/JS/CSS and proxies API requests.
- **FastAPI**: Backend logic and Azure Blob integration.
- **Cleaner**: Azure Function (running in Docker) for auto-deletion.
- **Azure Blob**: Storage for all files.

## 2. Infrastructure Setup (Single VPS)

### Prerequisites
- Ubuntu 22.04+
- Docker and Docker Compose installed.
- Domain `upload.izap.fun` pointing to VPS IP.

### Deployment Steps
1. **Clone & Prepare**:
   ```bash
   cd temp-share
   ```
2. **Environment Variables**:
   Ensure `.env` contains:
   ```env
   AZURE_STORAGE_CONNECTION_STRING="your_connection_string"
   CONTAINER_NAME="tempfiles"
   BASE_URL="http://upload.izap.fun"
   ```
3. **Launch**:
   ```bash
   docker-compose up -d --build
   ```

## 3. SSL Configuration (Let's Encrypt)

1. **Initial Run**: Nginx is currently listening on port 80.
2. **Obtain Certificate**:
   ```bash
   sudo apt install certbot
   sudo certbot certonly --webroot -w ./certbot/www -d upload.izap.fun
   ```
3. **Update Nginx for SSL**:
   Modify `nginx/nginx.conf` to add the port 443 server block:
   ```nginx
   server {
       listen 443 ssl;
       server_name upload.izap.fun;

       ssl_certificate /etc/letsencrypt/live/upload.izap.fun/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/upload.izap.fun/privkey.pem;

       # ... rest of the config same as port 80 ...
   }
   ```
4. **Restart**: `docker-compose restart nginx`.

## 4. DNS Instructions (Hostinger)
1. Log in to Hostinger.
2. Go to DNS Zone Editor.
3. Add/Update **A Record**:
   - Host: `upload`
   - Points to: `[Your VPS IP]`
   - TTL: 3600

## 5. Security & Limits
- **Upload Limit**: 500MB (defined in `nginx.conf`).
- **Rate Limit**: 5 requests per second per IP (defined in `nginx.conf`).
- **Auto-Delete**: Runs every 15 minutes (defined in `function-cleaner`).
