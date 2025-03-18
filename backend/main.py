from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolExecutor
import whisper
import tempfile
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Whisper model
model = whisper.load_model("base")

class MediaRequest(BaseModel):
    media_path: str
    video_file: str
    audio_file: str

class State(BaseModel):
    messages: list
    video_text: Optional[str] = None
    audio_text: Optional[str] = None
    combined_summary: Optional[str] = None
    blog_post: Optional[str] = None

def extract_text_from_video(video_path: str) -> str:
    """Extract text from video using speech recognition"""
    try:
        # Check if file exists
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail=f"Video file not found at path: {video_path}")
        
        # For now, we'll just return a placeholder since we're using separate audio file
        # In the future, we could add video content analysis here
        return "Video content description placeholder"
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

def extract_text_from_audio(audio_path: str) -> str:
    """Extract text from audio file using Whisper"""
    try:
        # Check if file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail=f"Audio file not found at path: {audio_path}")
        
        # Transcribe audio using Whisper
        result = model.transcribe(audio_path)
        return result["text"]
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

def create_summary(state: State) -> State:
    """Create a combined summary from video and audio text"""
    llm = ChatOpenAI(temperature=0)
    
    system_message = SystemMessage(content="You are a helpful assistant that creates concise summaries.")
    human_message = HumanMessage(content=f"Audio transcription: {state.audio_text}\n\nCreate a summary of the audio content.")
    
    response = llm.invoke([system_message, human_message])
    state.combined_summary = response.content
    return state

def generate_blog_post(state: State) -> State:
    """Generate a blog post from the combined summary"""
    llm = ChatOpenAI(temperature=0.7)
    
    system_message = SystemMessage(content="You are a creative blog writer. Create an engaging blog post based on the provided summary.")
    human_message = HumanMessage(content=f"Create a blog post based on this summary: {state.combined_summary}")
    
    response = llm.invoke([system_message, human_message])
    state.blog_post = response.content
    return state

@app.post("/process-media")
async def process_media(request: MediaRequest):
    try:
        # Initialize state
        state = State(messages=["Starting media processing..."])
        
        # Validate media path exists
        if not os.path.exists(request.media_path):
            raise HTTPException(status_code=404, detail=f"Media directory not found: {request.media_path}")
        
        # Process video (just validate it exists for now)
        video_path = os.path.join(request.media_path, request.video_file)
        state.messages.append(f"Validating video file: {video_path}")
        state.video_text = extract_text_from_video(video_path)
        state.messages.append("Video file validated.")
        
        # Process audio
        audio_path = os.path.join(request.media_path, request.audio_file)
        state.messages.append(f"Processing audio file: {audio_path}")
        try:
            state.audio_text = extract_text_from_audio(audio_path)
            state.messages.append("Audio processing completed.")
        except HTTPException as e:
            state.messages.append(f"Error processing audio: {str(e.detail)}")
            raise
        
        # Create summary
        state.messages.append("Creating summary from audio...")
        state = create_summary(state)
        state.messages.append("Summary created successfully.")
        
        # Generate blog post
        state.messages.append("Generating blog post...")
        state = generate_blog_post(state)
        state.messages.append("Blog post generated successfully.")
        
        return {
            "messages": state.messages,
            "blog_post": state.blog_post
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 