from typing import Any, Dict, Optional
import hashlib
import json
from pathlib import Path
import time
from .logger import setup_logger

logger = setup_logger(__name__)

def load_json(file_path: str) -> Optional[Dict]:
    """Load JSON file safely."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"JSON load error: {e}")
        return None

def save_json(data: Dict, file_path: str) -> bool:
    """Save dictionary to JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"JSON save error: {e}")
        return False

def hash_data(data: Any) -> str:
    """Create hash of data."""
    try:
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        return hashlib.sha256(str(data).encode()).hexdigest()
    except Exception as e:
        logger.error(f"Hash creation error: {e}")
        return ""

def ensure_directory(path: str) -> bool:
    """Create directory if it doesn't exist."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Directory creation error: {e}")
        return False

def retry_operation(
    func: callable,
    max_attempts: int = 3,
    delay: float = 1.0
) -> Any:
    """Retry an operation with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay * (2 ** attempt))

def sanitize_input(data: Dict) -> Dict:
    """Sanitize input data."""
    try:
        return {
            k: sanitize_value(v)
            for k, v in data.items()
        }
    except Exception as e:
        logger.error(f"Input sanitization error: {e}")
        return {}

def sanitize_value(value: Any) -> Any:
    """Sanitize a single value."""
    if isinstance(value, str):
        return value.strip()
    elif isinstance(value, dict):
        return sanitize_input(value)
    elif isinstance(value, list):
        return [sanitize_value(v) for v in value]
    return value