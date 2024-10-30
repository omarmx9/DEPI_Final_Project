const fileInput = document.getElementById('file-input');
const fileLabel = document.getElementById('file-label');
const loadingMessage = document.getElementById('loading-message');
const progressBarContainer = document.getElementById('progress-bar-container');
const progressBar = document.getElementById('progress-bar');
const progressPercent = document.getElementById('progress-percent');
const transcriptionContainer = document.getElementById('transcription-container');
const transcriptionText = document.getElementById('transcription-text');

// Show the selected file name
fileInput.addEventListener('change', () => {
    const fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file chosen';
    fileLabel.textContent = fileName;
});

// Function to upload the file to the server
function uploadFile() {
    const file = fileInput.files[0];
    if (!file) {
        alert('Please choose a file first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    // Show loading message and progress bar
    loadingMessage.style.display = 'block';
    progressBarContainer.style.display = 'block';
    progressBar.value = 0;
    progressPercent.textContent = '0%';

    fetch('http://127.0.0.1:5000/transcribe', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Hide loading message and progress bar, show transcription result
        loadingMessage.style.display = 'none';
        progressBarContainer.style.display = 'none';
        transcriptionContainer.style.display = 'block';

        if (data.transcription) {
            transcriptionText.value = data.transcription;
        } else if (data.error) {
            transcriptionText.value = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading the file: ' + error.message);
        loadingMessage.style.display = 'none';
        progressBarContainer.style.display = 'none';
    });
}

// Function to copy transcription text to clipboard
function copyToClipboard() {
    transcriptionText.select();
    document.execCommand('copy');
    alert('Transcription copied to clipboard!');
}
