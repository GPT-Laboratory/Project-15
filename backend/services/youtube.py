import os
import yt_dlp
import tempfile
from urllib.parse import urlparse, parse_qs

def is_valid_youtube_url(url):
    """
    Validate if the URL is a valid YouTube URL.
    """
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc:
        return True
    return False

def get_video_id(url):
    """
    Extract video ID from YouTube URL.
    """
    if 'youtu.be' in url:
        return os.path.basename(urlparse(url).path)
    
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    
    return None

def download_youtube_video(url):
    """
    Download a YouTube video and extract audio.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        tuple: (video_path, audio_path)
    """
    if not is_valid_youtube_url(url):
        raise ValueError("Invalid YouTube URL")
    
    video_id = get_video_id(url)
    if not video_id:
        raise ValueError("Could not extract video ID from URL")
    
    # Create temporary directories
    temp_dir = tempfile.gettempdir()
    video_path = os.path.join(temp_dir, f"{video_id}.mp4")
    audio_path = os.path.join(temp_dir, f"{video_id}.mp3")
    
    # Download options
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': video_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'keepvideo': True,
        'quiet': False,
        'no_warnings': False,
    }
    
    # Download the video
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")
    
    # Check if files were created
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file was not created at {video_path}")
    
    if not os.path.exists(audio_path):
        # If audio extraction failed, set audio_path to None
        audio_path = None
    
    return video_path, audio_path 