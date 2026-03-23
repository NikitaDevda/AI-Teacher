// import React, { useState, useEffect, useRef } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import TeacherAvatar from './components/TeacherAvatar';
// import ChatInterface from './components/ChatInterface';
// import DoubtInput from './components/DoubtInput';
// import { teachingAPI } from './services/api';

// function App() {
//   const [sessionId, setSessionId] = useState(null);
//   const [messages, setMessages] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [isSpeaking, setIsSpeaking] = useState(false);
//   const [currentVideoUrl, setCurrentVideoUrl] = useState(null);
//   const [currentAudio, setCurrentAudio] = useState(null);

//   const audioRef = useRef(null);

//   useEffect(() => {
//     // Initialize session
//     const newSessionId = uuidv4();
//     setSessionId(newSessionId);
//   }, []);

//   const playAudio = (audioUrl) => {
//     // Stop previous audio if playing
//     if (currentAudio) {
//       currentAudio.pause();
//       currentAudio.currentTime = 0;
//     }

//     const audio = new Audio(audioUrl);
//     audioRef.current = audio;
//     setCurrentAudio(audio);
//     setIsSpeaking(true);

//     audio.play();

//     audio.onended = () => {
//       setIsSpeaking(false);
//       setCurrentAudio(null);
//     };

//     audio.onerror = () => {
//       console.error('Audio playback error');
//       setIsSpeaking(false);
//       setCurrentAudio(null);
//     };
//   };

//   const handleAskQuestion = async (question, subject) => {
//     setLoading(true);

//     try {
//       const response = await teachingAPI.askQuestion(question, sessionId, subject);

//       // Update messages
//       setMessages(response.conversation_history);

//       // Play audio
//       if (response.audio_url) {
//         playAudio(response.audio_url);
//       }

//       // Set video if available
//       if (response.video_url) {
//         setCurrentVideoUrl(response.video_url);
//       }

//       // Update session ID if new
//       if (response.session_id && response.session_id !== sessionId) {
//         setSessionId(response.session_id);
//       }
//     } catch (error) {
//       console.error('Error asking question:', error);
//       alert('Error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleInterrupt = async (doubt) => {
//     // Stop current audio
//     if (currentAudio) {
//       currentAudio.pause();
//       currentAudio.currentTime = 0;
//       setIsSpeaking(false);
//     }

//     setLoading(true);

//     try {
//       const response = await teachingAPI.interruptWithDoubt(doubt, sessionId);

//       // Update messages (fetch full history)
//       const sessionData = await teachingAPI.getSession(sessionId);
//       setMessages(sessionData.history);

//       // Play audio response
//       if (response.audio_url) {
//         playAudio(response.audio_url);
//       }
//     } catch (error) {
//       console.error('Error interrupting:', error);
//       alert('Error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8 px-4">
//       <div className="container mx-auto">
//         {/* Header */}
//         <div className="text-center mb-8">
//           <h1 className="text-5xl font-bold text-gray-800 mb-2">
//             🎓 Live Teach AI
//           </h1>
//           <p className="text-gray-600 text-lg">
//             Your Personal AI Teacher - Ask anything, anytime!
//           </p>
//           {sessionId && (
//             <p className="text-xs text-gray-400 mt-2">
//               Session ID: {sessionId.slice(0, 8)}...
//             </p>
//           )}
//         </div>

//         {/* Teacher Avatar */}
//         <div className="mb-8">
//           <TeacherAvatar 
//             isSpeaking={isSpeaking} 
//             videoUrl={currentVideoUrl}
//           />
//         </div>

//         {/* Chat Interface */}
//         <div className="mb-6">
//           <ChatInterface messages={messages} />
//         </div>

//         {/* Input Section */}
//         <DoubtInput
//           onAskQuestion={handleAskQuestion}
//           onInterrupt={handleInterrupt}
//           isTeacherSpeaking={isSpeaking}
//           loading={loading}
//         />

//         {/* Status Indicator */}
//         {isSpeaking && (
//           <div className="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-full shadow-lg animate-pulse">
//             🎤 Teacher is speaking...
//           </div>
//         )}

