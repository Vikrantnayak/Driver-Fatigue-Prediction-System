# app.py
import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime
from model import train_model, predict_status
from utils import (
    create_gauge_chart, create_feature_radar, create_timeline_chart,
    get_risk_level, get_action_message
)

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Driver Fatigue Monitoring System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Load Custom CSS (robust to working directory)
# -----------------------------
_css_path = Path(__file__).parent / "style.css"
if _css_path.exists():
    st.markdown(f"<style>{_css_path.read_text()}</style>", unsafe_allow_html=True)

# -----------------------------
# Session State Initialization
# -----------------------------
if "driver_records" not in st.session_state:
    st.session_state.driver_records = pd.DataFrame(columns=[
        'Timestamp', 'Name', 'Sleep_Hours', 'Driving_Hours', 'Caffeine_Cups',
        'Rest_Breaks', 'Age', 'Stress_Level', 'Time_of_Day',
        'Fatigue_Score', 'Prediction', 'Confidence'
    ])

# -----------------------------
# Train Model (cached)
# -----------------------------
@st.cache_resource
def get_model():
    model, scaler, le_time = train_model()
    return model, scaler, le_time

model, scaler, le_time = get_model()

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    st.markdown("## 🚗 Navigation")
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "➕ Add Driver", "📈 Analytics", "📋 Records", "ℹ️ About"],
        label_visibility="collapsed"
    )
    st.markdown("---")

    st.markdown("### 📊 Quick Stats")
    total = len(st.session_state.driver_records)
    st.metric("Total Assessments", total)
    if total > 0:
        fatigued = (st.session_state.driver_records['Prediction'] == 'Fatigued').sum()
        alert = total - fatigued
        st.metric("Alert Drivers", alert)
        st.metric("Fatigued Drivers", fatigued)
        avg_score = st.session_state.driver_records['Fatigue_Score'].mean()
        st.metric("Avg Fatigue Score", f"{avg_score:.2f}")

# -----------------------------
# Dashboard Page
# -----------------------------
if page == "📊 Dashboard":
    st.header("📊 Dashboard Overview")

    if st.session_state.driver_records.empty:
        st.info("No assessments yet. Add a driver from the sidebar.")
    else:
        left, right = st.columns([2, 1])
        with left:
            st.subheader("Recent Assessments")
            recent = st.session_state.driver_records.tail(10).sort_values(by='Timestamp', ascending=False)
            st.dataframe(recent.reset_index(drop=True))

            timeline_fig = create_timeline_chart(st.session_state.driver_records)
            if timeline_fig:
                st.plotly_chart(timeline_fig, use_container_width=True)

        with right:
            st.subheader("Latest Driver Snapshot")
            last = st.session_state.driver_records.iloc[-1].to_dict()
            score = last['Fatigue_Score']
            pred = last['Prediction']
            conf = last['Confidence']

            st.metric("Driver", last['Name'])
            st.metric("Status", pred)
            st.metric("Confidence", f"{conf*100:.1f}%")

            st.plotly_chart(create_gauge_chart(score), use_container_width=True)
            st.plotly_chart(create_feature_radar(last), use_container_width=True)

            msg = get_action_message(score)
            if score < 3:
                st.success(msg)
            elif score < 5:
                st.warning(msg)
            else:
                st.error(msg)

# -----------------------------
# Add Driver Page
# -----------------------------
elif page == "➕ Add Driver":
    st.header("➕ Add Driver Assessment")

    with st.form("driver_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Driver Name", value="Driver 1")
            sleep = st.number_input("Sleep Hours (last 24h)", value=7.0, min_value=0.0, step=0.25)
            driving = st.number_input("Driving Hours (shift)", value=5.0, min_value=0.0, step=0.25)
            caffeine = st.number_input("Caffeine Cups", value=1.0, min_value=0.0, step=0.5)
        with col2:
            rest = st.number_input("Rest Breaks (minutes)", value=30.0, min_value=0.0, step=5.0)
            age = st.number_input("Age", value=35, min_value=0, step=1)
            stress = st.number_input("Stress Level (1 - 10)", value=4, min_value=1, max_value=10, step=1)
            tod = st.selectbox("Time of Day", ['Morning', 'Afternoon', 'Night'])

        submitted = st.form_submit_button("Assess Driver")

        if submitted:
            input_data = {
                'Name': name,
                'Sleep_Hours': sleep,
                'Driving_Hours': driving,
                'Caffeine_Cups': caffeine,
                'Rest_Breaks': rest,
                'Age': age,
                'Stress_Level': stress,
                'Time_of_Day': tod
            }

            pred, conf, score = predict_status(model, scaler, le_time, input_data)

            record = {
                **input_data,
                'Timestamp': datetime.now().isoformat(sep=' ', timespec='seconds'),
                'Fatigue_Score': score,
                'Prediction': pred,
                'Confidence': conf
            }

            st.session_state.driver_records = pd.concat(
                [st.session_state.driver_records, pd.DataFrame([record])],
                ignore_index=True
            )

            st.success(f"{name} is predicted as **{pred}** ({conf*100:.1f}% confidence)")

            st.subheader("🔍 Assessment Summary")
            st.metric("Fatigue Score", f"{score:.2f} ({get_risk_level(score)})")
            st.plotly_chart(create_gauge_chart(score), use_container_width=True)
            st.plotly_chart(create_feature_radar(input_data), use_container_width=True)

            msg = get_action_message(score)
            if score < 3:
                st.success(msg)
            elif score < 5:
                st.warning(msg)
            else:
                st.error(msg)

# (Questionnaire page removed as per request)

# -----------------------------
# Analytics Page
# -----------------------------
elif page == "📈 Analytics":
    st.header("📈 Analytics Dashboard")

    if st.session_state.driver_records.empty:
        st.info("No data available yet.")
    else:
        df = st.session_state.driver_records.copy()

        st.subheader("Fatigue Status Distribution")
        st.bar_chart(df['Prediction'].value_counts())

        st.subheader("Fatigue Score Trend")
        timeline_fig = create_timeline_chart(df)
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)

# -----------------------------
# Records Page
# -----------------------------
elif page == "📋 Records":
    st.header("📋 Saved Driver Records")

    if st.session_state.driver_records.empty:
        st.info("No records yet.")
    else:
        st.dataframe(st.session_state.driver_records)
        col1, col2, col3 = st.columns(3)

        with col1:
            csv = st.session_state.driver_records.to_csv(index=False)
            st.download_button("⬇️ Download CSV", csv, "driver_records.csv", "text/csv")

        with col2:
            if st.button("🗑️ Clear All Records"):
                st.session_state.driver_records = pd.DataFrame(columns=st.session_state.driver_records.columns)
                st.experimental_rerun()

        with col3:
            if st.button("Remove Last Entry"):
                st.session_state.driver_records = st.session_state.driver_records.iloc[:-1]
                st.experimental_rerun()

# -----------------------------
# About Page
# -----------------------------
elif page == "ℹ️ About":
    st.header("ℹ️ About the Project")
    st.markdown("""
    **Driver Fatigue Monitoring System**  
    A demo ML-powered web app for assessing driver fatigue levels using behavioral data.  
    - Built with **Python, Streamlit, Scikit-learn, and Plotly**
    - Uses a **Random Forest Classifier** trained on synthetic data  
    - Provides **interactive analytics** and real-time visual feedback  
    *Note:* This app is a **prototype**, not a certified safety device.
    """)
