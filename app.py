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

# Real-Time Navigation
if st.button("Start Navigation"):
    st.success("Real-Time Navigation Activated 🗺️")

# Caregiver Alerts
if user_type == "Caregiver":
    if st.button("Send Alert to Caregiver"):
        st.warning("Caregiver Alert Sent! 🚨")

# SOS Alert System
if st.button("Trigger SOS Alert"):
    st.error("SOS Alert Sent! Emergency Assistance On the Way 🚑")
    
    # Define Navi Mumbai SOS radius area
    sos_location = [19.0330, 73.0297]  # Default to Kharghar, Navi Mumbai
    df = pd.DataFrame([{ "lat": sos_location[0], "lon": sos_location[1] }])
    
    # Display SOS radius map for Navi Mumbai
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=sos_location[0],
            longitude=sos_location[1],
            zoom=12,  # Adjusted zoom level to cover Navi Mumbai
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position="[lon, lat]",
                get_color="[255, 0, 0, 160]",
                get_radius=10000,  # Radius covering Navi Mumbai
            )
        ],
    ))

# Multilingual Support
language = st.selectbox("Select Language", ["English", "Spanish", "French", "German", "Mandarin"])
st.success(f"Language set to {language} 🌍")

# Vibration Feedback (Simulated)
if st.button("Test Vibration Feedback"):
    st.info("Vibration Feedback Activated 📳 (Simulated)")
