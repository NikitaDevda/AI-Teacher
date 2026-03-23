import React, { useState, useEffect } from 'react';

function VideoPlayer({ videoUrl, loading }) {
  const [videoReady, setVideoReady] = useState(false);

  useEffect(() => {
    if (videoUrl) {
      setVideoReady(true);
    }
  }, [videoUrl]);

  if (loading) {
    return (
      <div className="bg-white h-full rounded-lg shadow-lg flex flex-col items-center justify-center p-8">
        <div className="text-center">
          <svg className="animate-spin h-16 w-16 text-blue-600 mx-auto mb-4" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          <p className="text-xl font-semibold text-gray-800 mb-2">
            🎬 Generating Video...
          </p>
          <p className="text-sm text-gray-600">
            Creating your personalized lesson video
          </p>
          <div className="mt-4 space-y-2 text-left max-w-md mx-auto">
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <span className="text-green-500">✓</span> Analyzing content
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <span className="text-green-500">✓</span> Generating scenes
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500 animate-pulse">
              <span className="text-blue-500">⟳</span> Rendering video...
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!videoUrl && !loading) {
    return (
      <div className="bg-white h-full rounded-lg shadow-lg flex flex-col items-center justify-center p-8">
        <div className="text-center">
          <p className="text-6xl mb-4">🎓</p>
          <p className="text-2xl font-semibold text-gray-800 mb-2">
            Ready to Learn!
          </p>
          <p className="text-gray-600">
            Ask a question to generate your personalized video lesson
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-black h-full rounded-lg shadow-2xl overflow-hidden">
      {/* Video Player */}
      <video
        key={videoUrl}
        controls
        autoPlay
        className="w-full h-full object-contain"
        style={{ maxHeight: '100%' }}
      >
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      
      {/* Video Info Overlay */}
      {videoReady && (
        <div className="absolute top-4 left-4 bg-black/70 text-white px-4 py-2 rounded-lg backdrop-blur-sm">
          <p className="text-sm font-medium">🎬 AI Generated Lesson</p>
        </div>
      )}
    </div>
  );
}

export default VideoPlayer;