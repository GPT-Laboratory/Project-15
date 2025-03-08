import os
from openai import OpenAI
import tempfile
import time

def transcribe_audio(audio_path):
    """
    Transcribe audio file using OpenAI's Whisper API.
    
    Args:
        audio_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    if not audio_path or not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at {audio_path}")
    
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    
    # Transcribe audio using OpenAI's Whisper API
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        return transcript.text
        
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

def chunked_transcribe(audio_path, chunk_size_mb=25):
    """
    Split a large audio file into chunks and transcribe each chunk.
    Used for files larger than OpenAI's API limit.
    
    Args:
        audio_path (str): Path to the audio file
        chunk_size_mb (int): Size of each chunk in MB
        
    Returns:
        str: Combined transcription
    """
    from pydub import AudioSegment
    import math
    
    # Get the audio file size in MB
    audio_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    
    # If the file is small enough, just transcribe it directly
    if audio_size_mb <= chunk_size_mb:
        return transcribe_audio(audio_path)
    
    # Load the audio file
    audio = AudioSegment.from_file(audio_path)
    
    # Calculate duration in milliseconds
    duration_ms = len(audio)
    
    # Calculate number of chunks
    num_chunks = math.ceil(audio_size_mb / chunk_size_mb)
    chunk_length_ms = duration_ms // num_chunks
    
    # Create temp directory for chunks
    temp_dir = tempfile.mkdtemp()
    
    transcripts = []
    
    try:
        # Process each chunk
        for i in range(num_chunks):
            start_ms = i * chunk_length_ms
            end_ms = min((i + 1) * chunk_length_ms, duration_ms)
            
            chunk = audio[start_ms:end_ms]
            chunk_path = os.path.join(temp_dir, f"chunk_{i}.mp3")
            chunk.export(chunk_path, format="mp3")
            
            # Transcribe this chunk
            chunk_transcript = transcribe_audio(chunk_path)
            transcripts.append(chunk_transcript)
            
            # Clean up
            os.remove(chunk_path)
            
            # Avoid rate limiting
            if i < num_chunks - 1:
                time.sleep(1)
                
    finally:
        # Remove the temp directory
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
    
    # Combine all transcripts
    full_transcript = " ".join(transcripts)
    return full_transcript 