import React from 'react';

function TeacherVideo({ videoUrl, isSpeaking }) {
  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="bg-white rounded-xl shadow-2xl overflow-hidden border-4 border-blue-500">
        {videoUrl ? (
          // Actual video player
          <div className="relative">
            <video
              key={videoUrl}
              src={videoUrl}
              autoPlay
              className="w-64 h-48 object-cover"
              onError={(e) => console.error('Video error:', e)}
            >
              Your browser does not support video.
            </video>
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2">
              <p className="text-white text-xs text-center font-medium">
                👩‍🏫 AI Teacher
              </p>
            </div>
          </div>
        ) : (
          // Placeholder when no video
          <div className="w-64 h-48 bg-gradient-to-br from-blue-500 to-purple-600 flex flex-col items-center justify-center">
            <div className={`text-6xl mb-2 ${isSpeaking ? 'animate-bounce' : ''}`}>
              👩‍🏫
            </div>
            <p className="text-white font-medium">
              {isSpeaking ? '🎤 Speaking...' : 'Ready to teach'}
            </p>
            {isSpeaking && (
              <div className="flex gap-1 mt-2">
                <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default TeacherVideo;