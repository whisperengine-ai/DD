"""
Anchor Triad: Embodiment/Feedback processing.
Simplified version with interaction logging and session tracking.
"""
import json
from datetime import datetime
from typing import Dict, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AnchorTriad:
    """Simplified embodiment/feedback processing."""
    
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Anchor initialized with log file: {log_file}")
    
    def process(self, text: str, user_id: str, session_id: str) -> Dict:
        """
        Simplified: Embodiment → Implementation → Reflection.
        """
        logger.info(f"Anchor processing for user {user_id}, session {session_id}")
        
        # 1. Embodiment: Log interaction
        interaction = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'session_id': session_id,
            'text': text,
            'text_length': len(text)
        }
        
        # 2. Implementation: Create response based on text
        response = self._generate_response(text)
        
        # 3. Reflection: Store feedback
        self._log_interaction(interaction)
        
        return {
            'interaction_logged': True,
            'session_id': session_id,
            'response': response,
            'interaction_count': self._count_interactions(session_id)
        }
    
    def _generate_response(self, text: str) -> str:
        """Generate a simple response based on input."""
        # For MVP: Simple echoing with affirmation
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['help', 'assist', 'guide']):
            return f"I'm here to help you. Processing: {text[:50]}..."
        elif any(word in text_lower for word in ['wisdom', 'knowledge', 'learn']):
            return f"Seeking wisdom is virtuous. Reflecting on: {text[:50]}..."
        elif any(word in text_lower for word in ['thank', 'grateful', 'appreciate']):
            return "Gratitude is a noble virtue. I'm glad to assist you."
        else:
            return f"Acknowledged. Processing your input: {text[:50]}..."
    
    def _log_interaction(self, interaction: Dict):
        """Append to JSON log file."""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(interaction) + '\n')
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")
    
    def get_session_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve past interactions for a session."""
        history = []
        try:
            if not self.log_file.exists():
                return history
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get('session_id') == session_id:
                            history.append(data)
                    except json.JSONDecodeError:
                        continue
            
            # Return most recent first
            return history[-limit:]
        except Exception as e:
            logger.error(f"Error retrieving session history: {e}")
            return []
    
    def _count_interactions(self, session_id: str) -> int:
        """Count interactions for a session."""
        return len(self.get_session_history(session_id, limit=9999))
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve past interactions for a user."""
        history = []
        try:
            if not self.log_file.exists():
                return history
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get('user_id') == user_id:
                            history.append(data)
                    except json.JSONDecodeError:
                        continue
            
            return history[-limit:]
        except Exception as e:
            logger.error(f"Error retrieving user history: {e}")
            return []
