from typing import Dict, Optional
from .policy_manager import PolicyManager
from .context_handler import ContextHandler
from .ml_engine import MLEngine
from .logger import setup_logger

logger = setup_logger(__name__)


class PolicyEnforcer:
    """Enforces privacy policies based on context and ML predictions."""

    def __init__(
            self,
            policy_manager: PolicyManager,
            context_handler: ContextHandler,
            ml_engine: MLEngine
    ):
        self.policy_manager = policy_manager
        self.context_handler = context_handler
        self.ml_engine = ml_engine
        self.decision_threshold = 0.7

    def check_access(
            self,
            user_id: str,
            data_type: str,
            action: str
    ) -> Dict:
        """Check if access should be granted."""
        try:
            # Get relevant policies
            policies = self.policy_manager.get_active_policies()

            # Get user context
            context = self.context_handler.get_context(user_id)
            if not context:
                return {'allowed': False, 'reason': 'No context available'}

            # Calculate risk
            risk_score = self.context_handler.evaluate_risk(user_id, action)

            # Prepare features for ML
            features = {
                'risk_score': risk_score,
                'data_type': hash(data_type) % 100,  # Simple feature
                'action_type': hash(action) % 100,
                'context_score': len(context) / 10
            }

            # Get ML prediction
            access_score = self.ml_engine.predict(features)

            # Make decision
            allowed = access_score > self.decision_threshold

            return {
                'allowed': allowed,
                'confidence': access_score,
                'risk_score': risk_score,
                'policy_ids': list(policies.keys())
            }

        except Exception as e:
            logger.error(f"Access check error: {e}")
            return {'allowed': False, 'reason': 'Error during check'}