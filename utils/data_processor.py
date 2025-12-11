import pandas as pd
import numpy as np
from config import FEATURE_RANGES


class DataProcessor:
    """Handle data validation and preprocessing."""

    @staticmethod
    def validate_input(data: dict) -> tuple[bool, str]:
        """Validate input features (excluding 'type')."""
        try:
            for feature, value in data.items():
                if feature == "type":
                    # 'type' is no longer used; ignore if present
                    continue
                min_val, max_val = FEATURE_RANGES.get(feature, (None, None))
                if min_val is not None and max_val is not None:
                    if not (min_val <= value <= max_val):
                        return False, f"{feature} hors limites : {min_val}–{max_val}"
            return True, "Valide"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def prepare_single_input(input_dict: dict, scaler) -> np.ndarray:
        """Prepare single input for prediction (5 numeric features only)."""
        feature_order = [
            "air_temperature_k", "process_temperature_k",
            "rotational_speed_rpm", "torque_nm", "tool_wear_min"
        ]

        # Use numpy array (no feature names) to avoid sklearn feature name mismatch
        X = np.array([[input_dict[f] for f in feature_order]])
        return scaler.transform(X)

    @staticmethod
    def process_csv(df: pd.DataFrame, scaler) -> pd.DataFrame:
        """Process CSV for batch prediction (ignore 'type' if present)."""
        required_cols = [
            "air_temperature_k", "process_temperature_k",
            "rotational_speed_rpm", "torque_nm", "tool_wear_min"
        ]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df_processed = df.copy()
        # Use numpy array (no feature names) to avoid sklearn feature name mismatch
        X = scaler.transform(df_processed[required_cols].values)
        return X, df_processed