//         {loading && (
//           <div className="fixed bottom-4 left-4 bg-blue-500 text-white px-6 py-3 rounded-full shadow-lg">
//             ⏳ Processing...
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default App;



// import React, { useState, useEffect, useRef } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import TeacherAvatar from './components/TeacherAvatar';
// import ChatInterface from './components/ChatInterface';
// import DoubtInput from './components/DoubtInput';
// import Whiteboard from './components/Whiteboard';  // ✅ NEW!
// import { teachingAPI } from './services/api';

// function App() {
//   const [sessionId, setSessionId] = useState(null);
//   const [messages, setMessages] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [isSpeaking, setIsSpeaking] = useState(false);
//   const [currentVideoUrl, setCurrentVideoUrl] = useState(null);
//   const [currentAudio, setCurrentAudio] = useState(null);
//   const [whiteboardContent, setWhiteboardContent] = useState('');  // ✅ NEW!

//   const audioRef = useRef(null);

//   useEffect(() => {
//     const newSessionId = uuidv4();
//     setSessionId(newSessionId);
//   }, []);

//   const playAudio = (audioUrl) => {
//     if (currentAudio) {
//       currentAudio.pause();
//       currentAudio.currentTime = 0;
//     }

//     const audio = new Audio(audioUrl);
//     audioRef.current = audio;
//     setCurrentAudio(audio);
//     setIsSpeaking(true);

//     audio.play();

//     audio.onended = () => {
//       setIsSpeaking(false);
//       setCurrentAudio(null);
//     };

//     audio.onerror = () => {
//       console.error('Audio playback error');
//       setIsSpeaking(false);
//       setCurrentAudio(null);
//     };
//   };

//   const handleAskQuestion = async (question, subject) => {
//     setLoading(true);

//     try {
//       const response = await teachingAPI.askQuestion(question, sessionId, subject);

//       setMessages(response.conversation_history);
//       setWhiteboardContent(response.whiteboard_content || '');  // ✅ NEW!

//       if (response.audio_url) {
//         playAudio(response.audio_url);
//       }

//       if (response.video_url) {
//         setCurrentVideoUrl(response.video_url);
//       }

//       if (response.session_id && response.session_id !== sessionId) {
//         setSessionId(response.session_id);
//       }
//     } catch (error) {
//       console.error('Error asking question:', error);
//       alert('Error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleInterrupt = async (doubt) => {
//     if (currentAudio) {
//       currentAudio.pause();
//       currentAudio.currentTime = 0;
//       setIsSpeaking(false);
//     }

//     setLoading(true);

//     try {
//       const response = await teachingAPI.interruptWithDoubt(doubt, sessionId);
//       const sessionData = await teachingAPI.getSession(sessionId);
//       setMessages(sessionData.history);

//       if (response.audio_url) {
//         playAudio(response.audio_url);
//       }
//     } catch (error) {
//       console.error('Error interrupting:', error);
//       alert('Error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-6 px-4">
//       <div className="container mx-auto max-w-7xl">
        
//         {/* Header */}
//         <div className="text-center mb-6">
//           <h1 className="text-4xl font-bold text-gray-800 mb-2">
//             🎓 AI Classroom
//           </h1>
//           <p className="text-gray-600">
//             Learn with AI Teacher & Interactive Whiteboard
//           </p>
//         </div>

//         {/* ✅ CLASSROOM LAYOUT: Split Screen */}
//         <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          
//           {/* LEFT SIDE: Teacher Video */}
//           <div className="space-y-4">
//             <TeacherAvatar 
//               isSpeaking={isSpeaking} 
//               videoUrl={currentVideoUrl}
//             />
//             <ChatInterface messages={messages} />
//           </div>

//           {/* RIGHT SIDE: Whiteboard */}
//           <div>
//             <Whiteboard content={whiteboardContent} />
//           </div>

//         </div>

//         {/* Input Section */}
//         <DoubtInput
//           onAskQuestion={handleAskQuestion}
//           onInterrupt={handleInterrupt}
//           isTeacherSpeaking={isSpeaking}
//           loading={loading}
//         />

