import React, { useState } from 'react';

function DoubtInput({ onAskQuestion, onInterrupt, isTeacherSpeaking, loading }) {
  const [input, setInput] = useState('');
  const [subject, setSubject] = useState('Mathematics');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    if (isTeacherSpeaking) {
      // If teacher is speaking, this is an interruption
      onInterrupt(input);
    } else {
      // Normal question
      onAskQuestion(input, subject);
    }

    setInput('');
  };

  return (
    <div className="card max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Subject Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Subject
          </label>
          <select
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option>Mathematics</option>
            <option>Physics</option>
            <option>Chemistry</option>
            <option>Biology</option>
            <option>Computer Science</option>
          </select>
        </div>

        {/* Question Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {isTeacherSpeaking ? '⚠️ Interrupt with your doubt' : 'Ask your question'}
          </label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              isTeacherSpeaking
                ? "Type your doubt to interrupt the teacher..."
                : "Example: Quadratic equation kya hai?"
            }
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows="3"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className={`w-full ${
            isTeacherSpeaking ? 'btn-danger' : 'btn-primary'
          }`}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Processing...
            </span>
          ) : isTeacherSpeaking ? (
            '⚠️ Interrupt & Ask Doubt'
          ) : (
            '🚀 Ask Teacher'
          )}
        </button>

        {/* Helper Text */}
        {isTeacherSpeaking && (
          <p className="text-sm text-orange-600 text-center">
            Teacher is currently speaking. Your question will interrupt the current explanation.
          </p>
        )}
      </form>
    </div>
  );
}

export default DoubtInput;