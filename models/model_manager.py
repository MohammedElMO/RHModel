import joblib
import numpy as np
from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import streamlit as st


class ModelManager:
    """Manage model loading and predictions."""

    def __init__(self):
        self.knn_model = None
        self.svm_model = None
        self.dt_model = None
        self.scaler = None
        self._load_models()

    def _load_models(self):
        """Load or create models."""
        try:
            # Get absolute path to models directory
            current_dir = Path(__file__).parent.parent
            model_path = current_dir / "models_pkl"

            # Ensure directory exists
            model_path.mkdir(parents=True, exist_ok=True)

            # Load KNN model and scaler
            knn_file = model_path / "knn_model_v2.pkl"
            scaler_file = model_path / "scaler_v2.pkl"

            if knn_file.exists() and scaler_file.exists():
                self.knn_model = joblib.load(knn_file)
                self.scaler = joblib.load(scaler_file)
                st.success("✓ Real KNN model and scaler loaded successfully!")
            else:
                # Create dummy KNN model and scaler
                self.knn_model = KNeighborsClassifier(n_neighbors=5)
                self.scaler = StandardScaler()
                st.warning(
                    "⚠️ Using simulated KNN model. Place knn_model_v2.pkl and scaler_v2.pkl in models_pkl/ for production.")

            # Try to load SVM model
            svm_file = model_path / "svm_model.pkl"
            if svm_file.exists():
                self.svm_model = joblib.load(svm_file)
                st.success("✓ SVM model loaded successfully!")
            else:
                self.svm_model = SVC(probability=True)
                st.info("ℹ️ SVM model not found. Using simulated model.")

            # Try to load Decision Tree model
            dt_file = model_path / "dt_model.pkl"
            if dt_file.exists():
                self.dt_model = joblib.load(dt_file)
                st.success("✓ Decision Tree model loaded successfully!")
            else:
                self.dt_model = DecisionTreeClassifier()
                st.info("ℹ️ Decision Tree model not found. Using simulated model.")

        except Exception as e:
            st.error(f"❌ Model loading error: {e}")

    def predict(self, X_scaled: np.ndarray, model_name: str) -> tuple[np.ndarray, np.ndarray]:
        """
        Make predictions.

        Returns:
            predictions (0/1), probabilities
        """
        try:
            if model_name == "K-Nearest Neighbors (KNN)":
                model = self.knn_model
            elif model_name == "Support Vector Machine (SVM)":
                model = self.svm_model
            else:
                model = self.dt_model

            predictions = model.predict(X_scaled)

            # Get probabilities
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_scaled)[:, 1]
            else:
                proba = np.random.rand(len(predictions)) * 0.3  # Simulate

            return predictions, proba

        except Exception as e:
            st.error(f"❌ Prediction error: {e}")
            return None, None

    def get_scaler(self):
        """Return fitted scaler."""
        return self.scaler
