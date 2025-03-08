import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="border-t border-gray-200 pt-6">
          <p className="text-center text-sm text-gray-500">
            &copy; {new Date().getFullYear()} YouTube to Blog Converter. All rights reserved.
          </p>
          <p className="text-center text-sm text-gray-500 mt-2">
            Built with React, Tailwind CSS, Python, LangChain, and LangGraph
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 