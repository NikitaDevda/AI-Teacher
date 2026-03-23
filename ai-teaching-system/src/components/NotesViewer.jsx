import React, { useState, useEffect } from 'react';

function NotesViewer({ notesData, pdfUrl }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedNotes, setEditedNotes] = useState(notesData);

  // Sync state if notesData prop changes externally
  useEffect(() => {
    if (notesData) {
      setEditedNotes(notesData);
    }
  }, [notesData]);

  if (!notesData || !editedNotes) return null;

  const handleEdit = (field, value) => {
    setEditedNotes(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePointEdit = (index, value) => {
    const newPoints = [...editedNotes.points];
    newPoints[index] = { ...newPoints[index], text: value };
    setEditedNotes(prev => ({
      ...prev,
      points: newPoints
    }));
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">📄 Study Notes</h2>
            <p className="text-blue-100 text-sm">
              {/* Added optional chaining to prevent crash if date is missing */}
              {notesData.generated_at ? new Date(notesData.generated_at).toLocaleDateString() : 'No date'}
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
            >
              {isEditing ? '✅ Done' : '✏️ Edit'}
            </button>
            <button
              onClick={handlePrint}
              className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
            >
              🖨️ Print
            </button>
            {pdfUrl && (
              <a // <--- FIXED: Added the missing 'a' tag here
                href={pdfUrl}
                download
                className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
              >
                ⬇️ Download
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-8 max-h-[600px] overflow-y-auto">
        
        {/* Title */}
        {isEditing ? (
          <input
            type="text"
            value={editedNotes.heading || ''}
            onChange={(e) => handleEdit('heading', e.target.value)}
            className="w-full text-3xl font-bold text-blue-800 mb-6 p-2 border-b-2 border-blue-300 focus:border-blue-600 outline-none"
          />
        ) : (
          <h1 className="text-3xl font-bold text-blue-800 mb-6 pb-2 border-b-2 border-blue-300">
            {editedNotes.heading}
          </h1>
        )}

        {/* Definition */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-3 flex items-center gap-2">
            📖 Definition
          </h2>
          {isEditing ? (
            <textarea
              value={editedNotes.definition || ''}
              onChange={(e) => handleEdit('definition', e.target.value)}
              rows="3"
              className="w-full p-3 bg-blue-50 rounded-lg border border-blue-200 focus:border-blue-500 outline-none resize-none"
            />
          ) : (
            <p className="text-lg text-gray-700 bg-blue-50 p-4 rounded-lg leading-relaxed">
              {editedNotes.definition}
            </p>
          )}
        </div>

        {/* Key Points */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            📌 Key Points
          </h2>
          <div className="space-y-3">
            {editedNotes.points?.map((point, index) => (
              <div key={index} className="flex items-start gap-3">
                <span className="text-blue-600 font-bold text-lg mt-1">
                  {index + 1}.
                </span>
                {isEditing ? (
                  <textarea
                    value={point.text || ''}
                    onChange={(e) => handlePointEdit(index, e.target.value)}
                    rows="2"
                    className="flex-1 p-2 bg-gray-50 rounded-lg border border-gray-300 focus:border-blue-500 outline-none resize-none"
                  />
                ) : (
                  <p className="flex-1 text-gray-700 leading-relaxed">
                    {point.text}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Additional Notes Section */}
        <div className="border-t pt-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-3">
            📝 Your Notes
          </h2>
          <textarea
            placeholder="Add your own notes here..."
            rows="5"
            className="w-full p-4 bg-yellow-50 border border-yellow-300 rounded-lg focus:border-yellow-500 outline-none resize-none"
          />
        </div>
      </div>
    </div>
  );
}

export default NotesViewer;