from config import FEATURE_RANGES, COLORS
from components.gauge_chart import display_failure_percentage
from components.status_badge import status_with_confidence
from utils.data_processor import DataProcessor
import streamlit as st
from utils.styles import apply_styles
from models.model_manager import ModelManager

st.set_page_config(page_title="Maintenance Prédictive IoT",
                   page_icon="🛠️", layout="wide")
apply_styles()

if "model_manager" not in st.session_state:
    st.session_state.model_manager = ModelManager()

st.title("🔧 Assistant de maintenance prédictive")
st.caption("Interface de diagnostic intelligent (Modèle : Arbre de Décision)")

# Simplified Sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px 0;">
        <div style="font-size: 20px; font-weight: 700;">⚡ Assistant IoT</div>
        <div style="font-size: 12px; opacity: 0.7;">Mode: Arbre de Décision</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("✅ Modèle Actif : Arbre de Décision")

    st.divider()
    st.markdown("### 💡 Plages de fonctionnement")
    st.markdown("- Air Temp: 295.3–304.5 K\n- Process Temp: 305.7–313.8 K\n- RPM: 1168–2886\n- Torque: 3.8–76.6 Nm\n- Tool Wear: 0–253 min")
    st.divider()
    st.markdown("### 📄 Colonnes CSV")
    st.code("air_temperature_k, process_temperature_k, rotational_speed_rpm, torque_nm, tool_wear_min")

tab_manual, tab_csv = st.tabs(["Saisie manuelle", "Import CSV"])

# --- MANUAL PREDICTION ---
with tab_manual:
    st.subheader("Données équipement")
    col1, col2, col3 = st.columns(3)
    with col1:
        air_temperature_k = st.number_input(
            "Air Temperature (K)", 295.3, 304.5, 299.9, 0.1)
    with col2:
        process_temperature_k = st.number_input(
            "Process Temperature (K)", 305.7, 313.8, 309.7, 0.1)
        rotational_speed_rpm = st.number_input(
            "Rotational Speed (RPM)", 1168, 2886, 2027, 10)
    with col3:
        torque_nm = st.number_input("Torque (N·m)", 3.8, 76.6, 40.2, 0.1)
        tool_wear_min = st.number_input("Tool Wear (min)", 0, 253, 126, 1)

    input_data = {
        "air_temperature_k": air_temperature_k,
        "process_temperature_k": process_temperature_k,
        "rotational_speed_rpm": rotational_speed_rpm,
        "torque_nm": torque_nm,
        "tool_wear_min": tool_wear_min,
    }

    if st.button("Prédire", use_container_width=True):
        valid, msg = DataProcessor.validate_input(input_data)
        if not valid:
            st.error(f"Erreur : {msg}")
        else:
            with st.spinner("Analyse par Arbre de Décision..."):
                X_scaled = DataProcessor.prepare_single_input(
                    input_data, st.session_state.model_manager.get_scaler())
                preds, probs = st.session_state.model_manager.predict(X_scaled)

                if preds is not None:
                    is_safe = preds[0] == 0
                    fail_prob = float(probs[0])
                    # Logic: If Decision Tree says Safe, confidence is (1-prob). If Fail, confidence is prob.
                    conf_pct = (100.0 * (1 - fail_prob)
                                ) if is_safe else (100.0 * fail_prob)

                    status_with_confidence(is_safe, conf_pct)
                    display_failure_percentage(fail_prob)

# --- CSV BATCH ---
with tab_csv:
    st.subheader("Prédiction par lot")
    uploaded = st.file_uploader("Importer CSV", type=["csv"])
    if uploaded:
        import pandas as pd
        df = pd.read_csv(uploaded)
        st.dataframe(df.head(), use_container_width=True)

        if st.button("Lancer l'analyse", use_container_width=True):
            with st.spinner("Traitement..."):
                X_proc, _ = DataProcessor.process_csv(
                    df, st.session_state.model_manager.get_scaler())
                preds, probs = st.session_state.model_manager.predict(X_proc)

                if preds is not None:
                    res = df.copy()
                    import numpy as np

                    # --- FRENCH COLUMN NAMES FOR CONSISTENCY ---
                    res["Statut_Predit"] = np.where(
                        preds == 0, "SAFE", "FAILURE")

                    # This matches the "Probabilité de défaillance" seen in Manual Mode
                    res["Probabilité_Défaillance_%"] = (probs * 100).round(2)

                    # Renaming confidence to French as well
                    res["Indice_Confiance_%"] = np.where(
                        preds == 0, ((1 - probs) * 100).round(2), (probs * 100).round(2))

                    st.success("Terminé !")
                    st.dataframe(res, use_container_width=True)

                    csv_data = res.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger les résultats",
                        data=csv_data,
                        file_name="resultats_predictions.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
