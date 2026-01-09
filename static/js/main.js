let uploadedFileId = null;
let uploadedFileName = null;
let uploadedFileExtension = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadTrigger = document.getElementById('uploadTrigger');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');
const formatSelect = document.getElementById('formatSelect');
const convertBtn = document.getElementById('convertBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultSection = document.getElementById('resultSection');
const downloadLink = document.getElementById('downloadLink');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const formatInfo = document.getElementById('formatInfo');
const inputFormat = document.getElementById('inputFormat');
const outputFormat = document.getElementById('outputFormat');

uploadArea.addEventListener('click', () => fileInput.click());

if (uploadTrigger) {
    uploadTrigger.addEventListener('click', () => {
        fileInput.click();
    });
}

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

removeFile.addEventListener('click', () => {
    resetUpload();
});

convertBtn.addEventListener('click', async () => {
    if (!uploadedFileId || !formatSelect.value) return;
    
    hideError();
    hideResult();
    showProgress();
    
    try {
        updateProgress(40);
        progressText.textContent = 'Converting file...';
        
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                file_id: uploadedFileId,
                format: formatSelect.value
            })
        });
        
        updateProgress(70);
        progressText.textContent = 'Finalizing...';
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Conversion failed');
        }
        
        updateProgress(100);
        progressText.textContent = 'Complete!';
        
        setTimeout(() => {
            hideProgress();
            showResult(data.download_url, data.output_file);
        }, 500);
    } catch (error) {
        hideProgress();
        showError(error.message);
    }
});

function getFileExtension(filename) {
    return filename.split('.').pop().toLowerCase();
}

async function handleFile(file) {
    const extension = getFileExtension(file.name);
    const supportedExtensions = ['txt', 'pdf', 'docx', 'html', 'json', 'csv', 'xml', 'rtf', 'epub', 'odt'];
    
    if (!supportedExtensions.includes(extension)) {
        showError(`Unsupported file type. Supported formats: ${supportedExtensions.join(', ')}`);
        return;
    }
    
    hideError();
    hideResult();
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        showProgress();
        progressText.textContent = 'Uploading file...';
        updateProgress(20);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        let data;
        try {
            const text = await response.text();
            if (!text) {
                throw new Error('Empty response from server');
            }
            data = JSON.parse(text);
        } catch (e) {
            if (e instanceof SyntaxError) {
                throw new Error(`Server error: ${response.status} ${response.statusText}. Response: ${e.message}`);
            }
            throw new Error(`Failed to parse server response: ${e.message}`);
        }
        
        if (!response.ok) {
            throw new Error(data.error || `Upload failed: ${response.status} ${response.statusText}`);
        }
        
        if (!data.success) {
            throw new Error(data.error || 'Upload was not successful');
        }
        
        updateProgress(100);
        uploadedFileId = data.file_id;
        uploadedFileName = data.filename;
        uploadedFileExtension = getFileExtension(uploadedFileName);
        
        fileName.textContent = uploadedFileName;
        fileSize.textContent = formatFileSize(data.size);
        
        fileInfo.style.display = 'flex';
        uploadArea.style.display = 'none';
        
        formatSelect.disabled = false;
        convertBtn.disabled = !formatSelect.value;
        
        setTimeout(() => {
            hideProgress();
        }, 500);
        loadFormats();
        updateFormatInfo();
    } catch (error) {
        hideProgress();
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showError('Network error: Could not connect to server. Make sure the server is running.');
        } else {
            showError(error.message || 'Upload failed. Please try again.');
        }
        console.error('Upload error:', error);
    }
}

async function loadFormats() {
    try {
        const response = await fetch('/api/formats');
        const data = await response.json();
        
        formatSelect.innerHTML = '<option value="">Choose a format...</option>';
        
        data.formats.forEach(format => {
            const option = document.createElement('option');
            option.value = format.id;
            option.textContent = format.name;
            formatSelect.appendChild(option);
        });
        
        const formatCountEl = document.getElementById('formatCount');
        if (formatCountEl && data.formats) {
            formatCountEl.textContent = data.formats.length;
        }
    } catch (error) {
        showError('Failed to load formats');
    }
}

formatSelect.addEventListener('change', () => {
    convertBtn.disabled = !uploadedFileId || !formatSelect.value;
    updateFormatInfo();
});

function updateFormatInfo() {
    if (uploadedFileExtension && formatSelect.value) {
        inputFormat.textContent = uploadedFileExtension.toUpperCase();
        outputFormat.textContent = formatSelect.value.toUpperCase();
        formatInfo.style.display = 'block';
    } else {
        formatInfo.style.display = 'none';
    }
}

function resetUpload() {
    uploadedFileId = null;
    uploadedFileName = null;
    uploadedFileExtension = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'block';
    formatSelect.value = '';
    formatSelect.disabled = true;
    convertBtn.disabled = true;
    hideResult();
    hideError();
    formatInfo.style.display = 'none';
}

function showProgress() {
    progressSection.style.display = 'block';
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        progressFill.style.width = progress + '%';
    }, 200);
    
    window.progressInterval = interval;
}

function updateProgress(value) {
    if (progressFill) {
        progressFill.style.width = value + '%';
    }
}

function hideProgress() {
    if (window.progressInterval) {
        clearInterval(window.progressInterval);
        window.progressInterval = null;
    }
    if (progressFill) {
        progressFill.style.width = '100%';
        setTimeout(() => {
            progressSection.style.display = 'none';
            progressFill.style.width = '0%';
        }, 300);
    } else {
        progressSection.style.display = 'none';
    }
}

function showResult(downloadUrl, filename) {
    resultSection.style.display = 'block';
    downloadLink.href = downloadUrl;
    downloadLink.download = filename;
}

function hideResult() {
    resultSection.style.display = 'none';
}

function showError(message) {
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

function hideError() {
    errorSection.style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function initDarkMode() {
    const themeToggle = document.getElementById('themeToggle');
    const sunIcon = document.getElementById('sunIcon');
    const moonIcon = document.getElementById('moonIcon');
    const html = document.documentElement;
    
    if (!themeToggle) return;
    
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcons(savedTheme);
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcons(newTheme);
    });
    
    function updateThemeIcons(theme) {
        if (theme === 'dark') {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        }
    }
}

loadFormats();
initDarkMode();