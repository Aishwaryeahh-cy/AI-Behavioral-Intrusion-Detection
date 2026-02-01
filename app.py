import streamlit as st
import pandas as pd
import joblib
import numpy as np
import datetime
import random

# 1. Page Configuration
st.set_page_config(
    page_title="Behavioral IDS | Academic Prototype",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Dashboard Styling (SOC Style)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    h1, h2, h3 { color: #00FF41 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 1px;}
    .status-panel { border: 1px solid #333; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 25px; background-color: #1A1C23; font-family: monospace; }
    .risk-score { font-size: 54px; font-weight: 800; text-align: center; margin-bottom: -10px; }
    .log-container { font-family: 'Consolas', monospace; background-color: #050505; color: #00FF41; padding: 20px; border-radius: 8px; font-size: 13px; line-height: 1.5; border: 1px solid #00FF4133; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #0E1117; color: #555; text-align: center; padding: 10px; font-size: 12px; border-top: 1px solid #333; }
    
    /* Input interaction colors */
    .stNumberInput input, .stSelectbox div, .stRadio div {
        color: white !important;
    }
    
    .caption-text { 
        font-size: 12px; 
        color: #888; 
        margin-top: -15px; 
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Model Loading
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('login_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler, True
    except:
        return None, None, False

model, scaler, assets_ready = load_assets()

# 4. App Header
st.title("🛡️ AI-Based Behavioral Intrusion Detection System")
st.markdown("**Academic research prototype for analyzing user behavior patterns to identify security anomalies.**")

st.markdown("""
<div class="status-panel">
    <span style="color: #666;">SYSTEM STATUS:</span> <span style="color: #00FF41;">ACTIVE_SIMULATION</span> | 
    <span style="color: #666;">USER INTERFACE:</span> <span style="color: #00AAFF;">FULLY_INTERACTIVE</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 5. UI Layout
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📡 Behavioral Telemetry")
    st.markdown("Manually input login metrics for the simulation.")
    
    # Fully editable number inputs with placeholders
    typing_speed_in = st.number_input(
        "Average Typing Speed (ms/key)", 
        min_value=0, 
        max_value=1000, 
        value=None, 
        placeholder="e.g. 215",
        key="typing_in"
    )
    st.markdown('<p class="caption-text"><i>In production, this data is captured automatically via keystroke sensors.</i></p>', unsafe_allow_html=True)
    
    login_hour_in = st.number_input(
        "Login Hour Profile (0-23)", 
        min_value=0, 
        max_value=23, 
        value=None, 
        placeholder="e.g. 14",
        key="hour_in"
    )
    st.markdown('<p class="caption-text"><i>In production, this data is captured automatically from system timestamps.</i></p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        device_status_in = st.radio(
            "Hardware State", 
            ("Known Device", "Unregistered Device"),
            index=None,
            key="device_radio"
        )
        st.markdown('<p class="caption-text"><i>In production, device fingerprints are captured automatically.</i></p>', unsafe_allow_html=True)
    with c2:
        geo_status_in = st.radio(
            "Geographical State", 
            ("Usual Location", "New Location"),
            index=None,
            key="geo_radio"
        )
        st.markdown('<p class="caption-text"><i>In production, IP-based geolocation is captured automatically.</i></p>', unsafe_allow_html=True)

with col2:
    st.subheader("🔍 Threat Assessment Engine")
    
    # Execution Button
    if st.button("🚀 EXECUTE BEHAVIORAL ANALYSIS", use_container_width=True):
        if assets_ready:
            # DYNAMIC DEFAULTING LOGIC (Apply only on click)
            used_defaults = []
            
            # Typing Speed: Default to normal range (220ms)
            if typing_speed_in is not None:
                final_typing = typing_speed_in
            else:
                final_typing = 220
                used_defaults.append("Typing Speed (220ms)")
                
            # Hour: Default to mid-day (12:00)
            if login_hour_in is not None:
                final_hour = login_hour_in
            else:
                final_hour = 12
                used_defaults.append("Login Hour (12:00)")
                
            # Device: Default to Verified
            if device_status_in is not None:
                final_device = 1 if device_status_in == "Unregistered Device" else 0
            else:
                final_device = 0
                used_defaults.append("Hardware Profile (Known)")
                
            # Geo: Default to Baseline
            if geo_status_in is not None:
                final_geo = 1 if geo_status_in == "Irregular Location" else 0
            else:
                final_geo = 0
                used_defaults.append("Geo-Location (Baseline)")

            # Warning for users if they didn't fill everything
            if used_defaults:
                st.warning(f"⚠️ **Incomplete telemetry input.** Applying standard baselines for: {', '.join(used_defaults)}")

            # 1. Calculation (Heuristic Logic)
            risk_score = 0
            factors = []
            
            if final_typing < 120 or final_typing > 400:
                risk_score += 35
                factors.append("CRITICAL: Significant deviation in keyboard cadence.")
            elif final_typing < 180 or final_typing > 260:
                risk_score += 15
                factors.append("NOTICE: Non-baseline behavioral typing detected.")
                
            if final_device == 1:
                risk_score += 25
                factors.append("ALERT: Access from unregistered hardware fingerprint.")
            if final_geo == 1:
                risk_score += 25
                factors.append("ALERT: Geographical ingress mismatch.")
            if 0 <= final_hour <= 5:
                risk_score += 15
                factors.append("CAUTION: Access attempt during high-risk off-hours.")
            
            risk_score = min(risk_score, 100)
            
            # Risk Gradation
            if risk_score >= 70: color, label, status, icon = "#FF4B4B", "CRITICAL", "POTENTIAL INTRUSION", "🚨"
            elif risk_score >= 40: color, label, status, icon = "#FFA421", "MODERATE", "BEHAVIORAL ANOMALY", "⚠️"
            else: color, label, status, icon = "#00C851", "LOW", "AUTHORIZED ACCESS", "✅"
            
            # Display Dashboard Metrics
            st.markdown(f"""
                <div style="text-align: center;">
                    <p style="color: {color}; font-weight: bold; margin-bottom: 5px; letter-spacing: 2px;">RISK PROBABILITY: {label}</p>
                    <div class="risk-score" style="color: {color};">{risk_score}%</div>
                    <h2 style="color: {color} !important; border-bottom: none; margin-top: 10px;">{icon} {status}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.progress(risk_score / 100)
            
            # Security Logs Output
            st.write("")
            ts = datetime.datetime.now().strftime("%Y-%m-%d %T")
            log_str = f"[{ts}] [TELEMETRY_LOG] Speed: {final_typing}ms | Hour: {final_hour} | Device: {'UNREG' if final_device else 'REG'} | Geo: {'ALT' if final_geo else 'BASE'}\n[{ts}] [AI_ASSESS] Result: {risk_score}%\n[{ts}] [AUDIT_TRAIL] Verdict: {status}"
            st.markdown(f'<div class="log-container"><code>{log_str.replace("\n", "<br>")}</code></div>', unsafe_allow_html=True)

            with st.expander("📝 Detailed Behavioral Analysis Breakdown", expanded=True):
                if factors:
                    for f in factors: st.markdown(f"- {f}")
                else:
                    st.success("Session behavior is fully consistent with authorized baseline parameters.")
        else:
            st.error("Engine failure: AI model baseline ('login_model.pkl') not detected. Ensure training is complete.")
    else:
        st.info("System Ready. Complete telemetry inputs and click 'Execute Analysis' to begin.")

# 6. Global Footer
st.markdown("""
<div class="footer">
    Academic Behavioral IDS Prototype | Educational prototype for cybersecurity learning | Version 1.0 (2026 Build)
</div>
""", unsafe_allow_html=True)
