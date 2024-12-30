const videoFrame = document.getElementById('videoFrame');
const youtubeLink = document.getElementById('youtubeLink');
const body = document.body;

window.onload = function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    }
};

function loadVideo() {
    const url = youtubeLink.value;
    const videoId = extractVideoId(url);
    if (videoId) {
        videoFrame.src = `https://www.youtube.com/embed/${videoId}`;
    } else {
        alert('Invalid YouTube URL');
    }
}

function extractVideoId(url) {
    const match = url.match(/(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/.*[?&]v=([^&]+)|youtu\.be\/([^?&]+)/);
    return match ? match[1] || match[2] : null;
}

function copyLink() {
    navigator.clipboard.writeText(youtubeLink.value).then(() => {
        alert('Link copied to clipboard!');
    }).catch(err => {
        alert('Failed to copy link: ' + err);
    });
}

function toggleTheme() {
    const isDark = body.classList.contains('dark-mode');
    const newTheme = isDark ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
}

function setTheme(theme) {
    if (theme === 'dark') {
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
    }
}

function downloadVideo() {
    const url = youtubeLink.value;
    if (url) {
        fetch(`/api/download?url=${encodeURIComponent(url)}`)
            .then(response => response.json())
            .then(data => {
                if (data.download_link) {
                    window.location.href = data.download_link;
                } else {
                    alert('Failed to get download link');
                }
            })
            .catch(error => {
                alert('Error: ' + error.message);
            });
    } else {
        alert("Please provide a YouTube URL.");
    }
}
