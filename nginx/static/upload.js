const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const fileNameDisplay = document.getElementById('file-name');
const uploadBtn = document.getElementById('upload-btn');
const expirySelect = document.getElementById('expiry-select');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');
const resultContainer = document.getElementById('result-container');
const uploadContainer = document.getElementById('upload-container');
const shareLinkDisplay = document.getElementById('share-link');
const qrCodeImg = document.getElementById('qr-code');
const copyBtn = document.getElementById('copy-btn');

let selectedFile = null;

// Drag and drop events
dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('drag-over');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('drag-over');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

dropzone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    fileNameDisplay.textContent = file.name;
    fileNameDisplay.classList.add('text-blue-600');
}

uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        alert("Please select a file first");
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('expiry_mins', expirySelect.value);

    // Show progress
    uploadContainer.classList.add('opacity-50', 'pointer-events-none');
    progressContainer.classList.remove('hidden');
    uploadBtn.disabled = true;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/upload', true);

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            const percentComplete = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = percentComplete + '%';
            progressText.textContent = percentComplete + '%';
        }
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            showResult(response);
        } else {
            alert("Upload failed: " + xhr.statusText);
            resetUpload();
        }
    };

    xhr.onerror = function() {
        alert("An error occurred during upload");
        resetUpload();
    };

    xhr.send(formData);
});

function showResult(data) {
    uploadContainer.classList.add('hidden');
    resultContainer.classList.remove('hidden');
    shareLinkDisplay.textContent = data.share_url;
    qrCodeImg.src = data.qr_code;
}

function resetUpload() {
    uploadContainer.classList.remove('hidden', 'opacity-50', 'pointer-events-none');
    progressContainer.classList.add('hidden');
    uploadBtn.disabled = false;
    progressBar.style.width = '0%';
    progressText.textContent = '0%';
}

copyBtn.addEventListener('click', () => {
    const link = shareLinkDisplay.textContent;
    navigator.clipboard.writeText(link).then(() => {
        const icon = copyBtn.querySelector('i');
        icon.classList.replace('far', 'fas');
        icon.classList.replace('fa-copy', 'fa-check');
        icon.classList.add('text-green-500');
        
        setTimeout(() => {
            icon.classList.replace('fas', 'far');
            icon.classList.replace('fa-check', 'fa-copy');
            icon.classList.remove('text-green-500');
        }, 2000);
    });
});
