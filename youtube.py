import yt_dlp
import os
import requests
import time
import subprocess
import uuid
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("CAPTIONS_API_KEY")
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def download_youtube_video(url, output_path="downloads"):
    """
    Download a YouTube video and return the file path.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    options = {
        'format': 'bv+ba/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(options) as downloader:
        video_info = downloader.extract_info(url, download=True)
        video_path = downloader.prepare_filename(video_info)

    print(f"Video downloaded: {video_path}")
    return video_path

def download_file(url, file_path):
    """
    Download a file from a URL.
    """
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"Downloaded file: {file_path}")

def generate_talking_head(script, creator_name, output_path="avatars"):
    """
    Generate a talking head video using Captions AI API.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    submit_url = "https://api.captions.ai/api/creator/submit"
    payload = {
        "resolution": "fhd",
        "script": script,
        "creatorName": creator_name
    }
    print(API_KEY)
    print(HEADERS)
    
    response = requests.post(submit_url, json=payload, headers=HEADERS)

    if response.status_code != 200:
        raise Exception("Failed to submit request: " + response.text)

    operation_id = response.json()["operationId"]
    print(f"Job submitted. Operation ID: {operation_id}")

    poll_url = "https://api.captions.ai/api/creator/poll"
    while True:
        poll_payload = {"operationId": operation_id}
        poll_response = requests.post(poll_url, json=poll_payload, headers=HEADERS)
        poll_data = poll_response.json()

        if "url" in poll_data:
            avatar_url = poll_data["url"]
            unique_filename = f"talking_head_{uuid.uuid4().hex}.mp4"
            avatar_path = os.path.join(output_path, unique_filename)
            download_file(avatar_url, avatar_path)
            return avatar_path
        
        state = poll_data.get("state")
        if state == "FAILED":
            raise Exception("Talking head generation failed.")
        
        print(f"Waiting for avatar generation... State: {state}")
        time.sleep(5)

def overlay_avatar(video_path, avatar_path, start_time=0, duration=7, output_path="output.mp4"):
    """
    Overlay the talking head avatar on top of the reaction video at a specific time.
    
    Args:
        video_path: Path to the main video.
        avatar_path: Path to the talking head video.
        start_time: Time in seconds when the avatar should appear.
        duration: Duration in seconds for the avatar to remain visible.
        output_path: Path for the final video.
    """
    command = [
        "ffmpeg", "-i", video_path, "-i", avatar_path,
        "-filter_complex",
        f"[1:v]format=rgba,fade=t=in:st={start_time}:d=1,fade=t=out:st={start_time+duration}:d=1[avatar];"
        f"[0:v][avatar]overlay=W-w-10:H-h-10:enable='between(t,{start_time},{start_time+duration})'[outv]",
        "-map", "[outv]", "-map", "1:a", "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",
        output_path
    ]
    subprocess.run(command, check=True)
    print(f"Overlay video saved: {output_path}")

if __name__ == "__main__":
    use_downloaded_video = input("Do you want to use an already downloaded video? (yes/no): ").strip().lower()
    
    if use_downloaded_video == "yes":
        video_file = input("Enter the path to the downloaded video (inside 'downloads' folder): ").strip()
        video_file = os.path.join("downloads", video_file) if not os.path.isabs(video_file) else video_file
    else:
        video_url = input("Enter YouTube URL: ")
        video_file = download_youtube_video(video_url)
    
    script = input("Enter script for AI avatar: ")
    creator_name = input("Enter creator name (e.g., 'Kate'): ")

    avatar_file = generate_talking_head(script, creator_name)
    overlay_avatar(video_file, avatar_file)
