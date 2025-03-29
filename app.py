import streamlit as st
import google.generativeai as genai
import folium
from streamlit_folium import folium_static

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

# Resource Mapping
if st.button("Show Nearby Safe Locations"):
    response = genai.generate_content("Find nearest safe locations for a vulnerable individual.")
    st.write(response)

# SOS Alert System with Map
if st.button("Trigger SOS Alert"):
    st.error("SOS Alert Sent! Emergency Assistance On the Way 🚑")
    
    # Display SOS location on map
    sos_location = [37.7749, -122.4194]  # Example coordinates (San Francisco)
    sos_map = folium.Map(location=sos_location, zoom_start=14)
    folium.Marker(sos_location, popup="SOS Location", icon=folium.Icon(color="red")).add_to(sos_map)
    folium_static(sos_map)

# Multilingual Support
language = st.selectbox("Select Language", ["English", "Spanish", "French", "German", "Mandarin"])
st.success(f"Language set to {language} 🌍")

# Vibration Feedback (Simulated)
if st.button("Test Vibration Feedback"):
    st.info("Vibration Feedback Activated 📳 (Simulated)")
