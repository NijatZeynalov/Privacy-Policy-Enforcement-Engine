from typing import Dict, List, Optional
import json
from datetime import datetime
from .logger import setup_logger

logger = setup_logger(__name__)


class RuleGenerator:
    """Generates dynamic privacy rules based on patterns."""

    def __init__(self):
        self.rules: Dict[str, Dict] = {}
        self.rule_templates = {
            'time_based': {
                'type': 'temporal',
                'conditions': ['time_range', 'day_of_week'],
                'actions': ['allow', 'deny', 'require_approval']
            },
            'location_based': {
                'type': 'spatial',
                'conditions': ['location', 'network_type'],
                'actions': ['allow', 'deny', 'require_mfa']
            },
            'risk_based': {
                'type': 'risk',
                'conditions': ['risk_score', 'attempt_count'],
                'actions': ['allow', 'deny', 'require_verification']
            }
        }

    def generate_rule(
            self,
            pattern_data: Dict,
            rule_type: str
    ) -> Optional[Dict]:
        """Generate a new rule based on observed patterns."""
        try:
            if rule_type not in self.rule_templates:
                return None

            template = self.rule_templates[rule_type]
            rule = {
                'id': f"rule_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'type': template['type'],
                'created_at': datetime.now().isoformat(),
                'conditions': {},
                'action': 'deny'  # Default to deny
            }

            # Add conditions based on pattern data
            for condition in template['conditions']:
                if condition in pattern_data:
                    rule['conditions'][condition] = pattern_data[condition]

            # Determine action based on risk
            risk_score = pattern_data.get('risk_score', 1.0)
            if risk_score < 0.3:
                rule['action'] = 'allow'
            elif risk_score < 0.7:
                rule['action'] = template['actions'][-1]  # Use strictest non-deny action

            return rule

        except Exception as e:
            logger.error(f"Rule generation error: {e}")
            return None

    def validate_rule(self, rule: Dict) -> bool:
        """Validate a generated rule."""
        try:
            required_fields = {'id', 'type', 'conditions', 'action'}
            if not all(field in rule for field in required_fields):
                return False

            if not rule['conditions']:
                return False

            if rule['type'] not in {t['type'] for t in self.rule_templates.values()}:
                return False

            return True

        except Exception as e:
            logger.error(f"Rule validation error: {e}")
            return False