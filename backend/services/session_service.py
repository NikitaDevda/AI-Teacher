from typing import Dict, List
from datetime import datetime

class SessionService:
    def __init__(self):
        self.sessions: Dict[str, List] = {}
    
    def create_session(self, session_id: str):
        """Create new teaching session"""
        self.sessions[session_id] = []
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to session history"""
        
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.sessions[session_id].append(message)
        return message
    
    def get_history(self, session_id: str):
        """Get conversation history"""
        return self.sessions.get(session_id, [])
    
    def get_context_messages(self, session_id: str):
        """Get messages in OpenAI format"""
        history = self.get_history(session_id)
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]

# Global session manager
session_manager = SessionService()