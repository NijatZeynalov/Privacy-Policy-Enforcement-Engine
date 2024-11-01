from typing import Dict, Optional
from datetime import datetime
import json
from .logger import setup_logger

logger = setup_logger(__name__)


class UserContext:
    """Manages and evaluates user context information."""

    def __init__(self):
        self.contexts: Dict[str, Dict] = {}
        self.risk_factors = {
            'location_change': 0.3,
            'unusual_time': 0.4,
            'new_device': 0.5,
            'vpn_usage': 0.2,
            'failed_attempts': 0.6
        }

    def update_context(
            self,
            user_id: str,
            context_data: Dict
    ) -> bool:
        """Update user's context."""
        try:
            old_context = self.contexts.get(user_id, {})

            self.contexts[user_id] = {
                **context_data,
                'last_updated': datetime.now().isoformat(),
                'previous_location': old_context.get('location'),
                'previous_device': old_context.get('device')
            }

            return True
        except Exception as e:
            logger.error(f"Context update error: {e}")
            return False

    def evaluate_risk(self, user_id: str) -> float:
        """Evaluate risk based on user's context."""
        try:
            context = self.contexts.get(user_id)
            if not context:
                return 1.0

            risk_score = 0.0

            # Check location change
            if (context.get('previous_location') and
                    context.get('location') != context['previous_location']):
                risk_score += self.risk_factors['location_change']

            # Check time
            current_hour = datetime.now().hour
            if current_hour < 6 or current_hour > 22:  # Outside business hours
                risk_score += self.risk_factors['unusual_time']

            # Check device
            if (context.get('previous_device') and
                    context.get('device') != context['previous_device']):
                risk_score += self.risk_factors['new_device']

            # Check VPN
            if context.get('vpn_enabled'):
                risk_score += self.risk_factors['vpn_usage']

            # Check failed attempts
            failed_attempts = context.get('failed_attempts', 0)
            if failed_attempts > 0:
                risk_score += min(
                    self.risk_factors['failed_attempts'] * failed_attempts,
                    0.8
                )

            return min(risk_score, 1.0)

        except Exception as e:
            logger.error(f"Risk evaluation error: {e}")
            return 1.0