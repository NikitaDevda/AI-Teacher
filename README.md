# AI-Powered Learning Platform
An intelligent educational platform that generates personalized video lessons, study notes, presentations, and practice assignments using AI technology.


## Overview

AI Study Portal is a full-stack educational platform that leverages artificial intelligence to create complete learning materials in seconds. Students can ask any question and receive:
- **AI-Generated Video Lessons** with synchronized audio narration
- **Auto-Generated Graphs** for mathematical concepts
- **Comprehensive PDF Notes** with definitions, formulas, and examples
- **PowerPoint Presentations** ready for review
- **Practice Assignments** with auto-graded quizzes and answer keys

The platform aims to make quality education accessible to everyone by automating content creation while maintaining high educational standards.

## Key Features

### AI-Powered Content Generation
- Generates explanations with **worked examples** and **step-by-step derivations**
- Detects mathematical topics and automatically creates **visual graphs**
- Includes **real-world applications** for better understanding
- Provides **multiple solved examples** for practice

### Multimedia Learning Materials
- **Audio-Synced Videos**: Perfectly synchronized audio narration with visual content
- **Dynamic Slides**: Automatically adjusts slide count based on content complexity
- **Smooth Animations**: Fade in/out effects and staggered text entry
- **Background Images**: Topic-relevant images for better engagement

### User Management
- **Secure Authentication**: JWT-based login system with password hashing
- **User Profiles**: Track learning progress and statistics
- **Lesson History**: Access all previously generated lessons
- **Guest Mode**: Try the platform without creating an account

### 📊 Interactive Features
- **Editable Notes**: Modify and personalize study notes
- **Carousel Slides**: Navigate through presentation slides
- **Interactive Quizzes**: Multiple choice, true/false, and short answer questions
- **Instant Feedback**: Auto-grading with explanations

### 🎯 Subject Coverage
- Mathematics (Algebra, Calculus, Geometry, Trigonometry)
- Physics (Mechanics, Thermodynamics, Electromagnetism)
- Chemistry (Organic, Inorganic, Physical Chemistry)
- Computer Science (Data Structures, Algorithms, Programming)
- And more...

## 🛠️ Tech Stack

### Frontend
- **React** - UI framework
- **Tailwind CSS** - Styling and animations
- **Axios** - HTTP client
- **React Router** - Navigation
- **Context API** - State management

### Backend
- **FastAPI** - Web framework
- **Python 3.11** - Programming language
- **SQLAlchemy** - ORM for database
- **PostgreSQL/SQLite** - Database
- **JWT** - Authentication

### AI & Media Processing
- **Google Gemini AI** - Content generation
- **gTTS** - Text-to-speech conversion
- **MoviePy** - Video creation and editing
- **Matplotlib** - Graph generation
- **Pillow** - Image processing
- **ReportLab** - PDF generation
- **python-pptx** - PowerPoint creation

## 📸 Screenshots

### Home Page
Ask any question and get instant learning materials

### Video Lesson
AI-generated video with synchronized audio and animations

### Interactive Notes
Editable study notes with key concepts and examples

### User Dashboard
Track your learning progress and access lesson history

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn package manager
- Git

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/NikitaDevda/AI-Teacher.git
cd AI-Teacher
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
touch .env

# Edit .env and add your API keys:
# GEMINI_API_KEY=your_gemini_api_key
# SECRET_KEY=your_secret_key_for_jwt
```

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ai-teaching-system

# Install dependencies
npm install

# Create .env file
touch .env

# Edit .env:
# VITE_API_BASE_URL=http://localhost:8000
```

#### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd ai-teaching-system
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📖 Usage Guide

### For Students

1. **Sign Up / Login**
   - Create a free account or try as a guest
   - Guest mode generates materials but doesn't save them

2. **Ask a Question**
   - Enter any topic or question in the search box
   - Select the subject category
   - Click "Generate Lesson"

3. **Learn**
   - Watch the AI-generated video
   - Read and edit your notes
   - Navigate through presentation slides
   - Take the practice quiz

4. **Download Materials**
   - Download PDF notes
   - Download PowerPoint presentation
   - Download assignment and answer key
   - Access everything offline

5. **Track Progress**
   - View your lesson history in the dashboard
   - See learning statistics
   - Mark lessons as complete

### Example Questions

- "Explain quadratic equations with examples"
- "What is Newton's second law of motion?"
- "How does photosynthesis work?"
- "Explain bubble sort algorithm step by step"
- "Derive the Pythagorean theorem"

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
# AI Service
GEMINI_API_KEY=your_gemini_api_key_here

# Security
SECRET_KEY=your-secret-key-for-jwt-tokens

# Database
DATABASE_URL=sqlite:///./ai_teacher.db  # Local
# DATABASE_URL=postgresql://user:pass@host/db  # Production

# Optional
UNSPLASH_ACCESS_KEY=your_unsplash_key  # For images
```

**Frontend (.env)**
```env
# API URL
VITE_API_BASE_URL=http://localhost:8000  # Development
# VITE_API_BASE_URL=https://your-backend.com  # Production
```

## 📁 Project Structure
