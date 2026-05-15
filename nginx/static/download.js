const loadingState = document.getElementById('loading-state');
const errorState = document.getElementById('error-state');
const contentState = document.getElementById('content-state');
const errorMessage = document.getElementById('error-message');
const fileNameDisplay = document.getElementById('file-name');
const expiryTimeDisplay = document.getElementById('expiry-time');
const downloadBtn = document.getElementById('download-btn');

async function fetchFileDetails() {
    // Extract ID from URL path (e.g., /d/file_id)
    const pathParts = window.location.pathname.split('/');
    const fileId = pathParts[pathParts.length - 1];

    if (!fileId || fileId === 'download.html') {
        showError("Invalid link format");
        return;
    }

    try {
        const response = await fetch(`/api/download/${fileId}`);
        
        if (response.status === 404 || response.status === 410) {
            const data = await response.json();
            showError(data.detail);
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to fetch file details");
        }

        const data = await response.json();
        showContent(data);
    } catch (error) {
        showError(error.message);
    }
}

function showContent(data) {
    loadingState.classList.add('hidden');
    contentState.classList.remove('hidden');
    
    fileNameDisplay.textContent = data.filename;
    
    // Format date
    const expiryDate = new Date(data.expires_at);
    expiryTimeDisplay.textContent = expiryDate.toLocaleString();
    
    downloadBtn.href = data.sas_url;
    // For direct downloads to work with SAS URLs sometimes you need download attribute
    downloadBtn.setAttribute('download', data.filename);
}

function showError(msg) {
    loadingState.classList.add('hidden');
    errorState.classList.remove('hidden');
    errorMessage.textContent = msg;
}

// Initial fetch
window.addEventListener('DOMContentLoaded', fetchFileDetails);
