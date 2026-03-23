import React, { useState } from 'react';

function QuestionInput({ onAskQuestion, loading, isTeaching }) {
  const [question, setQuestion] = useState('');
  const [subject, setSubject] = useState('general');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !loading) {
      onAskQuestion(question, subject);
      setQuestion('');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
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
            disabled={loading}
          >
            <option value="general">General</option>
            <option value="math">Mathematics</option>
            <option value="science">Science</option>
            <option value="physics">Physics</option>
            <option value="chemistry">Chemistry</option>
            <option value="biology">Biology</option>
            <option value="computer">Computer Science</option>
          </select>
        </div>

        {/* Question Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ask your question
          </label>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question here... (e.g., Explain quadratic equations)"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows="3"
            disabled={loading}
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            loading || !question.trim()
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg transform hover:scale-105'
          }`}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              Processing...
            </span>
          ) : (
            '🎓 Ask Teacher'
          )}
        </button>
      </form>

      {/* Quick Examples */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 mb-2">Quick examples:</p>
        <div className="flex flex-wrap gap-2">
          {[
            'Explain photosynthesis',
            'What is quadratic formula?',
            'Solve 2x + 5 = 11'
          ].map((example) => (
            <button
              key={example}
              onClick={() => setQuestion(example)}
              className="text-xs px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors"
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default QuestionInput;