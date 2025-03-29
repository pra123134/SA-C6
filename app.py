import streamlit as st
import google.generativeai as genai
import pandas as pd
import pydeck as pdk

# Configure Streamlit API Key securely
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

# App title and description
st.title("Prototype App for Vulnerable Groups")
st.markdown("""
This app provides real-time navigation, caregiver alerts, and SOS assistance for vulnerable groups, including children, the elderly, and individuals with cognitive impairments.
""")

# User Authentication
st.sidebar.header("User Authentication")
user_type = st.sidebar.selectbox("Select User Type", ["Caregiver", "Vulnerable Individual", "Rescuer"])

# Real-Time Navigation and SOS Tracking
def get_navigation_map():
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=19.0330,
            longitude=73.0297,
            zoom=11,  # Adjusted zoom level to cover entire Navi Mumbai
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=pd.DataFrame([{ "lat": 19.0330, "lon": 73.0297 }]),
                get_position="[lon, lat]",
                get_color="[0, 0, 255, 160]",  # Blue color for navigation point
                get_radius=100,
            )
        ]
    )

if st.button("Start Navigation"):
    st.success("Real-Time Navigation Activated 🗺️")
    st.pydeck_chart(get_navigation_map())

# Caregiver Alerts
if user_type == "Caregiver":
    if st.button("Send Alert to Caregiver"):
        st.warning("Caregiver Alert Sent! 🚨")

# SOS Alert System with Navigation Assistance
if st.button("Trigger SOS Alert"):
    st.error("SOS Alert Sent! Emergency Assistance On the Way 🚑")
    st.pydeck_chart(get_navigation_map())

# Multilingual Support
language = st.selectbox("Select Language", ["English", "Spanish", "French", "German", "Mandarin"])
st.success(f"Language set to {language} 🌍")

# Vibration Feedback (Simulated)
if st.button("Test Vibration Feedback"):
    st.info("Vibration Feedback Activated 📳 (Simulated)")
