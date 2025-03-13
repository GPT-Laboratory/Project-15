import yt_dlp
import os

def download_youtube_video(url, output_path="downloads"):
    """
    Download a YouTube video and separate it into audio and video files.
    
    Args:
        url: YouTube video URL
        output_path: Directory to save the files
    
    Returns:
        Tuple of (video_path, audio_path)
    """

    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Options for downloading video and audio separately 
    options = {
        'format': 'bv,ba',
        'outtmpl': os.path.join(output_path, '%(title)s.%(format_id)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'write_subtitles': True,
    }
    
    # Download video and audio file separately
    with yt_dlp.YoutubeDL(options) as downloader:
        video_info = downloader.extract_info(url, download=True)
        video_path = downloader.prepare_filename(video_info)
    
    
    print(f"Video and audio downloaded to: {video_path}")

    return video_path

if __name__ == "__main__":

    # Download video and audio files from YouTube video
    video_url = input("Enter YouTube URL: ")
    video_file = download_youtube_video(video_url)
