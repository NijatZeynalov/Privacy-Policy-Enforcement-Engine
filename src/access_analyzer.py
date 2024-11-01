from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta
from .logger import setup_logger

logger = setup_logger(__name__)


class AccessAnalyzer:
    """Analyzes data access patterns."""

    def __init__(self, lookback_days: int = 30):
        self.lookback_days = lookback_days
        self.access_history: List[Dict] = []

    def track_access(self, user_id: str, data_type: str, action: str):
        """Record a data access event."""
        self.access_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'data_type': data_type,
            'action': action
        })

    def analyze_patterns(self, user_id: str) -> Dict:
        """Analyze access patterns for a user."""
        try:
            df = pd.DataFrame(self.access_history)
            if df.empty:
                return {}

            df['timestamp'] = pd.to_datetime(df['timestamp'])
            user_df = df[df['user_id'] == user_id]

            cutoff = datetime.now() - timedelta(days=self.lookback_days)
            recent_df = user_df[user_df['timestamp'] > cutoff]

            return {
                'access_frequency': len(recent_df),
                'data_types': recent_df['data_type'].value_counts().to_dict(),
                'actions': recent_df['action'].value_counts().to_dict(),
                'last_access': recent_df['timestamp'].max().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing patterns: {e}")
            return {}
