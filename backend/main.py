

from datetime import datetime
import os
import uuid
import tempfile
import time
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# Import models
from models import QuestionRequest, SessionResponse, Message

# Import services
from services.ai_service import ai_service
from services.content_parser import content_parser
from services.synced_video_service import synced_video_service
from services.graph_generator import graph_generator
from services.fast_image_service import fast_image_service
from services.pdf_generator import pdf_generator
from services.ppt_generator import ppt_generator
from services.assignment_generator import assignment_generator
from services.session_service import session_manager

# Database and auth
from database import get_db, init_db, User, Lesson, UserProfile
from services.auth_service import auth_service
from services.email_service import email_service

from dotenv import load_dotenv
load_dotenv()

# ========================================
# FASTAPI APP
# ========================================

app = FastAPI(
    title="AI Study Portal - Complete System",
    description="AI-powered educational platform with video lessons, notes, slides, and assignments",
    version="3.0.0"
)

# ========================================
# CORS MIDDLEWARE
# ========================================
# ========================================
# CORS MIDDLEWARE
# ========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    "https://ai-teacher-84vo.vercel.app",
    allow_credentials=False,    # ← यह करो
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://localhost:5173",
#         "http://127.0.0.1:3000",
#         "http://127.0.0.1:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
    
# )

# ========================================
# CREATE DIRECTORIES
# ========================================

TEMP_DIRS = [
    "temp/videos",
    "temp/audio",
    "temp/notes",
    "temp/presentations",
    "temp/assignments",
    "temp/graphs",
    "temp/images"
]

for dir_path in TEMP_DIRS:
    os.makedirs(dir_path, exist_ok=True)

# ========================================
# STATIC FILE MOUNTS
# ========================================

app.mount("/temp/videos", StaticFiles(directory="temp/videos"), name="videos")
app.mount("/temp/audio", StaticFiles(directory="temp/audio"), name="audio")
app.mount("/temp/notes", StaticFiles(directory="temp/notes"), name="notes")
app.mount("/temp/presentations", StaticFiles(directory="temp/presentations"), name="presentations")
app.mount("/temp/assignments", StaticFiles(directory="temp/assignments"), name="assignments")
app.mount("/temp/graphs", StaticFiles(directory="temp/graphs"), name="graphs")
app.mount("/temp/images", StaticFiles(directory="temp/images"), name="images")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

# ========================================
# STARTUP EVENT
# ========================================

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    init_db()
    print("\n" + "="*60)
    print("🚀 AI STUDY PORTAL - SYSTEM STARTING")
    print("="*60)
    print("✅ Database initialized")
    print("✅ All services ready")
    print("✅ Static files mounted")
    print("="*60)
    print("🌐 Server running on: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("="*60 + "\n")

# ========================================
# SECURITY
# ========================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)

# ========================================
# PYDANTIC MODELS
# ========================================

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

# ========================================
# DEPENDENCY FUNCTIONS
# ========================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current authenticated user (required)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    payload = auth_service.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = auth_service.get_user_by_id(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if token provided, else None (for guest access)"""
    if not token:
        return None
    
    try:
        payload = auth_service.verify_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                return auth_service.get_user_by_id(db, int(user_id))
    except:
        pass
    
    return None

# ========================================
# BASIC ENDPOINTS
# ========================================

@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "message": "AI Study Portal - Complete Educational Platform ✅",
        "version": "3.0.0",
        "status": "running",
        "features": [
            "🎬 AI-Generated Video Lessons (Audio Synced)",
            "📊 Auto-Generated Graphs & Visualizations",
            "📝 Worked Examples & Derivations",
            "📄 PDF Study Notes",
            "📊 PowerPoint Presentations",
            "✍️ Practice Assignments with Answer Keys",
            "👤 User Authentication & Profiles",
            "💾 Lesson History & Dashboard",
            "🎯 Subject-Specific Content"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "ask": "/api/ask",
            "login": "/api/auth/login",
            "register": "/api/auth/register",
            "dashboard": "/api/user/lessons"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "✅ Running",
            "ai_service": "✅ Running",
            "video_generation": "✅ Running (Synced)",
            "graph_generation": "✅ Running",
            "pdf_generation": "✅ Running",
            "ppt_generation": "✅ Running",
            "assignment_generation": "✅ Running"
        },
        "temp_dirs": {
            dir_path: "✅ Ready" if os.path.exists(dir_path) else "❌ Missing"
            for dir_path in TEMP_DIRS
        }
    }

