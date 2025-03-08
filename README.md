# YouTube to Blog Post Converter

This application converts YouTube videos into blog posts using AI-powered language processing.

## Features

- Simple drag-and-drop or URL input for YouTube videos
- Automatic transcription of video content
- AI-generated blog posts from video content
- Modern React frontend with Tailwind CSS
- Python backend with LangChain and LangGraph

## Project Structure

```
project/
├── backend/             # Python Flask API
│   ├── app.py           # Main Flask application
│   ├── requirements.txt # Python dependencies
│   ├── services/        # Core services
│   │   ├── youtube.py   # YouTube video processing
│   │   ├── transcription.py # Video transcription
│   │   └── blog_generator.py # LangChain/Graph blog generation
│   └── ...
└── frontend/           # React application
    ├── package.json    # Node dependencies
    ├── public/         # Static files
    ├── src/            # React source code
    └── ...
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. Open your browser and navigate to http://localhost:3000

## Technologies Used

- **Backend**:
  - Python 3.9+
  - Flask
  - LangChain
  - LangGraph
  - yt-dlp (YouTube video processing)
  
- **Frontend**:
  - React
  - Tailwind CSS
  - Axios (for API requests) 