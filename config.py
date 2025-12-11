# Model Configuration
MODEL_PATH = "models_pkl"
SCALER_FILE = "scaler.pkl"

# Feature Ranges (Industrial Standards)
FEATURE_RANGES = {
    "air_temperature_k": (295.0, 305.0),
    "process_temperature_k": (305.0, 315.0),
    "rotational_speed_rpm": (1168, 2772),
    "torque_nm": (3.8, 76.6),
    "tool_wear_min": (0, 240),
    "type": ["L", "M", "H"]
}

# Modern Color Palette (Adaptive to System Theme)
COLORS = {
    "primary": "#6366F1",        # Indigo
    "primary_light": "#818CF8",
    "secondary": "#8B5CF6",     # Purple
    "success": "#10B981",       # Emerald
    "warning": "#F59E0B",       # Amber
    "danger": "#EF4444",        # Red
    "info": "#3B82F6",          # Blue
    "gradient_1": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "gradient_2": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "gradient_3": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    "gradient_success": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
    "gradient_danger": "linear-gradient(135deg, #ee0979 0%, #ff6a00 100%)"
}

# Model Algorithms
MODELS = [
    "Support Vector Machine (SVM)",
    "Decision Tree"
]
