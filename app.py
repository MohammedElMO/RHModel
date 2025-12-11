from config import FEATURE_RANGES, MODELS, COLORS
from components.gauge_chart import create_failure_gauge
from components.status_badge import status_with_confidence
from utils.data_processor import DataProcessor
import streamlit as st
from utils.styles import apply_styles
from models.model_manager import ModelManager
from config import MODELS, COLORS


st.set_page_config(
    page_title="IoT Predictive Maintenance",
    page_icon="🛠️",
    layout="wide",
)

apply_styles()

# Model manager in session
if "model_manager" not in st.session_state:
    st.session_state.model_manager = ModelManager()

st.title("🔧 Predictive Maintenance Assistant")
st.caption("Simple, chat-style UI: enter values or upload CSV, then predict.")

# Modern, helpful sidebar (no routes)
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px 0;">
        <div style="font-size: 20px; font-weight: 700;">⚡ IoT Assistant</div>
        <div style="font-size: 12px; opacity: 0.7;">AI-powered equipment analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🤖 Model")
    selected_model = st.selectbox(
        "Select Model",
        MODELS,
        label_visibility="collapsed",
        help="Choose the algorithm used for predictions"
    )

    st.divider()

    st.markdown("### 💡 Tips")
    st.markdown(
        "- Use Manual Input for quick checks\n- Use CSV for fleet analysis\n- Ensure values fall within typical ranges")

    st.divider()

    st.markdown("### 📄 Required CSV Columns")
    st.code("air_temperature_k, process_temperature_k, rotational_speed_rpm, torque_nm, tool_wear_min")

    st.divider()

    with st.expander("ℹ️ Help & About"):
        st.markdown(
            "This tool predicts equipment safety vs. failure risk using pre-trained models in `models_pkl/`.")
        st.markdown(
            "For better accuracy, keep sensor inputs realistic and consistent.")

tab_manual, tab_csv = st.tabs(["Manual Input", "CSV Upload"])

with tab_manual:
    st.subheader("Manual Equipment Data")
    col1, col2, col3 = st.columns(3)

    # Inputs
    with col1:
        min_t, max_t = FEATURE_RANGES["air_temperature_k"]
        air_temperature_k = st.number_input(
            "Air Temperature (K)", min_value=float(min_t), max_value=float(max_t), value=float((min_t+max_t)/2), step=0.1
        )
    with col2:
        min_pt, max_pt = FEATURE_RANGES["process_temperature_k"]
        process_temperature_k = st.number_input(
            "Process Temperature (K)", min_value=float(min_pt), max_value=float(max_pt), value=float((min_pt+max_pt)/2), step=0.1
        )
        min_rpm, max_rpm = FEATURE_RANGES["rotational_speed_rpm"]
        rotational_speed_rpm = st.number_input(
            "Rotational Speed (RPM)", min_value=int(min_rpm), max_value=int(max_rpm), value=int((min_rpm+max_rpm)/2), step=10
        )
    with col3:
        min_torque, max_torque = FEATURE_RANGES["torque_nm"]
        torque_nm = st.number_input(
            "Torque (N·m)", min_value=float(min_torque), max_value=float(max_torque), value=float((min_torque+max_torque)/2), step=1.0
        )
        min_wear, max_wear = FEATURE_RANGES["tool_wear_min"]
        tool_wear_min = st.number_input(
            "Tool Wear (min)", min_value=int(min_wear), max_value=int(max_wear), value=int(max_wear//2), step=5
        )

    input_data = {
        "air_temperature_k": air_temperature_k,
        "process_temperature_k": process_temperature_k,
        "rotational_speed_rpm": rotational_speed_rpm,
        "torque_nm": torque_nm,
        "tool_wear_min": tool_wear_min,
    }

    if st.button("Predict", width="stretch"):
        valid, msg = DataProcessor.validate_input(input_data)
        if not valid:
            st.error(f"Validation Error: {msg}")
        else:
            try:
                X_scaled = DataProcessor.prepare_single_input(
                    input_data, st.session_state.model_manager.get_scaler())
                preds, probs = st.session_state.model_manager.predict(
                    X_scaled, selected_model)
                if preds is None:
                    st.error("Prediction failed.")
                else:
                    is_safe = preds[0] == 0
                    # probs[0] is 0-1 probability of failure (class 1)
                    failure_prob = float(probs[0])  # keep as 0-1
                    failure_pct = failure_prob * 100.0  # for display
                    confidence = (
                        100.0 - failure_pct) if is_safe else failure_pct
                    status_with_confidence(is_safe, confidence)
                    # Pass 0-1 probability; gauge will scale internally
                    fig = create_failure_gauge(failure_prob)
                    st.plotly_chart(fig, width="stretch")
            except Exception as e:
                st.error(f"Prediction error: {e}")

with tab_csv:
    st.subheader("Batch Prediction via CSV")
    uploaded = st.file_uploader(
        "Upload CSV with required columns",
        type=["csv"],
        help="Columns: air_temperature_k, process_temperature_k, rotational_speed_rpm, torque_nm, tool_wear_min"
    )
    if uploaded:
        import pandas as pd
        try:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head(10), width="stretch")
            if st.button("Run Batch Prediction", width="stretch"):
                X_processed, df_processed = DataProcessor.process_csv(
                    df, st.session_state.model_manager.get_scaler())
                preds, probs = st.session_state.model_manager.predict(
                    X_processed, selected_model)
                if preds is None:
                    st.error("Prediction failed.")
                else:
                    results = df.copy()
                    import numpy as np
                    results["prediction"] = np.where(
                        preds == 0, "SAFE", "FAILURE")
                    results["failure_probability_%"] = (probs * 100).round(2)
                    results["confidence_%"] = np.where(
                        preds == 0, ((1 - probs) *
                                     100).round(2), (probs * 100).round(2)
                    )
                    st.success("Predictions complete")
                    st.dataframe(results, width="stretch")
                    st.download_button(
                        "Download Results CSV",
                        data=results.to_csv(index=False),
                        file_name="predictions_results.csv",
                        mime="text/csv",
                        width="stretch",
                    )
        except Exception as e:
            st.error(f"CSV processing error: {e}")
