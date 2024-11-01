from typing import Dict, List, Optional
import json
from datetime import datetime
from .logger import setup_logger

logger = setup_logger(__name__)


class PolicyManager:
    """Manages privacy policies and their rules."""

    def __init__(self, policy_file: Optional[str] = None):
        self.policies: Dict[str, Dict] = {}
        self.active_policies: Dict[str, bool] = {}
        if policy_file:
            self.load_policies(policy_file)

    def add_policy(self, policy_id: str, policy_data: Dict) -> bool:
        """Add or update a policy."""
        try:
            self.policies[policy_id] = {
                **policy_data,
                'last_updated': datetime.now().isoformat(),
                'version': policy_data.get('version', 1) + 1
            }
            self.active_policies[policy_id] = True
            logger.info(f"Policy {policy_id} added/updated")
            return True
        except Exception as e:
            logger.error(f"Error adding policy: {e}")
            return False

    def get_active_policies(self) -> Dict[str, Dict]:
        """Get all active policies."""
        return {
            pid: policy for pid, policy in self.policies.items()
            if self.active_policies.get(pid, False)
        }

    def validate_policy(self, policy_data: Dict) -> bool:
        """Validate policy structure."""
        required_fields = {'rules', 'data_types', 'actions'}
        return all(field in policy_data for field in required_fields)
