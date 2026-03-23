import React, { useState, useEffect } from 'react';

function AssignmentViewer({ assignmentData, assignmentUrl, answersUrl }) {
  const [userAnswers, setUserAnswers] = useState({});
  const [showAnswers, setShowAnswers] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  // Reset state when new assignment data is loaded
  useEffect(() => {
    setUserAnswers({});
    setShowAnswers(false);
    setSubmitted(false);
  }, [assignmentData]);

  if (!assignmentData || !assignmentData.questions) return null;

  const handleAnswerChange = (questionIndex, answer) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionIndex]: answer
    }));
  };

  const calculateScore = () => {
    let correct = 0;
    assignmentData.questions.forEach((q, i) => {
      const userAnswer = (userAnswers[i] || '').toLowerCase().trim();
      const correctAnswer = (q.answer || '').toLowerCase().trim();
      if (userAnswer === correctAnswer) {
        correct++;
      }
    });
    return correct;
  };

  const handleSubmit = () => {
    setSubmitted(true);
    setShowAnswers(true);
  };

  const score = submitted ? calculateScore() : 0;
  const total = assignmentData.questions.length;

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-teal-500 p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">📝 Practice Assignment</h2>
            <p className="text-green-100">
              {total} Questions • Test your understanding
            </p>
          </div>
          <div className="flex gap-2">
            {assignmentUrl && (
              <a // <--- FIXED: Added missing <a> tag
                href={assignmentUrl}
                download
                className="px-4 py-2 bg-white text-green-600 rounded-lg hover:bg-green-50 transition-colors font-medium"
              >
                ⬇️ Download
              </a>
            )}
            {answersUrl && (
              <a // <--- FIXED: Added missing <a> tag
                href={answersUrl}
                download
                className="px-4 py-2 bg-white text-green-600 rounded-lg hover:bg-green-50 transition-colors font-medium"
              >
                📋 Answers
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Score Card (if submitted) */}
      {submitted && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 border-b">
          <div className="text-center">
            <div className="text-5xl font-bold text-blue-600 mb-2">
              {score} / {total}
            </div>
            <p className="text-gray-700 text-lg">
              {score === total ? '🎉 Perfect Score!' : 
               score >= total * 0.7 ? '👍 Good Job!' :
               '💪 Keep Practicing!'}
            </p>
            <div className="mt-4">
              <div className="bg-gray-200 rounded-full h-4 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-green-400 to-green-600 h-full transition-all duration-1000"
                  style={{ width: `${(score / total) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Questions */}
      <div className="p-6 max-h-[600px] overflow-y-auto space-y-6">
        {assignmentData.questions.map((question, qIndex) => {
          const isCorrect = submitted && 
            (userAnswers[qIndex] || '').toLowerCase().trim() === (question.answer || '').toLowerCase().trim();
          
          return (
            <div
              key={qIndex}
              className={`p-6 rounded-xl border-2 transition-all ${
                submitted
                  ? isCorrect
                    ? 'bg-green-50 border-green-300'
                    : 'bg-red-50 border-red-300'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              
              {/* Question */}
              <div className="flex items-start gap-3 mb-4">
                <span className="text-2xl font-bold text-blue-600">
                  {qIndex + 1}.
                </span>
                <p className="flex-1 text-lg text-gray-800 font-medium">
                  {question.question}
                </p>
                {submitted && (
                  <span className="text-2xl">
                    {isCorrect ? '✅' : '❌'}
                  </span>
                )}
              </div>

              {/* Options (if MCQ) */}
              {question.options && question.options.length > 0 && (
                <div className="ml-10 space-y-2 mb-4">
                  {question.options.map((option, oIndex) => (
                    <label
                      key={oIndex}
                      className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors ${
                        userAnswers[qIndex] === option
                          ? 'bg-blue-100 border-2 border-blue-500'
                          : 'bg-white border border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      <input
                        type="radio"
                        name={`question-${qIndex}`}
                        value={option}
                        checked={userAnswers[qIndex] === option}
                        onChange={(e) => handleAnswerChange(qIndex, e.target.value)}
                        disabled={submitted}
                        className="w-5 h-5"
                      />
                      <span className="text-gray-800">{option}</span>
                    </label>
                  ))}
                </div>
              )}

              {/* Text Answer (if not MCQ) */}
              {(!question.options || question.options.length === 0) && (
                <div className="ml-10">
                  <input
                    type="text"
                    placeholder="Type your answer here..."
                    value={userAnswers[qIndex] || ''}
                    onChange={(e) => handleAnswerChange(qIndex, e.target.value)}
                    disabled={submitted}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
                  />
                </div>
              )}

              {/* Show Answer (if submitted) */}
              {showAnswers && (
                <div className="ml-10 mt-4 p-4 bg-white rounded-lg border-l-4 border-green-500">
                  <p className="text-sm font-semibold text-green-700 mb-1">
                    ✓ Correct Answer:
                  </p>
                  <p className="text-gray-800 font-medium mb-2">
                    {question.answer}
                  </p>
                  {question.explanation && (
                    <>
                      <p className="text-sm font-semibold text-blue-700 mb-1">
                        💡 Explanation:
                      </p>
                      <p className="text-gray-700 text-sm">
                        {question.explanation}
                      </p>
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Action Buttons */}
      <div className="p-6 bg-gray-50 border-t">
        {!submitted ? (
          <button
            onClick={handleSubmit}
            disabled={Object.keys(userAnswers).length === 0}
            className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${
              Object.keys(userAnswers).length === 0
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-green-500 to-teal-500 text-white hover:shadow-lg transform hover:scale-105'
            }`}
          >
            {Object.keys(userAnswers).length === 0
              ? '👆 Answer questions to submit'
              : '🚀 Submit Assignment'}
          </button>
        ) : (
          <button
            onClick={() => {
              setUserAnswers({});
              setSubmitted(false);
              setShowAnswers(false);
            }}
            className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
          >
            🔄 Try Again
          </button>
        )}
      </div>
    </div>
  );
}

export default AssignmentViewer;