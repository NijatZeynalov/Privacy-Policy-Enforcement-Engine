from typing import Dict, List, Optional
import sqlite3
from datetime import datetime
import json
from .logger import setup_logger

logger = setup_logger(__name__)


class DataTracker:
    """Tracks and logs data access events."""

    def __init__(self, db_path: str = "data/access_logs.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS access_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        user_id TEXT,
                        data_type TEXT,
                        action TEXT,
                        success INTEGER,
                        context TEXT
                    )
                """)
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    def log_access(
            self,
            user_id: str,
            data_type: str,
            action: str,
            success: bool,
            context: Dict
    ):
        """Log a data access event."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO access_logs
                    (timestamp, user_id, data_type, action, success, context)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    user_id,
                    data_type,
                    action,
                    int(success),
                    json.dumps(context)
                ))
        except Exception as e:
            logger.error(f"Error logging access: {e}")

    def get_user_history(
            self,
            user_id: str,
            limit: int = 100
    ) -> List[Dict]:
        """Get access history for a user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM access_logs
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (user_id, limit))

                return [{
                    'timestamp': row[1],
                    'data_type': row[3],
                    'action': row[4],
                    'success': bool(row[5]),
                    'context': json.loads(row[6])
                } for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error retrieving history: {e}")
            return []