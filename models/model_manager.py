import joblib
import numpy as np
import warnings
from pathlib import Path
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
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
    """Manage model loading and predictions."""

    def __init__(self):
        self.svm_model = None
        self.dt_model = None
        self.scaler = None
        self._load_models()
        self._ensure_fitted_scaler()

    def _load_models(self):
        """Load models and scaler from configured paths, fallback to simulated if missing."""
        try:
            # Resolve absolute path to models directory from config
            project_root = Path(__file__).resolve().parent.parent
            model_path = project_root / MODEL_PATH

            # Ensure directory exists
            model_path.mkdir(parents=True, exist_ok=True)

            # Load scaler if present
            scaler_file = model_path / SCALER_FILE
            if scaler_file.exists():
                self.scaler = joblib.load(scaler_file)
                st.success("✓ Échelle (scaler) chargée avec succès !")
            else:
                self.scaler = StandardScaler()
                st.info(
                    "ℹ️ Fichier du scaler introuvable. Initialisation d'un nouveau scaler.")

            # Try to load SVM model
            svm_file = model_path / "svm_model.pkl"
            if svm_file.exists():
                self.svm_model = joblib.load(svm_file)
                st.success("✓ Modèle SVM chargé avec succès !")
            else:
                self.svm_model = SVC(probability=True)
                st.info("ℹ️ Modèle SVM introuvable. Utilisation d'un modèle simulé.")

            # Try to load Decision Tree model
            dt_file = model_path / "decision_tree_model.pkl"
            if dt_file.exists():
                self.dt_model = joblib.load(dt_file)
                st.success("✓ Modèle Arbre de décision chargé avec succès !")
            else:
                self.dt_model = DecisionTreeClassifier()
                st.info(
                    "ℹ️ Modèle Arbre de décision introuvable. Utilisation d'un modèle simulé.")

        except Exception as e:
            st.error(f"❌ Erreur de chargement des modèles : {e}")

    def _ensure_fitted_scaler(self):
        """Ensure the scaler is fitted; if not, fit on synthetic data from feature ranges."""
        try:
            if self.scaler is None:
                self.scaler = StandardScaler()

            # Check if scaler has been fitted
            if not hasattr(self.scaler, "mean_"):
                from config import FEATURE_RANGES
                import numpy as np

                # Build a small synthetic dataset using min/mean/max per feature (5 features)
                mins = [
                    FEATURE_RANGES["air_temperature_k"][0],
                    FEATURE_RANGES["process_temperature_k"][0],
                    FEATURE_RANGES["rotational_speed_rpm"][0],
                    FEATURE_RANGES["torque_nm"][0],
                    FEATURE_RANGES["tool_wear_min"][0],
                ]
                means = [
                    sum(FEATURE_RANGES["air_temperature_k"]) / 2,
                    sum(FEATURE_RANGES["process_temperature_k"]) / 2,
                    int(sum(FEATURE_RANGES["rotational_speed_rpm"]) / 2),
                    sum(FEATURE_RANGES["torque_nm"]) / 2,
                    int(sum(FEATURE_RANGES["tool_wear_min"]) / 2),
                ]
                maxs = [
                    FEATURE_RANGES["air_temperature_k"][1],
                    FEATURE_RANGES["process_temperature_k"][1],
                    FEATURE_RANGES["rotational_speed_rpm"][1],
                    FEATURE_RANGES["torque_nm"][1],
                    FEATURE_RANGES["tool_wear_min"][1],
                ]

                X_synth = np.array([mins, means, maxs], dtype=float)
                self.scaler.fit(X_synth)
                st.info(
                    "ℹ️ Scaler not found/fitted. Using synthetic fit based on feature ranges.")
        except Exception as e:
            st.error(f"❌ Erreur lors de la configuration du scaler : {e}")

    def predict(self, X_scaled: np.ndarray, model_name: str) -> tuple[np.ndarray, np.ndarray]:
        """
        Make predictions.

        Returns:
            predictions (0/1), probabilities
        """
        try:
            if model_name == "Support Vector Machine (SVM)":
                model = self.svm_model
            else:
                model = self.dt_model

            predictions = model.predict(X_scaled)

            # Get probabilities
            if hasattr(model, "predict_proba"):
                proba_all = model.predict_proba(X_scaled)
                # Determine the column corresponding to class label 1
                try:
                    classes = getattr(model, "classes_", None)
                    if classes is not None:
                        # Find index of class 1; default to last column if not found
                        if 1 in classes:
                            idx1 = int(np.where(classes == 1)[0][0])
                        else:
                            idx1 = -1
                        proba = proba_all[:, idx1]
                    else:
                        # Fallback: assume second column corresponds to class 1
                        proba = proba_all[:, -1]
                except Exception:
                    # Robust fallback
                    proba = proba_all[:, -1]
            else:
                proba = np.random.rand(len(predictions)) * 0.3  # Simulate

            return predictions, proba

        except Exception as e:
            st.error(f"❌ Erreur de prédiction : {e}")
            return None, None

    def get_scaler(self):
        """Return fitted scaler."""
        return self.scaler
