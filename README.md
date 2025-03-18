pip insta# Media Processor with AI Blog Generation

This application processes video and audio files to generate AI-powered blog posts using LangGraph and LangChain. It features a React frontend and a Python FastAPI backend.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key

## Setup

### Backend Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_api_key_here
```

4. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

The backend will run on http://localhost:8000

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the frontend development server:
```bash
npm start
```

The frontend will run on http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser
2. Enter the path to your media files directory
3. Enter the names of your video and audio files
4. Click "Start Generation"
5. Wait for the process to complete
6. View the generated blog post

## Features

- Video and audio file processing
- Speech-to-text conversion
- AI-powered text summarization
- Blog post generation
- Real-time process status updates
- Modern Material-UI interface

## Note

Make sure your media files are accessible to the backend server. The application expects the media files to be in the specified directory path. 