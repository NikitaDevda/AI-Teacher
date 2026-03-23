// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { v4 as uuidv4 } from 'uuid';
// import { useAuth } from '../context/AuthContext';
// import VideoPlayer from '../components/VideoPlayer';
// import QuestionInput from '../components/QuestionInput';
// import NotesViewer from '../components/NotesViewer';
// import SlidesViewer from '../components/SlidesViewer';
// import AssignmentViewer from '../components/AssignmentViewer';
// import { teachingAPI } from '../services/api';

// function HomePage() {
//   const [sessionId, setSessionId] = useState(null);
//   const [videoUrl, setVideoUrl] = useState(null);
//   const [loading, setLoading] = useState(false);
  
//   const [notesData, setNotesData] = useState(null);
//   const [slidesData, setSlidesData] = useState(null);
//   const [assignmentData, setAssignmentData] = useState(null);
//   const [downloadUrls, setDownloadUrls] = useState({});
  
//   const [activeTab, setActiveTab] = useState('video');
  
//   const { user, isAuthenticated, logout } = useAuth();
//   const navigate = useNavigate();

//   useEffect(() => {
//     setSessionId(uuidv4());
//   }, []);

//   const handleAskQuestion = async (question, subject) => {
//     setLoading(true);
//     setVideoUrl(null);
//     setNotesData(null);
//     setSlidesData(null);
//     setAssignmentData(null);
//     setActiveTab('video');

//     try {
//       const response = await teachingAPI.askQuestion(question, sessionId, subject);
      
//       if (response.video_url) {
//         setVideoUrl(response.video_url);
//       }
      
//       if (response.notes_content) {
//         setNotesData(response.notes_content);
//       }
      
//       if (response.slides_content) {
//         setSlidesData(response.slides_content);
//       }
      
//       if (response.assignment_content) {
//         setAssignmentData(response.assignment_content);
//       }
      
//       setDownloadUrls({
//         pdf: response.pdf_notes_url,
//         ppt: response.ppt_url,
//         assignment: response.assignment_url,
//         answers: response.answers_url
//       });
      
//       if (response.session_id) {
//         setSessionId(response.session_id);
//       }
//     } catch (error) {
//       console.error('Error:', error);
//       alert('Error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const tabs = [
//     { id: 'video', label: '🎬 Video', icon: '🎬' },
//     { id: 'notes', label: '📄 Notes', icon: '📄', disabled: !notesData },
//     { id: 'slides', label: '📊 Slides', icon: '📊', disabled: !slidesData },
//     { id: 'assignment', label: '📝 Assignment', icon: '📝', disabled: !assignmentData },
//   ];

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      
//       {/* Header */}
//       <header className="bg-white shadow-md">
//         <div className="container mx-auto px-4 py-4">
//           <div className="flex items-center justify-between">
//             <div className="flex items-center gap-3">
//               <span className="text-4xl">🎓</span>
//               <div>
//                 <h1 className="text-2xl font-bold text-gray-800">
//                   AI Study Portal
//                 </h1>
//                 <p className="text-sm text-gray-600">
//                   Learn • Practice • Excel
//                 </p>
//               </div>
//             </div>
            
//             {/* User Menu */}
//             <div className="flex items-center gap-3">
//               {isAuthenticated ? (
//                 <>
//                   <button
//                     onClick={() => navigate('/dashboard')}
//                     className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
//                   >
//                     📊 My Dashboard
//                   </button>
//                   <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg">
//                     <span className="text-2xl">👤</span>
//                     <span className="font-medium text-gray-700">{user?.username}</span>
//                   </div>
//                   <button
//                     onClick={logout}
//                     className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
//                   >
//                     Logout
//                   </button>
//                 </>
//               ) : (
//                 <>
//                   <button
//                     onClick={() => navigate('/login')}
//                     className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
//                   >
//                     Login
//                   </button>
//                   <button
//                     onClick={() => navigate('/signup')}
//                     className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium"
//                   >
//                     Sign Up
//                   </button>
//                 </>
//               )}
//             </div>
//           </div>
//         </div>
//       </header>

