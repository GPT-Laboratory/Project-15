import React, { useState } from 'react';
import axios from 'axios';
import VideoInput from '../components/VideoInput';
import BlogDisplay from '../components/BlogDisplay';

const Home = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [blogPost, setBlogPost] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);

  const handleVideoSubmit = async (url) => {
    setLoading(true);
    setError(null);
    setBlogPost(null);
    
    try {
      const response = await axios.post('/api/process', {
        video_url: url
      });
      
      setVideoUrl(url);
      setBlogPost(response.data.blog_post);
    } catch (err) {
      console.error('Error processing video:', err);
      setError(
        err.response?.data?.error || 
        'An error occurred while processing the video. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight">
          <span className="text-primary-600">YouTube</span> to Blog Post Converter
        </h1>
        <p className="mt-3 max-w-3xl mx-auto text-xl text-gray-500 sm:mt-4">
          Transform any YouTube video into a well-structured, SEO-friendly blog post with just a few clicks.
        </p>
      </div>
      
      <div className="max-w-3xl mx-auto">
        <VideoInput onVideoSubmit={handleVideoSubmit} isLoading={loading} />
        
        {error && (
          <div className="mt-8 rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {blogPost && <BlogDisplay blogContent={blogPost} videoUrl={videoUrl} />}
        
        {loading && (
          <div className="mt-8 flex justify-center">
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
              <p className="mt-4 text-gray-600">Processing your video. This may take a few minutes...</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="mt-20 max-w-5xl mx-auto">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-600 text-white mb-4">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900">Easy Upload</h3>
            <p className="mt-2 text-base text-gray-500 text-center">
              Simply paste a YouTube URL or drag and drop a file with URLs to get started.
            </p>
          </div>
          
          <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-600 text-white mb-4">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900">AI-Powered</h3>
            <p className="mt-2 text-base text-gray-500 text-center">
              Our advanced AI processes the video content and generates high-quality blog posts.
            </p>
          </div>
          
          <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-600 text-white mb-4">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900">Ready to Publish</h3>
            <p className="mt-2 text-base text-gray-500 text-center">
              Download your blog post in Markdown format, ready to publish on any platform.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 