# ========================================
# AUTHENTICATION ENDPOINTS
# ========================================

@app.post("/api/auth/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register new user
    
    Creates user account and sends verification email
    """
    try:
        # Create user
        user, verification_token = auth_service.create_user(
            db=db,
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name
        )
        
        # Send verification email (prints to console in development)
        email_service.send_verification_email(
            user_data.email,
            verification_token,
            user_data.username
        )
        
        return {
            "success": True,
            "message": "Registration successful! Check your email for verification link (or terminal in development).",
            "user_id": user.id,
            "username": user.username
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed. Please try again.")


@app.post("/api/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user
    
    Returns JWT access token for authenticated requests
    """
    # Authenticate user
    user = auth_service.authenticate_user(db, user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_verified": user.is_verified
        }
    }


@app.get("/api/auth/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify email with token from verification link"""
    success = auth_service.verify_email(db, token)
    
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    
    return {
        "success": True,
        "message": "Email verified successfully! You can now login."
    }


@app.get("/api/auth/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile and statistics"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at.isoformat(),
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
        "profile": {
            "total_lessons": profile.total_lessons if profile else 0,
            "total_study_time": profile.total_study_time if profile else 0,
            "grade": profile.grade if profile else None,
            "subjects_interested": profile.subjects_interested if profile else None
        }
    }

# ========================================
# MAIN LESSON GENERATION ENDPOINT
# ========================================

@app.post("/api/ask", response_model=SessionResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Generate complete educational lesson
    
    Features:
    - AI-generated explanations with examples and derivations
    - Audio narration
    - Video with synchronized audio
    - Auto-generated graphs for math topics
    - PDF notes
    - PowerPoint slides
    - Practice assignments with answer keys
    
    Works for both logged-in users (saves to account) and guests (temporary)
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Log request
        print(f"\n{'='*60}")
        if current_user:
            print(f"👤 User: {current_user.username} ({current_user.email})")
        else:
            print(f"👤 Guest User (not logged in)")
        print(f"📝 Question: {request.question}")
        print(f"📚 Subject: {request.subject}")
        print(f"🔑 Session ID: {session_id}")
        print(f"{'='*60}\n")
        
        # ========================================
        # 1. GENERATE AI ANSWER
        # ========================================
        print("🤖 Step 1/7: Generating AI answer...")
        answer = ai_service.generate_answer(request.question, request.subject)
        print(f"✅ AI answer generated ({len(answer)} characters)")
        
        # ========================================
        # 2. PARSE CONTENT
        # ========================================
        print("📝 Step 2/7: Parsing content structure...")
        parsed_content = content_parser.parse_content(answer)
        
        # Prepare content data for generators
        content_data = parsed_content[0] if parsed_content else {
            'heading': request.question,
            'definition': answer[:200] if len(answer) > 200 else answer,
            'points': []
        }
        print(f"✅ Content parsed: {content_data.get('heading', 'Untitled')}")
        
        # ========================================
        # 3. GENERATE AUDIO
        # ========================================
        print("🎵 Step 3/7: Generating audio narration...")
        audio_filename = f"audio_{int(time.time())}_{session_id[:8]}.mp3"
        audio_path = f"temp/audio/{audio_filename}"
        
        ai_service.text_to_speech(answer, audio_path)
        audio_url = f"http://localhost:8000/temp/audio/{audio_filename}"
        print(f"✅ Audio generated: {audio_filename}")
        
        # ========================================
        # 4. GENERATE VIDEO (SYNCED WITH AUDIO)
        # ========================================
        print("🎬 Step 4/7: Generating video (synced with audio, graphs included)...")
        video_filename = f"lesson_{int(time.time())}_{session_id[:8]}.mp4"
        video_path = f"temp/videos/{video_filename}"
        
        synced_video_service.create_synced_video(
            parsed_content=parsed_content,
            audio_path=audio_path,
            output_path=video_path,
            topic=request.question,
            answer_text=answer  # For graph detection
        )
        
        video_url = f"http://localhost:8000/temp/videos/{video_filename}"
        print(f"✅ Video generated (synced): {video_filename}")
        
        # ========================================
        # 5. GENERATE PDF NOTES
        # ========================================
        print("📄 Step 5/7: Generating PDF notes...")
        pdf_filename = f"notes_{int(time.time())}_{session_id[:8]}.pdf"
        
        try:
            pdf_path = pdf_generator.generate_notes(content_data, pdf_filename)
            pdf_notes_url = f"http://localhost:8000/temp/notes/{pdf_filename}" if pdf_path else None
            print(f"✅ PDF generated: {pdf_filename}")
        except Exception as e:
            print(f"⚠️ PDF generation failed: {e}")
            pdf_notes_url = None
        
        # ========================================
        # 6. GENERATE POWERPOINT SLIDES
        # ========================================
        print("📊 Step 6/7: Generating PowerPoint presentation...")
        ppt_filename = f"slides_{int(time.time())}_{session_id[:8]}.pptx"
        
        try:
            ppt_path = ppt_generator.generate_presentation(content_data, ppt_filename)
            ppt_url = f"http://localhost:8000/temp/presentations/{ppt_filename}" if ppt_path else None
            print(f"✅ PPT generated: {ppt_filename}")
        except Exception as e:
            print(f"⚠️ PPT generation failed: {e}")
            ppt_url = None
        
        # ========================================
        # 7. GENERATE ASSIGNMENT
        # ========================================
        print("📝 Step 7/7: Generating practice assignment...")
        topic = content_data.get('heading', request.question)
        
        try:
            q_path, a_path = assignment_generator.generate_assignment(topic)
            
            assignment_url = None
            answers_url = None
            
            if q_path and os.path.exists(q_path):
                assignment_url = f"http://localhost:8000/temp/assignments/{os.path.basename(q_path)}"
            
            if a_path and os.path.exists(a_path):
                answers_url = f"http://localhost:8000/temp/assignments/{os.path.basename(a_path)}"
            
            # Get assignment data for web display
            assignment_data = assignment_generator._generate_questions_ai(topic, 'medium')
            print(f"✅ Assignment generated")
            
        except Exception as e:
            print(f"⚠️ Assignment generation failed: {e}")
            assignment_url = None
            answers_url = None
            assignment_data = {
                'questions': [
                    {
                        'question': f'What is the main concept of {topic}?',
                        'options': [],
                        'answer': 'Review the lesson materials',
                        'explanation': 'Check the notes and video for details'
                    }
                ]
            }
        
        # ========================================
        # 8. PREPARE WEB CONTENT
        # ========================================
        print("🌐 Preparing web-friendly content...")
        
        # Notes content for web viewer
        notes_content = {
            'heading': content_data.get('heading', 'Lesson Notes'),
            'definition': content_data.get('definition', ''),
            'points': content_data.get('points', [])[:15],  # First 15 points
            'generated_at': datetime.now().isoformat()
        }
        
        # Slides content for carousel viewer
        slides_content = []
        
        # Title slide
        slides_content.append({
            'type': 'title',
            'content': content_data.get('heading', 'Lesson')
        })
        
        # Definition slide
        if content_data.get('definition'):
            slides_content.append({
                'type': 'definition',
                'title': 'Definition',
                'content': content_data.get('definition', '')
            })
        
        # Points slides (2 points per slide)
        points = content_data.get('points', [])
        for i in range(0, min(len(points), 12), 2):  # Max 6 slides of points
            slide_points = []
            
            if i < len(points):
                slide_points.append(points[i].get('text', ''))
            if i + 1 < len(points):
                slide_points.append(points[i + 1].get('text', ''))
            
            if slide_points:
                slides_content.append({
                    'type': 'points',
                    'title': content_data.get('heading', 'Key Points'),
                    'points': slide_points
                })
        
        print(f"✅ Web content prepared ({len(slides_content)} slides)")
        
        # ========================================
        # 9. SAVE TO DATABASE (IF LOGGED IN)
        # ========================================
        if current_user:
            try:
                print(f"💾 Saving lesson to {current_user.username}'s account...")
                
                lesson = Lesson(
                    user_id=current_user.id,
                    question=request.question,
                    subject=request.subject,
                    answer=answer,
                    video_url=video_url,
                    audio_url=audio_url,
                    pdf_url=pdf_notes_url,
                    ppt_url=ppt_url,
                    assignment_url=assignment_url,
                    answers_url=answers_url,
                    completed=False
                )
                
                db.add(lesson)
                
                # Update user profile statistics
                profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
                if profile:
                    profile.total_lessons += 1
                
                db.commit()
                db.refresh(lesson)
                
                print(f"✅ Lesson saved to database (ID: {lesson.id})")
                
            except Exception as e:
                print(f"⚠️ Database save failed: {e}")
                db.rollback()
        else:
            print("ℹ️ Guest user - lesson generated but NOT saved to account")
            print("💡 Create account to save your lessons!")
        
        # ========================================
        # 10. PREPARE RESPONSE
        # ========================================
        print(f"\n{'='*60}")
        print("✅ ALL MATERIALS GENERATED SUCCESSFULLY!")
        print(f"{'='*60}")
        print(f"📹 Video: {video_url}")
        print(f"🎵 Audio: {audio_url}")
        print(f"📄 PDF: {pdf_notes_url}")
        print(f"📊 PPT: {ppt_url}")
        print(f"📝 Assignment: {assignment_url}")
        print(f"✅ Answers: {answers_url}")
        print(f"{'='*60}\n")
        
        return SessionResponse(
            session_id=session_id,
            answer=answer,
            audio_url=audio_url,
            video_url=video_url,
            pdf_notes_url=pdf_notes_url,
            ppt_url=ppt_url,
            assignment_url=assignment_url,
            answers_url=answers_url,
            notes_content=notes_content,
            slides_content=slides_content,
            assignment_content=assignment_data,
            whiteboard_content=None,
            conversation_history=[]
        )
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERROR OCCURRED")
        print(f"{'='*60}")
        print(f"Error: {str(e)}")
        print(f"{'='*60}\n")
        
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Lesson generation failed: {str(e)}"
        )

# ========================================
# USER DASHBOARD ENDPOINTS
# ========================================

@app.get("/api/user/lessons")
async def get_user_lessons(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """
    Get user's lesson history
    
    Returns paginated list of lessons with metadata
    """
    # Get total count
    total = db.query(Lesson).filter(Lesson.user_id == current_user.id).count()
    
    # Get lessons with pagination
    lessons = db.query(Lesson).filter(
        Lesson.user_id == current_user.id
    ).order_by(
        Lesson.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "lessons": [
            {
                "id": lesson.id,
                "question": lesson.question,
                "subject": lesson.subject,
                "created_at": lesson.created_at.isoformat(),
                "video_url": lesson.video_url,
                "audio_url": lesson.audio_url,
                "pdf_url": lesson.pdf_url,
                "ppt_url": lesson.ppt_url,
                "assignment_url": lesson.assignment_url,
                "answers_url": lesson.answers_url,
                "completed": lesson.completed
            }
            for lesson in lessons
        ]
    }


@app.get("/api/user/lessons/{lesson_id}")
async def get_lesson_detail(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific lesson with full details"""
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.user_id == current_user.id
    ).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return {
        "id": lesson.id,
        "question": lesson.question,
        "subject": lesson.subject,
        "answer": lesson.answer,
        "video_url": lesson.video_url,
        "audio_url": lesson.audio_url,
        "pdf_url": lesson.pdf_url,
        "ppt_url": lesson.ppt_url,
        "assignment_url": lesson.assignment_url,
        "answers_url": lesson.answers_url,
        "created_at": lesson.created_at.isoformat(),
        "updated_at": lesson.updated_at.isoformat() if lesson.updated_at else None,
        "completed": lesson.completed
    }


@app.delete("/api/user/lessons/{lesson_id}")
async def delete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a lesson from user's history"""
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.user_id == current_user.id
    ).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Delete lesson
    db.delete(lesson)
    
    # Update user profile stats
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile and profile.total_lessons > 0:
        profile.total_lessons -= 1
    
    db.commit()
    
    return {
        "success": True,
        "message": "Lesson deleted successfully"
    }


@app.get("/api/user/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics and learning analytics"""
    # Total lessons
    total_lessons = db.query(Lesson).filter(Lesson.user_id == current_user.id).count()
    
    # Distinct subjects
    subjects = db.query(Lesson.subject).filter(
        Lesson.user_id == current_user.id
    ).distinct().all()
    
    # Last lesson
    last_lesson = db.query(Lesson).filter(
        Lesson.user_id == current_user.id
    ).order_by(Lesson.created_at.desc()).first()
    
    # Completed lessons
    completed_lessons = db.query(Lesson).filter(
        Lesson.user_id == current_user.id,
        Lesson.completed == True
    ).count()
    
    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "subjects_studied": len(subjects),
        "subjects": [s[0] for s in subjects if s[0]],
        "member_since": current_user.created_at.isoformat(),
        "last_lesson": last_lesson.created_at.isoformat() if last_lesson else None,
        "completion_rate": round((completed_lessons / total_lessons * 100), 2) if total_lessons > 0 else 0
    }


@app.patch("/api/user/lessons/{lesson_id}/complete")
async def mark_lesson_complete(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark lesson as completed"""
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.user_id == current_user.id
    ).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson.completed = True
    db.commit()
    
    return {
        "success": True,
        "message": "Lesson marked as complete"
    }

# ========================================
# ADDITIONAL ENDPOINTS
# ========================================

@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio to text
    
    Useful for voice-based question input
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Transcribe
        text = ai_service.speech_to_text(temp_path, language="en")
        
        # Clean up
        os.unlink(temp_path)
        
        return {
            "success": True,
            "text": text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@app.post("/api/interrupt")
async def interrupt_with_doubt(request: QuestionRequest):
    """
    Handle student interruption/doubt during lesson
    
    Maintains conversation context
    """
    try:
        session_id = request.session_id
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID required")
        
        # Add to session history
        interrupt_message = f"[STUDENT DOUBT] {request.question}"
        session_manager.add_message(session_id, "user", interrupt_message)
        
        # Get context
        context = session_manager.get_context_messages(session_id)
        
        # Generate response
        answer = ai_service.get_teaching_response(
            question=interrupt_message,
            conversation_history=context,
            subject=request.subject
        )
        
        session_manager.add_message(session_id, "assistant", answer)
        
        # Generate audio
        audio_file = f"temp/audio/interrupt_{session_id}_{int(time.time())}.mp3"
        ai_service.text_to_speech(answer, audio_file)
        
        return {
            "success": True,
            "answer": answer,
            "audio_url": f"http://localhost:8000/{audio_file}",
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get conversation history for a session"""
    history = session_manager.get_history(session_id)
    
    return {
        "session_id": session_id,
        "message_count": len(history),
        "history": history
    }

# ========================================
# RUN SERVER
# ========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
# # uvicorn main:app --reload