//         {/* Status Indicators */}
//         {isSpeaking && (
//           <div className="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-full shadow-lg animate-pulse">
//             🎤 Teacher is speaking...
//           </div>
//         )}

//         {loading && (
//           <div className="fixed bottom-4 left-4 bg-blue-500 text-white px-6 py-3 rounded-full shadow-lg">
//             ⏳ Processing...
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default App;











// import React, { useState, useEffect, useRef } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import Whiteboard from './components/Whiteboard';
// import TeacherVideo from './components/TeacherVideo';
// import QuestionInput from './components/QuestionInput';
// import { teachingAPI } from './services/api';
// import { parseTeachingContent } from './utils/contentParser';

// function App() {
//   const [sessionId, setSessionId] = useState(null);
//   const [sections, setSections] = useState([]);
//   const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
//   const [loading, setLoading] = useState(false);
//   const [isSpeaking, setIsSpeaking] = useState(false);
//   const [currentVideoUrl, setCurrentVideoUrl] = useState(null);
//   const [currentAudio, setCurrentAudio] = useState(null);

//   const audioRef = useRef(null);
//   const sectionTimerRef = useRef(null);

//   useEffect(() => {
//     const newSessionId = uuidv4();
//     setSessionId(newSessionId);
//   }, []);

//   const playAudio = (audioUrl) => {
//     // Stop previous
//     if (currentAudio) {
//       currentAudio.pause();
//       currentAudio.currentTime = 0;
//     }

//     if (sectionTimerRef.current) {
//       clearInterval(sectionTimerRef.current);
//     }

//     const audio = new Audio(audioUrl);
//     audioRef.current = audio;
//     setCurrentAudio(audio);
//     setIsSpeaking(true);
//     setCurrentSectionIndex(0);

//     audio.play();

//     audio.onended = () => {
//       setIsSpeaking(false);
//       setCurrentAudio(null);
//       if (sectionTimerRef.current) {
//         clearInterval(sectionTimerRef.current);
//       }
//       // Show all sections at end
//       setCurrentSectionIndex(sections.length - 1);
//     };

//     audio.onerror = () => {
//       console.error('Audio error');
//       setIsSpeaking(false);
//       setCurrentAudio(null);
//       if (sectionTimerRef.current) {
//         clearInterval(sectionTimerRef.current);
//       }
//     };
//   };

//   const startSectionReveal = (totalSections, audioDuration) => {
//     if (totalSections === 0) return;

//     // Show sections progressively during audio
//     const intervalTime = (audioDuration / totalSections) * 1000;
//     let index = 0;

//     sectionTimerRef.current = setInterval(() => {
//       index++;
//       if (index < totalSections) {
//         setCurrentSectionIndex(index);
//       } else {
//         clearInterval(sectionTimerRef.current);
//       }
//     }, intervalTime);
//   };

//   const handleAskQuestion = async (question, subject) => {
//     setLoading(true);
//     setSections([]);
//     setCurrentSectionIndex(0);

//     try {
//       const response = await teachingAPI.askQuestion(question, sessionId, subject);

//       console.log('AI Response:', response.answer);

//       // Parse into structured sections
//       const parsedSections = parseTeachingContent(response.answer);
//       console.log('Parsed Sections:', parsedSections);
      
//       setSections(parsedSections);

//       // Play audio
//       if (response.audio_url) {
//         playAudio(response.audio_url);
        
//         // Start revealing sections during audio
//         // Estimate: ~10 seconds per section
//         const estimatedDuration = parsedSections.length * 10;
//         startSectionReveal(parsedSections.length, estimatedDuration);
//       } else {
//         // No audio - show all immediately
//         setCurrentSectionIndex(parsedSections.length - 1);
//       }

//       // Video
//       if (response.video_url) {
//         setCurrentVideoUrl(response.video_url);
//       }