//       {/* Main Content */}
//       <div className="container mx-auto px-4 py-6">
        
//         {/* Info Banner for Guest Users */}
//         {!isAuthenticated && (
//           <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
//             <p className="text-yellow-800">
//               💡 <strong>Guest Mode:</strong> You can generate lessons, but they won't be saved. 
//               <button
//                 onClick={() => navigate('/login')}
//                 className="ml-2 text-blue-600 font-semibold hover:underline"
//               >
//                 Login
//               </button> or 
//               <button
//                 onClick={() => navigate('/signup')}
//                 className="ml-1 text-purple-600 font-semibold hover:underline"
//               >
//                 Sign up
//               </button> to save your lessons!
//             </p>
//           </div>
//         )}

//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
//           {/* Content Area */}
//           <div className="lg:col-span-2">
            
//             {/* Tabs */}
//             {(videoUrl || notesData || slidesData || assignmentData) && (
//               <div className="bg-white rounded-xl shadow-lg mb-6">
//                 <div className="flex border-b overflow-x-auto">
//                   {tabs.map(tab => (
//                     <button
//                       key={tab.id}
//                       onClick={() => !tab.disabled && setActiveTab(tab.id)}
//                       disabled={tab.disabled}
//                       className={`flex items-center gap-2 px-6 py-4 font-semibold transition-all whitespace-nowrap ${
//                         activeTab === tab.id
//                           ? 'text-blue-600 border-b-2 border-blue-600'
//                           : tab.disabled
//                           ? 'text-gray-400 cursor-not-allowed'
//                           : 'text-gray-600 hover:text-blue-600'
//                       }`}
//                     >
//                       <span className="text-xl">{tab.icon}</span>
//                       {tab.label}
//                     </button>
//                   ))}
//                 </div>
//               </div>
//             )}

//             {/* Tab Content */}
//             <div className="min-h-[600px]">
//               {activeTab === 'video' && (
//                 <VideoPlayer videoUrl={videoUrl} loading={loading} />
//               )}
              
//               {activeTab === 'notes' && notesData && (
//                 <NotesViewer 
//                   notesData={notesData}
//                   pdfUrl={downloadUrls.pdf}
//                 />
//               )}
              
//               {activeTab === 'slides' && slidesData && (
//                 <SlidesViewer 
//                   slidesData={slidesData}
//                   pptUrl={downloadUrls.ppt}
//                 />
//               )}
              
//               {activeTab === 'assignment' && assignmentData && (
//                 <AssignmentViewer 
//                   assignmentData={assignmentData}
//                   assignmentUrl={downloadUrls.assignment}
//                   answersUrl={downloadUrls.answers}
//                 />
//               )}
//             </div>
//           </div>

//           {/* Input Area */}
//           <div className="lg:col-span-1">
//             <QuestionInput
//               onAskQuestion={handleAskQuestion}
//               loading={loading}
//             />
//           </div>
//         </div>
//       </div>

//       {/* Loading Overlay */}
//       {loading && (
//         <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
//           <div className="bg-white rounded-2xl p-8 max-w-md mx-4 shadow-2xl">
//             <div className="text-center">
//               <div className="text-6xl mb-4 animate-bounce">🎓</div>
//               <h3 className="text-2xl font-bold text-gray-800 mb-2">
//                 Preparing Your Lesson
//               </h3>
//               <p className="text-gray-600 mb-6">
//                 Creating video, notes, slides & assignment...
//               </p>
              
//               <div className="space-y-3">
//                 <div className="flex items-center gap-3">
//                   <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
//                     <span className="text-green-600">✓</span>
//                   </div>
//                   <span className="text-gray-700">Analyzing content</span>
//                 </div>
                
//                 <div className="flex items-center gap-3 animate-pulse">
//                   <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
//                     <svg className="animate-spin h-4 w-4 text-blue-600" viewBox="0 0 24 24">
//                       <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
//                       <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
//                     </svg>
//                   </div>
//                   <span className="text-gray-700">Generating materials...</span>
//                 </div>
//               </div>
              
