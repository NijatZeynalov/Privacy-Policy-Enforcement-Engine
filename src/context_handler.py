from typing import Dict, Optional
from datetime import datetime
from .logger import setup_logger

logger = setup_logger(__name__)


class ContextHandler:
    """Handles user context and environment factors."""

    def __init__(self):
        self.contexts: Dict[str, Dict] = {}

    def update_context(self, user_id: str, context_data: Dict) -> bool:
        """Update user context."""
        try:
            self.contexts[user_id] = {
                **context_data,
                'last_updated': datetime.now().isoformat()
            }
            return True
        except Exception as e:
            logger.error(f"Error updating context: {e}")
            return False

    def get_context(self, user_id: str) -> Optional[Dict]:
        """Get current context for a user."""
        return self.contexts.get(user_id)

    def evaluate_risk(self, user_id: str, action: str) -> float:
        """Evaluate risk based on context."""
        try:
            context = self.get_context(user_id)
            if not context:
                return 1.0  # High risk if no context

            risk_factors = {
                'unknown_location': 0.8,
                'unusual_time': 0.6,
                'suspicious_ip': 0.9,
                'new_device': 0.7
            }

            risk_score = 0.0
            flags = context.get('risk_flags', [])

            for flag in flags:
                if flag in risk_factors:
                    risk_score = max(risk_score, risk_factors[flag])

            return risk_score
        except Exception as e:
            logger.error(f"Error evaluating risk: {e}")
            return 1.0