//       // Session
//       if (response.session_id && response.session_id !== sessionId) {
//         setSessionId(response.session_id);
//       }
//     } catch (error) {
//       console.error('Error:', error);
//       alert('Error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

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
//                   AI Classroom
//                 </h1>
//                 <p className="text-sm text-gray-600">
//                   Structured Learning with Smart Whiteboard
//                 </p>
//               </div>
//             </div>
//           </div>
//         </div>
//       </header>

//       {/* Main Content */}
//       <div className="container mx-auto px-4 py-6">
//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
//           {/* Whiteboard */}
//           <div className="lg:col-span-2">
//             <div className="h-[600px]">
//               <Whiteboard 
//                 sections={sections}
//                 currentSectionIndex={currentSectionIndex}
//                 isTeaching={isSpeaking}
//               />
//             </div>
//           </div>

//           {/* Input */}
//           <div className="lg:col-span-1">
//             <QuestionInput
//               onAskQuestion={handleAskQuestion}
//               loading={loading}
//               isTeaching={isSpeaking}
//             />
//           </div>
//         </div>
//       </div>

//       {/* Teacher Video */}
//       <TeacherVideo 
//         videoUrl={currentVideoUrl}
//         isSpeaking={isSpeaking}
//       />

//       {/* Loading */}
//       {loading && (
//         <div className="fixed bottom-4 left-4 bg-blue-600 text-white px-6 py-3 rounded-full shadow-lg flex items-center gap-2">
//           <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
//             <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
//             <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
//           </svg>
//           <span>Preparing...</span>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

















// import React, { useState, useEffect } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import VideoPlayer from './components/VideoPlayer';
// import QuestionInput from './components/QuestionInput';
// import { teachingAPI } from './services/api';

// function App() {
//   const [sessionId, setSessionId] = useState(null);
//   const [videoUrl, setVideoUrl] = useState(null);
//   const [loading, setLoading] = useState(false);

//   useEffect(() => {
//     const newSessionId = uuidv4();
//     setSessionId(newSessionId);
//   }, []);

//   const handleAskQuestion = async (question, subject) => {
//     setLoading(true);
//     setVideoUrl(null);

//     try {
//       console.log('📤 Asking question:', question);
      
//       const response = await teachingAPI.askQuestion(question, sessionId, subject);
      
//       console.log('📥 Response received:', response);

//       // Set video URL
//       if (response.video_url) {
//         console.log('🎬 Video URL:', response.video_url);
//         setVideoUrl(response.video_url);
//       } else {
//         console.warn('⚠️ No video URL in response');
//         alert('Video generation failed. Please try again.');
//       }

//       // Update session
//       if (response.session_id && response.session_id !== sessionId) {
//         setSessionId(response.session_id);
//       }
//     } catch (error) {
//       console.error('❌ Error:', error);
//       alert('Error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
//       {/* Header */}
//       <header className="bg-white shadow-md">
//         <div className="container mx-auto px-4 py-4">
//           <div className="flex items-center justify-between">
//             <div className="flex items-center gap-3">
//               <span className="text-4xl">🎬</span>
//               <div>
//                 <h1 className="text-2xl font-bold text-gray-800">
//                   AI Video Teacher
//                 </h1>
//                 <p className="text-sm text-gray-600">
//                   YouTube-style AI Generated Lessons
//                 </p>
//               </div>
//             </div>
//             {loading && (
//               <div className="flex items-center gap-2 text-blue-600">
//                 <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
//                   <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
//                   <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
//                 </svg>
//                 <span className="font-medium">Generating...</span>
//               </div>
//             )}
//           </div>
//         </div>
//       </header>

//       {/* Main Content */}
//       <div className="container mx-auto px-4 py-6">
//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
//           {/* Video Player - Large */}
//           <div className="lg:col-span-2">
//             <div className="h-[600px] relative">
//               <VideoPlayer 
//                 videoUrl={videoUrl}
//                 loading={loading}
//               />
//             </div>
//           </div>

//           {/* Question Input */}
//           <div className="lg:col-span-1">
//             <QuestionInput
//               onAskQuestion={handleAskQuestion}
//               loading={loading}
//             />
            
