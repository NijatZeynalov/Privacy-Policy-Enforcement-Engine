from .policy_manager import PolicyManager
from .enforcer import PolicyEnforcer
from .context_handler import ContextHandler
from .ml_engine import MLEngine
from .logger import setup_logger

logger = setup_logger(__name__)


class PrivacyEngine:
    """Main class for privacy policy enforcement."""

    def __init__(self, model_path: Optional[str] = None):
        try:
            self.policy_manager = PolicyManager()
            self.context_handler = ContextHandler()
            self.ml_engine = MLEngine(model_path)

            self.enforcer = PolicyEnforcer(
                self.policy_manager,
                self.context_handler,
                self.ml_engine
            )

        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise

    def check_access(
            self,
            user_id: str,
            data_type: str,
            action: str,
            context: Optional[Dict] = None
    ) -> Dict:
        """Check access permission."""
        try:
            # Update context if provided
            if context:
                self.context_handler.update_context(user_id, context)

            # Check access
            result = self.enforcer.check_access(user_id, data_type, action)

            logger.info(
                f"Access check - User: {user_id}, "
                f"Type: {data_type}, "
                f"Action: {action}, "
                f"Result: {result['allowed']}"
            )

            return result

        except Exception as e:
            logger.error(f"Access check error: {e}")
            return {'allowed': False, 'reason': 'System error'}


if __name__ == "__main__":
    engine = PrivacyEngine()
    result = engine.check_access(
        user_id="user123",
        data_type="customer_data",
        action="read",
        context={"location": "office", "device": "laptop"}
    )
    print(f"Access decision: {result}")