# from pydantic import BaseModel
# from typing import List, Optional

# class QuestionRequest(BaseModel):
#     """Request model for asking questions"""
#     question: str
#     subject: str = "general"
#     language: str = "hi"
#     session_id: Optional[str] = None

# class Message(BaseModel):
#     """Individual message in conversation"""
#     role: str  # "user" or "assistant"
#     content: str
#     timestamp: str

# # class SessionResponse(BaseModel):
# #     """Response model with answer and metadata"""
# #     session_id: str
# #     answer: str
# #     video_url: Optional[str] = None
# #     audio_url: Optional[str] = None
# #     conversation_history: List[Message]

# class SessionResponse(BaseModel):
#     session_id: str
#     answer: str
#     whiteboard_content: Optional[str] = None  # ✅ NEW!
#     video_url: Optional[str] = None
#     audio_url: Optional[str] = None
#     conversation_history: List[Message]




from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    subject: str = "general"

class Message(BaseModel):
    role: str
    content: str
    timestamp: str = datetime.now().isoformat()

class SessionResponse(BaseModel):
    session_id: str
    answer: str
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    pdf_notes_url: Optional[str] = None
    ppt_url: Optional[str] = None
    assignment_url: Optional[str] = None
    answers_url: Optional[str] = None
    # ✅ NEW: Web content for interactive display
    notes_content: Optional[dict] = None
    slides_content: Optional[list] = None
    assignment_content: Optional[dict] = None
    whiteboard_content: Optional[str] = None
    conversation_history: List[Message] = []