//             {/* Info Card */}
//             <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
//               <h3 className="text-lg font-bold text-gray-800 mb-3">
//                 ℹ️ How it works
//               </h3>
//               <ul className="space-y-2 text-sm text-gray-600">
//                 <li className="flex items-start gap-2">
//                   <span className="text-green-500 mt-1">✓</span>
//                   <span>Ask any question</span>
//                 </li>
//                 <li className="flex items-start gap-2">
//                   <span className="text-green-500 mt-1">✓</span>
//                   <span>AI generates personalized video</span>
//                 </li>
//                 <li className="flex items-start gap-2">
//                   <span className="text-green-500 mt-1">✓</span>
//                   <span>Watch YouTube-style lesson</span>
//                 </li>
//                 <li className="flex items-start gap-2">
//                   <span className="text-blue-500 mt-1">⏱️</span>
//                   <span>Video generation takes 30-60 seconds</span>
//                 </li>
//               </ul>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Loading Overlay */}
//       {loading && (
//         <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
//           <div className="bg-white rounded-2xl p-8 max-w-md mx-4 shadow-2xl">
//             <div className="text-center">
//               <div className="text-6xl mb-4">🎬</div>
//               <h3 className="text-2xl font-bold text-gray-800 mb-2">
//                 Creating Your Video
//               </h3>
//               <p className="text-gray-600 mb-6">
//                 Generating personalized educational video...
//               </p>
              
//               <div className="space-y-3">
//                 <div className="flex items-center gap-3 text-left">
//                   <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
//                     <span className="text-green-600">✓</span>
//                   </div>
//                   <span className="text-gray-700">AI analyzing content</span>
//                 </div>
                
//                 <div className="flex items-center gap-3 text-left">
//                   <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
//                     <span className="text-green-600">✓</span>
//                   </div>
//                   <span className="text-gray-700">Generating audio</span>
//                 </div>
                
//                 <div className="flex items-center gap-3 text-left animate-pulse">
//                   <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
//                     <svg className="animate-spin h-4 w-4 text-blue-600" viewBox="0 0 24 24">
//                       <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
//                       <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
//                     </svg>
//                   </div>
//                   <span className="text-gray-700">Rendering video frames...</span>
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

// export default App;
















// import React, { useState, useEffect } from 'react';
// import { v4 as uuidv4 } from 'uuid';
// import VideoPlayer from './components/VideoPlayer';
// import QuestionInput from './components/QuestionInput';
// import NotesViewer from './components/NotesViewer';
// import SlidesViewer from './components/SlidesViewer';
// import AssignmentViewer from './components/AssignmentViewer';
// import { teachingAPI } from './services/api';

// function App() {
//   const [sessionId, setSessionId] = useState(null);
//   const [videoUrl, setVideoUrl] = useState(null);
//   const [loading, setLoading] = useState(false);
  
//   // Study materials
//   const [notesData, setNotesData] = useState(null);
//   const [slidesData, setSlidesData] = useState(null);
//   const [assignmentData, setAssignmentData] = useState(null);
//   const [downloadUrls, setDownloadUrls] = useState({});
  
//   // Active tab
//   const [activeTab, setActiveTab] = useState('video');

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
      
//       // Video
//       if (response.video_url) {
//         setVideoUrl(response.video_url);
//       }
      
//       // Study materials
//       if (response.notes_content) {
//         setNotesData(response.notes_content);
//       }
      
//       if (response.slides_content) {
//         setSlidesData(response.slides_content);
//       }
      
//       if (response.assignment_content) {
//         setAssignmentData(response.assignment_content);
//       }
      
//       // Download URLs
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
//             {loading && (
//               <div className="flex items-center gap-2 text-blue-600">
//                 <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
//                   <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
//                   <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
//                 </svg>
//                 <span className="font-medium">Generating...</span>
//               </div>
//             )}
//           </div>
//         </div>
//       </header>

//       {/* Main Content */}
//       <div className="container mx-auto px-4 py-6">
//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
//           {/* Content Area - 2 columns */}
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

//           {/* Input Area - 1 column */}
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

// export default App;














import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import HomePage from './pages/HomePage';

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-spin">⏳</div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;