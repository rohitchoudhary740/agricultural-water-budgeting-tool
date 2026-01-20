import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
import random

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart Irrigation & Water Budgeting",
    layout="wide"
)

st.title("Smart Irrigation & AI Assistant for Farmers")
st.caption(
    "Precision irrigation and water budgeting using government data "
    "and field-level sensing."
)

# ===============================
# LOAD GOVERNMENT DATA
# ===============================

# --- Rainfall (Government CSV) ---
rainfall_df = pd.read_csv("gov_rainfall_tn.csv")
RAINFALL_DATA = dict(
    zip(
        rainfall_df["District"],
        rainfall_df["Total_Actual_Rainfall_mm"]
    )
)

# --- Groundwater (Government CSV) ---
gw_df = pd.read_csv("gov_groundwater_tn.csv")

GW_MAP = {
    "Safe": 0.6,
    "Semi-critical": 0.4,
    "Critical": 0.2,
    "Over-exploited": 0.1
}

# ===============================
# STATIC AGRI DATA
# ===============================
CROP_WATER_REQUIREMENT = {
    "Rice": 1200,
    "Wheat": 450,
    "Soybean": 500,
    "Maize": 600
}

IRRIGATION_FACTOR = {
    "Flood": 1.0,
    "Sprinkler": 0.75,
    "Drip": 0.6
}

SEASON_INFO = {
    "Kharif": {
        "months": "June – October",
        "rain": "High rainfall",
        "common_crops": "Rice, Soybean, Maize",
        "irrigation_tip": "Irrigation required only if rainfall is irregular."
    },
    "Rabi": {
        "months": "October – March",
        "rain": "Low rainfall",
        "common_crops": "Wheat, Gram, Mustard",
        "irrigation_tip": "Regular irrigation required."
    }
}

# ===============================
# SIDEBAR INPUTS
# ===============================
st.sidebar.header("Farm Details")

location = st.sidebar.selectbox(
    "District (Government Data)",
    sorted(RAINFALL_DATA.keys())
)

season = st.sidebar.selectbox("Crop Season", ["Kharif", "Rabi"])
crop = st.sidebar.selectbox("Selected Crop", list(CROP_WATER_REQUIREMENT.keys()))
area = st.sidebar.number_input("Farm Area (hectares)", min_value=0.1, value=1.0)
irrigation = st.sidebar.selectbox("Irrigation Method", list(IRRIGATION_FACTOR.keys()))

# --- Groundwater from Govt CSV ---
gw_status = gw_df[gw_df["District"] == location]["Groundwater_Status"].values[0]
groundwater_factor = GW_MAP[gw_status]

st.sidebar.write(f"Groundwater Status (Govt): **{gw_status}**")

# --- Soil Moisture (Live / Manual) ---
soil_mode = st.sidebar.radio(
    "Soil Moisture Source",
    ["Live Sensor (Simulated)", "Manual"]
)

if soil_mode == "Manual":
    soil_moisture = st.sidebar.selectbox(
        "Soil Moisture Level",
        ["Low", "Medium", "High"]
    )
else:
    if "sensor_value" not in st.session_state:
        st.session_state.sensor_value = "Medium"

    if st.sidebar.button("Fetch Sensor Reading"):
        st.session_state.sensor_value = random.choice(
            ["Low", "Medium", "High"]
        )

    soil_moisture = st.session_state.sensor_value
    st.sidebar.write(f"Live Soil Moisture: **{soil_moisture}**")

# ===============================
# TABS
# ===============================
tab1, tab2, tab3 = st.tabs(
    ["Water Budget", "AI Assistant", "Season Guidance"]
)

# ===============================
# TAB 1 – WATER BUDGET
# ===============================
with tab1:
    rainfall_mm = RAINFALL_DATA[location]

    rainfall_water = rainfall_mm * area * 10
    groundwater_water = rainfall_water * groundwater_factor
    total_available_water = rainfall_water + groundwater_water

    crop_wr = CROP_WATER_REQUIREMENT[crop]
    base_demand = crop_wr * area * 10 * IRRIGATION_FACTOR[irrigation]

    moisture_factor = (
        0.6 if soil_moisture == "High"
        else 0.8 if soil_moisture == "Medium"
        else 1.0
    )

    adjusted_demand = base_demand * moisture_factor
    water_balance = total_available_water - adjusted_demand

    c1, c2, c3 = st.columns(3)
    c1.metric("Available Water (m³)", round(total_available_water, 2))
    c2.metric("Crop Water Demand (m³)", round(adjusted_demand, 2))
    c3.metric("Water Balance (m³)", round(water_balance, 2))

    fig, ax = plt.subplots()
    ax.bar(
        ["Available Water", "Crop Demand"],
        [total_available_water, adjusted_demand]
    )
    ax.set_ylabel("Water (m³)")
    st.pyplot(fig)

    def recommend_crop(total_water, area):
        wph = total_water / area
        if wph >= 10000:
            return "Rice"
        elif wph >= 6000:
            return "Maize"
        elif wph >= 5000:
            return "Soybean"
        else:
            return "Wheat"

    recommended_crop = recommend_crop(total_available_water, area)

    if water_balance < 0:
        risk_level = "High"
    elif water_balance < 2000:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    st.subheader("Crop & Risk Advisory")
    st.write(f"Recommended Crop: **{recommended_crop}**")
    st.write(f"Risk Level: **{risk_level}**")

    st.markdown("### Data Sources")
    st.write("Rainfall: Government district-wise rainfall dataset")
    st.write("Groundwater: CGWB / India-WRIS classification")
    st.write("Soil Moisture: Field sensor (live simulation)")

# ===============================
# TAB 2 – AI ASSISTANT
# ===============================
with tab2:
    st.subheader("AI Irrigation Assistant")

    language = st.selectbox("Response Language", ["English", "Hindi"])

    user_text = st.text_input("Type your question (optional)")
    audio = st.audio_input("Speak your question")

    def irrigation_advice(lang):
        if soil_moisture == "High":
            return (
                "Soil moisture is sufficient. Irrigation is not required now."
                if lang == "English"
                else "मिट्टी में पर्याप्त नमी है। अभी सिंचाई की आवश्यकता नहीं है।"
            )
        elif soil_moisture == "Medium":
            return (
                "Soil moisture is moderate. Irrigation can be done in 1–2 days."
                if lang == "English"
                else "मिट्टी में मध्यम नमी है। 1–2 दिन में सिंचाई करें।"
            )
        else:
            return (
                "Soil is dry. Immediate irrigation is required."
                if lang == "English"
                else "मिट्टी सूखी है। तुरंत सिंचाई आवश्यक है।"
            )

    if st.button("Get AI Advice"):
        with st.spinner("Analyzing field conditions..."):
            time.sleep(1)

        if user_text or audio is not None:
            response = irrigation_advice(language)
        else:
            response = (
                "Please provide text or voice input."
                if language == "English"
                else "कृपया टेक्स्ट या वॉइस इनपुट दें।"
            )

        st.write(response)

# ===============================
# TAB 3 – SEASON GUIDANCE
# ===============================
with tab3:
    info = SEASON_INFO[season]
    st.subheader(f"{season} Season Guidance")

    st.markdown(f"""
    Duration: {info['months']}  
    Rainfall Pattern: {info['rain']}  
    Common Crops: {info['common_crops']}  
    Irrigation Tip: {info['irrigation_tip']}
    """)
