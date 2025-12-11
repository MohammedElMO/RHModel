import joblib
import numpy as np
import warnings
from pathlib import Path
import streamlit as st
from config import MODEL_PATH, SCALER_FILE

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


class ModelManager:
    """Manage model loading and predictions for Decision Tree only."""

    def __init__(self):
        self.dt_model = None
        self.scaler = None
        self._load_models()

    def _load_models(self):
        """Load Decision Tree and Scaler."""
        try:
            project_root = Path(__file__).resolve().parent.parent
            model_path = project_root / MODEL_PATH

            if not model_path.exists():
                st.error(f"Error: Directory '{model_path}' not found.")
                return

            # 1. Load Scaler (Still needed if DT was trained on scaled data)
            scaler_file = model_path / SCALER_FILE
            if scaler_file.exists():
                self.scaler = joblib.load(scaler_file)
            else:
                st.error(f"Scaler missing: {scaler_file}")
                return

            # 2. Load Decision Tree Only
            dt_file = model_path / "decision_tree_model.pkl"
            if dt_file.exists():
                self.dt_model = joblib.load(dt_file)
                st.success("Modèle IA (Arbre de Décision) chargé !")
            else:
                st.error("Modèle Arbre de Décision introuvable.")

        except Exception as e:
            st.error(f"Load Error: {e}")

    def predict(self, X_scaled: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Make predictions using the Decision Tree.
        """
        if self.scaler is None or self.dt_model is None:
            st.error("Modèle non chargé.")
            return None, None

        try:
            # Prediction
            predictions = self.dt_model.predict(X_scaled)

            # Probabilities (Decision Trees support this naturally)
            if hasattr(self.dt_model, "predict_proba"):
                proba_all = self.dt_model.predict_proba(X_scaled)
                # Handle binary classification probability (Class 1)
                if proba_all.shape[1] > 1:
                    proba = proba_all[:, 1]
                else:
                    proba = proba_all[:, -1]
            else:
                proba = np.zeros(len(predictions))

            return predictions, proba

        except Exception as e:
            st.error(f"Prediction Error: {e}")
            return None, None

    def get_scaler(self):
        return self.scaler
