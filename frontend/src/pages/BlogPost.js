import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// This component would be used in a future version to display saved blog posts
// Currently, it's a placeholder for future functionality
const BlogPost = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [blogPost, setBlogPost] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // In a real implementation, this would fetch the blog post from an API
    // For now, it's a placeholder that simulates loading and then shows an error
    const fetchBlogPost = async () => {
      setLoading(true);
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // For now, we'll just set an error since we don't have a backend for storing blog posts yet
        setError('This feature is not yet implemented. Blog posts are not currently saved on the server.');
      } catch (err) {
        setError('Failed to load blog post. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchBlogPost();
  }, [id]);

  const handleBackClick = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto py-8 px-4">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-3xl mx-auto py-8 px-4">
        <div className="bg-white shadow-md rounded-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Blog Post Not Found</h1>
          <p className="text-gray-600 mb-6">{error}</p>
          <button onClick={handleBackClick} className="btn-primary">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  // This would render the blog post if we had one
  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <div className="bg-white shadow-md rounded-lg p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{blogPost?.title}</h1>
        <p className="text-gray-500 mb-6">Generated from: {blogPost?.videoUrl}</p>
        
        <div className="prose prose-sm sm:prose lg:prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {blogPost?.content || ''}
          </ReactMarkdown>
        </div>
        
        <div className="mt-8">
          <button onClick={handleBackClick} className="btn-secondary">
            Back to Home
          </button>
        </div>
      </div>
    </div>
  );
};

export default BlogPost; 