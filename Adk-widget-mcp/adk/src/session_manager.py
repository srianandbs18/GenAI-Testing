"""
Session Manager for ADK
Handles in-memory session storage with automatic cleanup
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import threading


class SessionManager:
    """In-memory session storage for demo purposes"""
    
    def __init__(self, session_timeout: int = 1800):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.session_timeout = session_timeout
    
    def create_session(self) -> str:
        """Create new session and return session_id"""
        session_id = str(uuid.uuid4())
        
        with self._lock:
            self._sessions[session_id] = {
                "session_id": session_id,
                "created_at": datetime.utcnow(),
                "last_activity": datetime.utcnow(),
                "context": {
                    "timezone": "Eastern Time (ET)",
                    "timezone_abbr": "ET",
                    "selected_date": None,
                    "selected_date_value": None,
                    "selected_time": None,
                    "selected_time_value": None,
                    "current_widget": "schedule_meeting",
                    "current_action": None
                },
                "conversation_history": []
            }
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session by ID"""
        with self._lock:
            session = self._sessions.get(session_id)
            
            if session:
                if self._is_expired(session):
                    del self._sessions[session_id]
                    return None
                
                session["last_activity"] = datetime.utcnow()
            
            return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session context"""
        with self._lock:
            if session_id not in self._sessions:
                return False
            
            session = self._sessions[session_id]
            
            if "context" in data:
                session["context"].update(data["context"])
            
            if "conversation_history" in data:
                session["conversation_history"].extend(data["conversation_history"])
            
            session["last_activity"] = datetime.utcnow()
            return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions"""
        with self._lock:
            expired_ids = [
                sid for sid, session in self._sessions.items()
                if self._is_expired(session)
            ]
            
            for sid in expired_ids:
                del self._sessions[sid]
            
            return len(expired_ids)
    
    def _is_expired(self, session: Dict[str, Any]) -> bool:
        """Check if session is expired"""
        last_activity = session["last_activity"]
        age = (datetime.utcnow() - last_activity).total_seconds()
        return age > self.session_timeout


# Singleton instance
_session_manager = None


def get_session_manager() -> SessionManager:
    """Get or create singleton SessionManager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