//               <p className="mt-6 text-sm text-gray-500">
//                 This may take 30-60 seconds
//               </p>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default HomePage;




import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';
import { useAuth } from '../context/AuthContext';
import VideoPlayer from '../components/VideoPlayer';
import QuestionInput from '../components/QuestionInput';
import NotesViewer from '../components/NotesViewer';
import SlidesViewer from '../components/SlidesViewer';
import AssignmentViewer from '../components/AssignmentViewer';
import { teachingAPI } from '../services/api';

function HomePage() {
  const [sessionId, setSessionId] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeSection, setActiveSection] = useState('hero');
  
  const [notesData, setNotesData] = useState(null);
  const [slidesData, setSlidesData] = useState(null);
  const [assignmentData, setAssignmentData] = useState(null);
  const [downloadUrls, setDownloadUrls] = useState({});
  const [activeTab, setActiveTab] = useState('video');
  
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    setSessionId(uuidv4());
  }, []);

  const handleAskQuestion = async (question, subject) => {
    setLoading(true);
    setActiveSection('content');
    setVideoUrl(null);
    setNotesData(null);
    setSlidesData(null);
    setAssignmentData(null);
    setActiveTab('video');

    try {
      const response = await teachingAPI.askQuestion(question, sessionId, subject);
      
      if (response.video_url) setVideoUrl(response.video_url);
      if (response.notes_content) setNotesData(response.notes_content);
      if (response.slides_content) setSlidesData(response.slides_content);
      if (response.assignment_content) setAssignmentData(response.assignment_content);
      
      setDownloadUrls({
        pdf: response.pdf_notes_url,
        ppt: response.ppt_url,
        assignment: response.assignment_url,
        answers: response.answers_url
      });
      
      if (response.session_id) setSessionId(response.session_id);
      
      // Smooth scroll to content
      setTimeout(() => {
        document.getElementById('content-section')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 500);
      
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating lesson. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ 
      behavior: 'smooth' 
    });
  };

  const features = [
    {
      icon: '🎬',
      title: 'AI Video Lessons',
      description: 'Watch professionally narrated video lessons with synchronized visuals, created instantly by AI.',
      gradient: 'from-red-500 to-pink-500'
    },
    {
      icon: '📄',
      title: 'Smart Notes',
      description: 'Get comprehensive, editable study notes in PDF format with key concepts and definitions.',
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      icon: '📊',
      title: 'PowerPoint Slides',
      description: 'Download professional presentation slides perfect for review and sharing.',
      gradient: 'from-orange-500 to-yellow-500'
    },
    {
      icon: '📝',
      title: 'Practice Tests',
      description: 'Test your knowledge with AI-generated quizzes and get instant feedback.',
      gradient: 'from-purple-500 to-indigo-500'
    }
  ];

  const stats = [
    { number: '10,000+', label: 'Lessons Created' },
    { number: '5,000+', label: 'Active Students' },
    { number: '50+', label: 'Subjects Covered' },
    { number: '98%', label: 'Satisfaction Rate' }
  ];

  const howItWorks = [
    {
      step: '1',
      title: 'Ask Your Question',
      description: 'Simply type any topic or question you want to learn about',
      icon: '❓'
    },
    {
      step: '2',
      title: 'AI Creates Content',
      description: 'Our advanced AI generates comprehensive learning materials',
      icon: '🤖'
    },
    {
      step: '3',
      title: 'Learn & Practice',
      description: 'Watch videos, read notes, and test your knowledge',
      icon: '📚'
    },
    {
      step: '4',
      title: 'Track Progress',
      description: 'Save lessons to your account and monitor your learning journey',
      icon: '📈'
    }
  ];

  const tabs = [
    { id: 'video', label: 'Video Lesson', icon: '🎬' },
    { id: 'notes', label: 'Notes', icon: '📄', disabled: !notesData },
    { id: 'slides', label: 'Slides', icon: '📊', disabled: !slidesData },
    { id: 'assignment', label: 'Practice', icon: '📝', disabled: !assignmentData },
  ];

  return (
    <div className="min-h-screen gradient-bg">
      
      {/* FIXED NAVIGATION */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass-card border-b">
        <div className="container-custom">
          <div className="flex items-center justify-between h-20">
            
            {/* Logo */}
            <div className="flex items-center gap-3 cursor-pointer" onClick={() => scrollToSection('hero')}>
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-2xl shadow-lg">
                🎓
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800">AI Study Portal</h1>
                <p className="text-xs text-gray-500">Learn Anything, Instantly</p>
              </div>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-6">
              <button onClick={() => scrollToSection('features')} className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Features
              </button>
              <button onClick={() => scrollToSection('how-it-works')} className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                How It Works
              </button>
              <button onClick={() => scrollToSection('try-it')} className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Try Now
              </button>
            </div>

            {/* User Menu */}
            <div className="flex items-center gap-3">
              {isAuthenticated ? (
                <>
                  <button onClick={() => navigate('/dashboard')} className="btn-secondary">
                    Dashboard
                  </button>
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold cursor-pointer">
                    {user?.username?.[0]?.toUpperCase()}
                  </div>
                </>
              ) : (
                <>
                  <button onClick={() => navigate('/login')} className="btn-secondary">
                    Login
                  </button>
                  <button onClick={() => navigate('/signup')} className="btn-primary">
                    Sign Up Free
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section id="hero" className="section pt-32 pb-20">
        <div className="container-custom text-center">
          
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full mb-6 animate-fadeIn">
            <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
            <span className="text-sm font-semibold">Powered by Advanced AI Technology</span>
          </div>

          {/* Main Headline */}
          <h1 className="heading-xl mb-6 animate-slideUp">
            Learn Anything with
            <span className="gradient-text block mt-2">AI-Powered Education</span>
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto animate-slideUp" style={{ animationDelay: '0.1s' }}>
            Get instant video lessons, interactive notes, presentations, and practice tests
            <br />
            <span className="font-semibold text-gray-800">All generated by AI in seconds</span>
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16 animate-slideUp" style={{ animationDelay: '0.2s' }}>
            <button 
              onClick={() => scrollToSection('try-it')}
              className="btn-primary w-full sm:w-auto"
            >
              🚀 Try It Free Now
            </button>
            <button 
              onClick={() => scrollToSection('how-it-works')}
              className="btn-outline w-full sm:w-auto"
            >
              📖 See How It Works
            </button>
          </div>

          {/* Hero Image/Animation */}
          <div className="relative max-w-5xl mx-auto animate-fadeIn" style={{ animationDelay: '0.3s' }}>
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl blur-3xl opacity-20 animate-float"></div>
            <div className="relative glass-card p-8 rounded-3xl">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {features.map((feature, idx) => (
                  <div key={idx} className="text-center p-4 bg-white/50 rounded-xl">
                    <div className="text-4xl mb-2">{feature.icon}</div>
                    <p className="text-sm font-semibold text-gray-700">{feature.title}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* STATS SECTION */}
      <section className="section py-12 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="container-custom">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center text-white">
            {stats.map((stat, idx) => (
              <div key={idx} className="animate-slideUp" style={{ animationDelay: `${idx * 0.1}s` }}>
                <div className="text-4xl md:text-5xl font-bold mb-2">{stat.number}</div>
                <div className="text-blue-100">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="section">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="heading-lg mb-4">
              Everything You Need to
              <span className="gradient-text"> Master Any Subject</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our AI creates comprehensive learning materials tailored to your needs
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, idx) => (
              <div key={idx} className="feature-card animate-slideUp" style={{ animationDelay: `${idx * 0.1}s` }}>
                <div className={`text-6xl mb-4 bg-gradient-to-r ${feature.gradient} bg-clip-text text-transparent`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-3 text-gray-800">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS SECTION */}
      <section id="how-it-works" className="section bg-white">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="heading-lg mb-4">
              How It <span className="gradient-text">Works</span>
            </h2>
            <p className="text-xl text-gray-600">Simple, fast, and effective learning in 4 steps</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {howItWorks.map((item, idx) => (
              <div key={idx} className="text-center animate-slideUp" style={{ animationDelay: `${idx * 0.1}s` }}>
                <div className="relative mb-6 inline-block">
                  <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-3xl font-bold shadow-xl">
                    {item.step}
                  </div>
                  <div className="absolute -bottom-2 -right-2 text-4xl">{item.icon}</div>
                </div>
                <h3 className="text-xl font-bold mb-3 text-gray-800">{item.title}</h3>
                <p className="text-gray-600">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* TRY IT NOW SECTION */}
      <section id="try-it" className="section">
        <div className="container-custom">
          <div className="text-center mb-12">
            <h2 className="heading-lg mb-4">
              Try It <span className="gradient-text">Right Now</span>
            </h2>
            <p className="text-xl text-gray-600">Ask any question and watch AI create your personalized lesson</p>
          </div>

          <div className="max-w-2xl mx-auto mb-12">
            <QuestionInput onAskQuestion={handleAskQuestion} loading={loading} />
          </div>

          {!isAuthenticated && (
            <div className="glass-card max-w-2xl mx-auto text-center p-6">
              <p className="text-gray-700 mb-4">
                💡 <strong>Sign up for free</strong> to save your lessons and track your progress!
              </p>
              <button onClick={() => navigate('/signup')} className="btn-primary">
                Create Free Account
              </button>
            </div>
          )}
        </div>
      </section>

      {/* CONTENT SECTION (Shows after generating) */}
      {(videoUrl || notesData || slidesData || assignmentData) && (
        <section id="content-section" className="section bg-white">
          <div className="container-custom">
            <h2 className="heading-md mb-8 text-center">Your <span className="gradient-text">Generated Lesson</span></h2>
            
            {/* Tabs */}
            <div className="glass-card rounded-2xl mb-6 overflow-hidden">
              <div className="flex overflow-x-auto">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => !tab.disabled && setActiveTab(tab.id)}
                    disabled={tab.disabled}
                    className={`
                      flex items-center gap-2 px-8 py-4 font-semibold transition-all whitespace-nowrap
                      ${activeTab === tab.id
                        ? 'bg-blue-600 text-white'
                        : tab.disabled
                        ? 'text-gray-400 cursor-not-allowed'
                        : 'text-gray-700 hover:bg-gray-50'
                      }
                    `}
                  >
                    <span className="text-2xl">{tab.icon}</span>
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="animate-fadeIn">
              {activeTab === 'video' && <VideoPlayer videoUrl={videoUrl} loading={loading} />}
              {activeTab === 'notes' && notesData && <NotesViewer notesData={notesData} pdfUrl={downloadUrls.pdf} />}
              {activeTab === 'slides' && slidesData && <SlidesViewer slidesData={slidesData} pptUrl={downloadUrls.ppt} />}
              {activeTab === 'assignment' && assignmentData && <AssignmentViewer assignmentData={assignmentData} assignmentUrl={downloadUrls.assignment} answersUrl={downloadUrls.answers} />}
            </div>
          </div>
        </section>
      )}

      {/* CTA SECTION */}
      <section className="section bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container-custom text-center">
          <h2 className="heading-lg mb-6">
            Ready to Transform Your Learning?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of students already learning with AI
          </p>
          <button onClick={() => navigate('/signup')} className="btn-secondary bg-white text-blue-600 hover:bg-gray-100">
            Get Started Free →
          </button>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container-custom text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-2xl">
              🎓
            </div>
            <span className="text-2xl font-bold">AI Study Portal</span>
          </div>
          <p className="text-gray-400 mb-4">
            Powered by Advanced AI • Built for Students
          </p>
          <p className="text-gray-500 text-sm">
            © 2024 AI Study Portal. All rights reserved.
          </p>
        </div>
      </footer>

      {/* LOADING OVERLAY */}
      {loading && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="glass-card p-10 rounded-3xl max-w-md text-center">
            <div className="text-6xl mb-4 animate-bounce">🎓</div>
            <h3 className="text-2xl font-bold mb-3 gradient-text">Creating Your Lesson</h3>
            <p className="text-gray-600 mb-6">AI is generating your personalized content...</p>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;