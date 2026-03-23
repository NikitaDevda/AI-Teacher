import React, { useEffect, useState } from 'react';

function Whiteboard({ sections, currentSectionIndex, isTeaching }) {
  const [visibleSections, setVisibleSections] = useState([]);

  useEffect(() => {
    if (!sections || sections.length === 0) {
      setVisibleSections([]);
      return;
    }

    // Show sections up to current index
    const toShow = sections.slice(0, currentSectionIndex + 1);
    setVisibleSections(toShow);
  }, [sections, currentSectionIndex]);

  const getPointIcon = (type) => {
    const icons = {
      equation: '🔢',
      bullet: '•',
      keypoint: '⭐',
      text: '→'
    };
    return icons[type] || '•';
  };

  const getPointStyle = (type) => {
    const styles = {
      equation: 'bg-yellow-50 border-yellow-400 text-xl font-mono',
      keypoint: 'bg-red-50 border-red-400 font-semibold',
      bullet: 'bg-white border-gray-200',
      text: 'bg-blue-50 border-blue-200'
    };
    return styles[type] || 'bg-white border-gray-200';
  };

  return (
    <div className="bg-white h-full rounded-lg shadow-lg p-8 relative overflow-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-gray-300 sticky top-0 bg-white z-10">
        <div className="flex items-center gap-2">
          <span className="text-2xl">📝</span>
          <h2 className="text-2xl font-bold text-gray-800">Whiteboard</h2>
        </div>
        {isTeaching && (
          <div className="flex items-center gap-2 text-green-600">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="font-medium">Teaching...</span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="space-y-8">
        {visibleSections.length > 0 ? (
          visibleSections.map((section, sectionIdx) => (
            <div 
              key={sectionIdx}
              className="animate-fadeIn"
              style={{ animationDelay: `${sectionIdx * 0.2}s` }}
            >
              {/* HEADING */}
              <div className="mb-4">
                <h3 className="text-3xl font-bold text-blue-800 pb-2 border-b-4 border-blue-500 inline-block">
                  📌 {section.heading}
                </h3>
              </div>

              {/* DEFINITION */}
              {section.definition && (
                <div className="mb-4 bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
                  <p className="text-lg text-gray-800 leading-relaxed">
                    <span className="font-semibold text-blue-700">Definition: </span>
                    {section.definition}
                  </p>
                </div>
              )}

              {/* BULLET POINTS */}
              {section.points.length > 0 && (
                <div className="space-y-3 ml-4">
                  {section.points.map((point, pointIdx) => (
                    <div
                      key={pointIdx}
                      className={`flex items-start gap-3 p-3 rounded-lg border-l-4 ${getPointStyle(point.type)} animate-slideIn`}
                      style={{ animationDelay: `${(sectionIdx * 0.2) + (pointIdx * 0.1)}s` }}
                    >
                      <span className="text-xl flex-shrink-0 mt-1">
                        {getPointIcon(point.type)}
                      </span>
                      <p className="text-lg text-gray-800 leading-relaxed">
                        {point.text}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-6xl mb-4">🎓</p>
            <p className="text-2xl font-semibold mb-2">Ready to Learn!</p>
            <p className="text-lg">Ask a question to start the lesson</p>
          </div>
        )}
      </div>

      {/* Progress Indicator */}
      {visibleSections.length > 0 && sections.length > 0 && (
        <div className="fixed bottom-20 right-6 bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg">
          <span className="text-sm font-medium">
            Section {visibleSections.length} / {sections.length}
          </span>
        </div>
      )}
    </div>
  );
}

export default Whiteboard;