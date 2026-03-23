import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { userAPI } from '../services/api';

function Dashboard() {
  const { user, logout } = useAuth();
  const [lessons, setLessons] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setError(null);
      
      const [lessonsData, statsData] = await Promise.all([
        userAPI.getLessons(0, 20),
        userAPI.getStats()
      ]);
      
      setLessons(lessonsData.lessons || []);
      setStats(statsData);
      
      console.log('📊 Dashboard data loaded:', {
        lessons: lessonsData.lessons?.length,
        stats: statsData
      });
    } catch (error) {
      console.error('❌ Failed to fetch dashboard data:', error);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteLesson = async (lessonId) => {
    if (!window.confirm('Are you sure you want to delete this lesson?')) return;
    
    try {
      await userAPI.deleteLesson(lessonId);
      
      // Remove lesson from list
      setLessons(lessons.filter(l => l.id !== lessonId));
      
      // Update stats
      if (stats) {
        setStats({
          ...stats,
          total_lessons: Math.max(0, stats.total_lessons - 1)
        });
      }
      
      console.log('✅ Lesson deleted successfully');
    } catch (error) {
      console.error('❌ Failed to delete lesson:', error);
      alert('Failed to delete lesson. Please try again.');
    }
  };

  const handleViewLesson = async (lessonId) => {
    try {
      const lessonDetails = await userAPI.getLesson(lessonId);
      console.log('📖 Lesson details:', lessonDetails);
      // You can navigate to a lesson detail page or show in modal
      // For now, just log it
    } catch (error) {
      console.error('❌ Failed to fetch lesson details:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">📚</div>
          <p className="text-gray-600 text-lg">Loading your dashboard...</p>
          <div className="mt-4">
            <div className="animate-spin inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-4xl">🎓</span>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">
                  My Dashboard
                </h1>
                <p className="text-sm text-gray-600">
                  Welcome back, <span className="font-semibold">{user?.username || 'Student'}</span>!
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => navigate('/')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all transform hover:scale-105 font-medium shadow-md"
              >
                🎬 New Lesson
              </button>
              <button
                onClick={logout}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all font-medium"
              >
                🚪 Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        
        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mb-6 flex items-center gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="font-semibold">Error</p>
              <p>{error}</p>
            </div>
            <button
              onClick={fetchDashboardData}
              className="ml-auto px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Retry
            </button>
          </div>
        )}

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            
            {/* Total Lessons */}
            <div className="bg-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-all">
              <div className="flex items-center gap-4">
                <div className="text-5xl">📚</div>
                <div className="flex-1">
                  <p className="text-4xl font-bold text-blue-600 mb-1">
                    {stats.total_lessons}
                  </p>
                  <p className="text-gray-600 font-medium">Total Lessons</p>
                </div>
              </div>
            </div>

            {/* Subjects Studied */}
            <div className="bg-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-all">
              <div className="flex items-center gap-4">
                <div className="text-5xl">🎯</div>
                <div className="flex-1">
                  <p className="text-4xl font-bold text-purple-600 mb-1">
                    {stats.subjects_studied}
                  </p>
                  <p className="text-gray-600 font-medium">Subjects</p>
                  {stats.subjects && stats.subjects.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {stats.subjects.slice(0, 3).map((subject, idx) => (
                        <span
                          key={idx}
                          className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded-full"
                        >
                          {subject}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Member Since */}
            <div className="bg-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition-all">
              <div className="flex items-center gap-4">
                <div className="text-5xl">📅</div>
                <div className="flex-1">
                  <p className="text-lg font-bold text-green-600 mb-1">
                    {new Date(stats.member_since).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric'
                    })}
                  </p>
                  <p className="text-gray-600 font-medium">Member Since</p>
                  {stats.last_lesson && (
                    <p className="text-xs text-gray-500 mt-1">
                      Last activity: {new Date(stats.last_lesson).toLocaleDateString()}
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Lessons List */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              📖 Your Lessons
            </h2>
            {lessons.length > 0 && (
              <span className="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
                {lessons.length} lesson{lessons.length !== 1 ? 's' : ''}
              </span>
            )}
          </div>
          
          {lessons.length === 0 ? (
            <div className="text-center py-16">
              <div className="text-7xl mb-4">📚</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">
                No lessons yet!
              </h3>
              <p className="text-gray-600 mb-6">
                Start your learning journey by creating your first lesson
              </p>
              <button
                onClick={() => navigate('/')}
                className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all font-semibold"
              >
                🚀 Create Your First Lesson
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {lessons.map((lesson) => (
                <div
                  key={lesson.id}
                  className="border border-gray-200 rounded-xl p-5 hover:shadow-lg transition-all bg-gradient-to-r from-white to-gray-50"
                >
                  <div className="flex items-start justify-between gap-4">
                    
                    {/* Lesson Content */}
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-800 mb-2 line-clamp-2">
                        {lesson.question}
                      </h3>
                      
                      {/* Metadata */}
                      <div className="flex flex-wrap items-center gap-3 text-sm text-gray-600 mb-3">
                        <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full font-medium">
                          📚 {lesson.subject}
                        </span>
                        <span className="flex items-center gap-1">
                          📅 {new Date(lesson.created_at).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric'
                          })}
                        </span>
                        <span className="flex items-center gap-1">
                          🕐 {new Date(lesson.created_at).toLocaleTimeString('en-US', {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                      </div>
                      
                      {/* Download Links */}
                      <div className="flex flex-wrap gap-2">
                        {lesson.video_url && (
                          <a 
                            href={lesson.video_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-3 py-1.5 bg-red-100 text-red-700 rounded-lg text-sm hover:bg-red-200 transition-colors font-medium flex items-center gap-1"
                          >
                            🎬 Video
                          </a>
                        )}
                        {lesson.pdf_url && (
                          <a 
                            href={lesson.pdf_url}
                            download
                            className="px-3 py-1.5 bg-green-100 text-green-700 rounded-lg text-sm hover:bg-green-200 transition-colors font-medium flex items-center gap-1"
                          >
                            📄 PDF
                          </a>
                        )}
                        {lesson.ppt_url && (
                          <a 
                            href={lesson.ppt_url}
                            download
                            className="px-3 py-1.5 bg-orange-100 text-orange-700 rounded-lg text-sm hover:bg-orange-200 transition-colors font-medium flex items-center gap-1"
                          >
                            📊 PPT
                          </a>
                        )}
                        {lesson.assignment_url && (
                          <a 
                            href={lesson.assignment_url}
                            download
                            className="px-3 py-1.5 bg-purple-100 text-purple-700 rounded-lg text-sm hover:bg-purple-200 transition-colors font-medium flex items-center gap-1"
                          >
                            📝 Assignment
                          </a>
                        )}
                        {lesson.answers_url && (
                          <a 
                            href={lesson.answers_url}
                            download
                            className="px-3 py-1.5 bg-teal-100 text-teal-700 rounded-lg text-sm hover:bg-teal-200 transition-colors font-medium flex items-center gap-1"
                          >
                            ✅ Answers
                          </a>
                        )}
                      </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="flex flex-col gap-2">
                      <button
                        onClick={() => handleDeleteLesson(lesson.id)}
                        className="text-red-600 hover:text-red-800 hover:bg-red-50 p-2 rounded-lg transition-all"
                        title="Delete lesson"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Actions */}
        {lessons.length > 0 && (
          <div className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
            <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
              ⚡ Quick Actions
            </h3>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => navigate('/')}
                className="px-4 py-2 bg-white text-gray-800 rounded-lg hover:shadow-md transition-all font-medium border border-gray-200"
              >
                ➕ Create New Lesson
              </button>
              <button
                onClick={fetchDashboardData}
                className="px-4 py-2 bg-white text-gray-800 rounded-lg hover:shadow-md transition-all font-medium border border-gray-200"
              >
                🔄 Refresh
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;