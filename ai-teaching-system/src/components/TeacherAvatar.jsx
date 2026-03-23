function TeacherAvatar({ isSpeaking, videoUrl }) {
  return (
    <div className="flex justify-center">
      <div className="bg-white rounded-2xl shadow-xl p-4 w-full max-w-2xl">
        
        {/* Video Player - shows when video is ready */}
        {videoUrl ? (
          <div>
            <video
              key={videoUrl}  // Re-render when URL changes
              src={videoUrl}
              autoPlay
              controls
              className="w-full rounded-xl"
              style={{ maxHeight: '400px' }}
            >
              Your browser does not support video.
            </video>
            <p className="text-center text-sm text-gray-500 mt-2">
              🎬 AI Teacher Speaking...
            </p>
          </div>
        ) : (
          /* Static avatar when no video */
          <div className="text-center py-12">
            <div className={`text-8xl mb-4 ${isSpeaking ? 'animate-bounce' : ''}`}>
              👩‍🏫
            </div>
            <p className="text-gray-600 font-medium">
              {isSpeaking ? '🎤 Teacher is speaking...' : '💬 Ask a question!'}
            </p>
            
            {/* Speaking animation */}
            {isSpeaking && (
              <div className="flex justify-center gap-1 mt-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default TeacherAvatar;