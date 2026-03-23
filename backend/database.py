from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL (SQLite - creates file in backend folder)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./ai_teacher.db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ========================================
# DATABASE MODELS
# ========================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)  # Set to True for development
    verification_token = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    lessons = relationship("Lesson", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    bio = Column(Text)
    avatar_url = Column(String(500))
    phone = Column(String(20))
    grade = Column(String(50))
    subjects_interested = Column(Text)
    
    total_lessons = Column(Integer, default=0)
    total_study_time = Column(Integer, default=0)
    
    user = relationship("User", back_populates="profile")


class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    question = Column(Text, nullable=False)
    subject = Column(String(100))
    answer = Column(Text)
    
    # File URLs
    video_url = Column(String(500))
    audio_url = Column(String(500))
    pdf_url = Column(String(500))
    ppt_url = Column(String(500))
    assignment_url = Column(String(500))
    answers_url = Column(String(500))
    
    # Metadata
    video_duration = Column(Integer)
    completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="lessons")


class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    
    answers = Column(Text)
    score = Column(Integer)
    total = Column(Integer)
    
    submitted_at = Column(DateTime, default=datetime.utcnow)


# ========================================
# INITIALIZE DATABASE
# ========================================

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")
    print(f"📂 Database file: {SQLALCHEMY_DATABASE_URL}")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()