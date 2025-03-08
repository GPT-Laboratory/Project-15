import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const BlogDisplay = ({ blogContent, videoUrl }) => {
  const [copied, setCopied] = useState(false);

  const handleCopyClick = () => {
    navigator.clipboard.writeText(blogContent).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handleDownloadClick = () => {
    const element = document.createElement('a');
    const file = new Blob([blogContent], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = 'blog-post.md';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="card mb-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Generated Blog Post</h2>
        <div className="flex space-x-2">
          <button 
            onClick={handleCopyClick} 
            className="btn-secondary flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
              <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
            </svg>
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button 
            onClick={handleDownloadClick} 
            className="btn-secondary flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
            Download
          </button>
        </div>
      </div>
      
      {videoUrl && (
        <div className="mb-6 p-4 bg-gray-50 rounded-md">
          <p className="text-gray-500 text-sm">Generated from:</p>
          <a 
            href={videoUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-primary-600 hover:text-primary-700 truncate block"
          >
            {videoUrl}
          </a>
        </div>
      )}
      
      <div className="bg-gray-50 rounded-md p-6 prose prose-sm sm:prose max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {blogContent}
        </ReactMarkdown>
      </div>
    </div>
  );
};

export default BlogDisplay; 