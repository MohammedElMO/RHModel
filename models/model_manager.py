import joblib
import numpy as np
import warnings
from pathlib import Path
import streamlit as st
from config import MODEL_PATH, SCALER_FILE

# Suppress sklearn version mismatch warnings globally
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
try:
    from sklearn.exceptions import InconsistentVersionWarning
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
except ImportError:
    pass


class ModelManager:
    """Manage model loading and predictions without simulation fallback."""

    def __init__(self):
        self.svm_model = None
        self.dt_model = None
        self.scaler = None
        self._load_models()
        # Removed _ensure_fitted_scaler() to prevent synthetic data usage

    def _load_models(self):
        """Load models and scaler from configured paths. Fail if missing."""
        try:
            # Resolve absolute path to models directory from config
            project_root = Path(__file__).resolve().parent.parent
            model_path = project_root / MODEL_PATH

            # Ensure directory exists
            if not model_path.exists():
                st.error(
                    f"❌ Error: The model directory '{model_path}' does not exist.")
                return

            # 1. Load Scaler (Strict Requirement)
            scaler_file = model_path / SCALER_FILE
            if scaler_file.exists():
                self.scaler = joblib.load(scaler_file)
                st.success("✓ Échelle (scaler) chargée avec succès !")
            else:
                self.scaler = None
                st.error(
                    f"❌ Erreur critique : Fichier scaler introuvable ({scaler_file}). Les prédictions sont impossibles.")

            # 2. Load SVM Model
            svm_file = model_path / "svm_model.pkl"
            if svm_file.exists():
                self.svm_model = joblib.load(svm_file)
                st.success("✓ Modèle SVM chargé avec succès !")
            else:
                self.svm_model = None
                st.warning("⚠️ Modèle SVM introuvable (svm_model.pkl).")

            # 3. Load Decision Tree Model
            dt_file = model_path / "decision_tree_model.pkl"
            if dt_file.exists():
                self.dt_model = joblib.load(dt_file)
                st.success("✓ Modèle Arbre de décision chargé avec succès !")
            else:
                self.dt_model = None
                st.warning(
                    "⚠️ Modèle Arbre de décision introuvable (decision_tree_model.pkl).")

        except Exception as e:
            st.error(f"❌ Erreur de chargement des modèles : {e}")

    def predict(self, X_scaled: np.ndarray, model_name: str) -> tuple[np.ndarray, np.ndarray]:
        """
        Make predictions only if models are loaded.
        Returns: predictions (0/1), probabilities
        """
        # Strict check: If scaler failed to load, we cannot trust X_scaled
        if self.scaler is None:
            st.error("⛔ Action bloquée : Le scaler n'est pas chargé.")
            return None, None

        # Select the model
        if model_name == "Support Vector Machine (SVM)":
            model = self.svm_model
        else:
            model = self.dt_model

        # Strict check: If model failed to load, do not predict
        if model is None:
            st.error(
                f"⛔ Action bloquée : Le modèle '{model_name}' n'est pas chargé. Vérifiez le dossier models_pkl.")
            return None, None

        try:
            predictions = model.predict(X_scaled)

            # Get probabilities
            if hasattr(model, "predict_proba"):
                proba_all = model.predict_proba(X_scaled)
                # Determine the column corresponding to class label 1
                try:
                    classes = getattr(model, "classes_", None)
                    if classes is not None:
                        if 1 in classes:
                            idx1 = int(np.where(classes == 1)[0][0])
                        else:
                            idx1 = -1
                        proba = proba_all[:, idx1]
                    else:
                        proba = proba_all[:, -1]
                except Exception:
                    proba = proba_all[:, -1]
            else:
                # Removed random simulation. If model has no probabilities, warn user.
                st.warning(
                    "⚠️ Ce modèle ne supporte pas les probabilités (predict_proba manquant).")
                proba = np.zeros(len(predictions))

            return predictions, proba

        except Exception as e:
            st.error(f"❌ Erreur de prédiction : {e}")
            return None, None

    def get_scaler(self):
        """Return loaded scaler or None."""
        return self.scaler
