import React from 'react';

function ChatInterface({ messages }) {
  return (
    <div className="card max-w-4xl mx-auto max-h-96 overflow-y-auto">
      <h3 className="text-xl font-bold mb-4 text-gray-800">Conversation</h3>
      
      <div className="space-y-3">
        {messages.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            Ask a question to start learning! 📚
          </p>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${
                msg.role === 'user' ? 'message-user' : 'message-teacher'
              }`}
            >
              <div className="flex items-start space-x-2">
                <span className="text-2xl">
                  {msg.role === 'user' ? '🧑‍🎓' : '👨‍🏫'}
                </span>
                <div className="flex-1">
                  <p className="font-semibold text-sm text-gray-600 mb-1">
                    {msg.role === 'user' ? 'You' : 'Teacher'}
                  </p>
                  <p className="text-gray-800">{msg.content}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ChatInterface;