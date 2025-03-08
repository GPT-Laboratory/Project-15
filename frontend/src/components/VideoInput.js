import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';

const VideoInput = ({ onVideoSubmit, isLoading }) => {
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!videoUrl) {
      setError('Please enter a YouTube URL');
      return;
    }
    
    // Basic YouTube URL validation
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
    if (!youtubeRegex.test(videoUrl)) {
      setError('Please enter a valid YouTube URL');
      return;
    }
    
    setError('');
    onVideoSubmit(videoUrl);
  };

  // Dropzone configuration
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'text/plain': ['.txt'],
    },
    onDrop: (acceptedFiles) => {
      // Handle dropped files (e.g., text files with YouTube URLs)
      const file = acceptedFiles[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const content = e.target.result;
          // Assume file contains a YouTube URL
          setVideoUrl(content.trim());
        };
        reader.readAsText(file);
      }
    },
  });

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Convert YouTube Video to Blog Post</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="videoUrl" className="block text-sm font-medium text-gray-700 mb-1">
            YouTube Video URL
          </label>
          <input
            type="text"
            id="videoUrl"
            name="videoUrl"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            className="input-field"
            disabled={isLoading}
          />
          {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
        </div>
        
        <div 
          {...getRootProps()} 
          className={`border-2 border-dashed rounded-md p-6 mb-6 text-center cursor-pointer hover:bg-gray-50 transition-colors ${
            isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300'
          }`}
        >
          <input {...getInputProps()} disabled={isLoading} />
          <p className="text-gray-600">Drag and drop a file with a YouTube URL, or click to select a file</p>
          <p className="text-sm text-gray-500 mt-1">Accepts .txt files</p>
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            className="btn-primary"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </>
            ) : (
              'Generate Blog Post'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default VideoInput; 