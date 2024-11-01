from typing import Dict, List, Any
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
from .logger import setup_logger

logger = setup_logger(__name__)


class MLEngine:
    """Machine learning engine for policy decisions."""

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.feature_names: List[str] = []
        if model_path:
            self.load_model(model_path)
        else:
            self.model = RandomForestClassifier(n_estimators=100)

    def train(self, features: List[Dict], labels: List[int]):
        """Train the ML model."""
        try:
            if not features or not labels:
                return False

            X = self._prepare_features(features)
            self.model.fit(X, labels)
            return True
        except Exception as e:
            logger.error(f"Training error: {e}")
            return False

    def predict(self, feature_dict: Dict) -> float:
        """Predict access permission probability."""
        try:
            if not self.model:
                return 0.5

            X = self._prepare_features([feature_dict])
            return float(self.model.predict_proba(X)[0][1])
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 0.5

    def _prepare_features(self, feature_dicts: List[Dict]) -> np.ndarray:
        """Prepare feature dictionary for model."""
        try:
            if not self.feature_names:
                self.feature_names = list(feature_dicts[0].keys())

            X = np.zeros((len(feature_dicts), len(self.feature_names)))
            for i, fd in enumerate(feature_dicts):
                for j, feature in enumerate(self.feature_names):
                    X[i, j] = fd.get(feature, 0)
            return X
        except Exception as e:
            logger.error(f"Feature preparation error: {e}")
            return np.array([])