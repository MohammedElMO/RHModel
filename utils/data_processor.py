import pandas as pd
import numpy as np
from config import FEATURE_RANGES


class DataProcessor:
    """Handle data validation and preprocessing."""

    @staticmethod
    def validate_input(data: dict) -> tuple[bool, str]:
        """Validate input features."""
        try:
            for feature, value in data.items():
                if feature == "type":
                    if value not in FEATURE_RANGES["type"]:
                        return False, f"Invalid type: {value}"
                else:
                    min_val, max_val = FEATURE_RANGES.get(
                        feature, (None, None))
                    if min_val and max_val:
                        if not (min_val <= value <= max_val):
                            return False, f"{feature} out of range: {min_val}-{max_val}"
            return True, "Valid"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def prepare_single_input(input_dict: dict, scaler) -> np.ndarray:
        """Prepare single input for prediction."""
        feature_order = [
            "type", "air_temperature_k", "process_temperature_k",
            "rotational_speed_rpm", "torque_nm", "tool_wear_min"
        ]

        # Encode type (L=0, M=1, H=2)
        type_map = {"L": 0, "M": 1, "H": 2}
        input_dict["type"] = type_map.get(input_dict["type"], 0)

        X = np.array([[input_dict[f] for f in feature_order]])
        return scaler.transform(X)

    @staticmethod
    def process_csv(df: pd.DataFrame, scaler) -> pd.DataFrame:
        """Process CSV for batch prediction."""
        required_cols = [
            "type", "air_temperature_k", "process_temperature_k",
            "rotational_speed_rpm", "torque_nm", "tool_wear_min"
        ]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df_processed = df.copy()
        type_map = {"L": 0, "M": 1, "H": 2}
        df_processed["type"] = df_processed["type"].map(type_map)

        X = scaler.transform(df_processed[required_cols])
        return pd.DataFrame(X, columns=required_cols), df_processed
