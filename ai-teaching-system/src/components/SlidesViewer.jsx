import React, { useState, useEffect } from 'react';

function SlidesViewer({ slidesData, pptUrl }) {
  const [currentSlide, setCurrentSlide] = useState(0);

  // Sync state if slidesData changes (e.g., loading a different presentation)
  useEffect(() => {
    setCurrentSlide(0);
  }, [slidesData]);

  // Handle Keyboard Navigation (Left/Right Arrows)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowRight') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentSlide, slidesData?.length]);

  if (!slidesData || slidesData.length === 0) return null;

  const nextSlide = () => {
    setCurrentSlide(prev => (prev + 1) % slidesData.length);
  };

  const prevSlide = () => {
    setCurrentSlide(prev => (prev - 1 + slidesData.length) % slidesData.length);
  };

  const slide = slidesData[currentSlide];

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-red-500 p-4 text-white flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl">📊</span>
          <div>
            <h3 className="font-bold text-lg">Presentation Slides</h3>
            <p className="text-sm text-orange-100">
              Slide {currentSlide + 1} of {slidesData.length}
            </p>
          </div>
        </div>
        {pptUrl && (
          <a // <--- FIXED: Added the missing <a> tag here
            href={pptUrl}
            download
            className="px-4 py-2 bg-white text-orange-600 rounded-lg hover:bg-orange-50 transition-colors font-medium text-sm"
          >
            ⬇️ Download PPT
          </a>
        )}
      </div>

      {/* Slide Display */}
      <div className="relative bg-gradient-to-br from-blue-50 to-purple-50 min-h-[500px] flex items-center justify-center p-8">
        
        {/* Slide Content */}
        <div className="w-full max-w-4xl">
          
          {/* Title Slide */}
          {slide.type === 'title' && (
            <div className="text-center">
              <h1 className="text-6xl font-bold text-blue-800 mb-4 animate-fadeIn">
                {slide.content}
              </h1>
              <div className="text-4xl mt-8">🎓</div>
            </div>
          )}

          {/* Definition Slide */}
          {slide.type === 'definition' && (
            <div className="animate-fadeIn">
              <h2 className="text-4xl font-bold text-blue-800 mb-8 pb-3 border-b-4 border-blue-500">
                📖 {slide.title}
              </h2>
              <p className="text-2xl text-gray-800 leading-relaxed bg-white p-6 rounded-xl shadow-md">
                {slide.content}
              </p>
            </div>
          )}

          {/* Points Slide */}
          {slide.type === 'points' && (
            <div className="animate-fadeIn">
              <h2 className="text-3xl font-bold text-blue-800 mb-6">
                📌 {slide.title}
              </h2>
              <div className="space-y-4">
                {slide.points?.map((point, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-4 bg-white p-4 rounded-lg shadow-md animate-slideIn"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <span className="text-3xl text-blue-600 font-bold">
                      •
                    </span>
                    <p className="text-xl text-gray-800 flex-1 leading-relaxed">
                      {point}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Navigation Arrows */}
        <button
          onClick={prevSlide}
          aria-label="Previous Slide"
          className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white p-3 rounded-full shadow-lg transition-all hover:scale-110"
        >
          <svg className="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <button
          onClick={nextSlide}
          aria-label="Next Slide"
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white p-3 rounded-full shadow-lg transition-all hover:scale-110"
        >
          <svg className="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Slide Dots */}
      <div className="p-4 bg-gray-50 flex items-center justify-center gap-2">
        {slidesData.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            aria-label={`Go to slide ${index + 1}`}
            className={`w-3 h-3 rounded-full transition-all ${
              index === currentSlide
                ? 'bg-blue-600 w-8'
                : 'bg-gray-300 hover:bg-gray-400'
            }`}
          />
        ))}
      </div>
    </div>
  );
}

export default SlidesViewer;