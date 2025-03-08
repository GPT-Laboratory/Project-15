import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.youtube import download_youtube_video
from services.transcription import transcribe_audio
from services.blog_generator import generate_blog_post

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint to check if the API is running."""
    return jsonify({"status": "ok", "message": "YouTube to Blog Post API is running"})

@app.route('/api/process', methods=['POST'])
def process_video():
    """Process a YouTube video and generate a blog post."""
    data = request.json
    if not data or 'video_url' not in data:
        return jsonify({"error": "Missing video URL"}), 400
    
    video_url = data['video_url']
    try:
        # Step 1: Download the YouTube video
        video_path, audio_path = download_youtube_video(video_url)
        
        # Step 2: Transcribe the audio
        transcript = transcribe_audio(audio_path)
        
        # Step 3: Generate blog post from transcript
        blog_post = generate_blog_post(transcript, video_url)
        
        # Clean up temporary files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return jsonify({
            "status": "success",
            "blog_post": blog_post,
            "video_url": video_url
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 