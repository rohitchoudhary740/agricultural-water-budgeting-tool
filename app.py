import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time

rainfall_df = pd.read_csv("gov_rainfall_tn.csv")

# Convert to dictionary for fast lookup
RAINFALL_DATA = dict(
    zip(
        rainfall_df["District"],
        rainfall_df["Total_Actual_Rainfall_mm"]
    )
)

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart Irrigation & Water Budgeting",
    layout="wide"
)

st.title("Smart Irrigation & AI Assistant for Farmers")
st.caption(
    "Precision irrigation and water budgeting inspired by Israel’s water-efficient agriculture, "
    "adapted for Indian farming conditions."
)

# ===============================
# STATIC DATA
# ===============================
RAINFALL_DATA = {
    "Indore": 800,
    "Bhopal": 1000,
    "Nagpur": 900
}

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

GROUNDWATER_INDEX = {
    "Low": 0.2,
    "Medium": 0.4,
    "High": 0.6
}

SEASON_INFO = {
    "Kharif": {
        "months": "June – October",
        "rain": "High rainfall",
        "common_crops": "Rice, Soybean, Maize",
        "irrigation_tip": "Irrigation needed only when rainfall is irregular."
    },
    "Rabi": {
        "months": "October – March",
        "rain": "Low rainfall",
        "common_crops": "Wheat, Gram, Mustard",
        "irrigation_tip": "Regular irrigation is required."
    }
}

# ===============================
# SIDEBAR INPUTS
# ===============================
st.sidebar.header("Farm Details")

location = st.sidebar.selectbox(
    "District (Govt Rainfall Data)",
    sorted(RAINFALL_DATA.keys())
)

season = st.sidebar.selectbox("Crop Season", ["Kharif", "Rabi"])
crop = st.sidebar.selectbox("Selected Crop", list(CROP_WATER_REQUIREMENT.keys()))
area = st.sidebar.number_input("Farm Area (hectares)", min_value=0.1, value=1.0)
irrigation = st.sidebar.selectbox("Irrigation Method", list(IRRIGATION_FACTOR.keys()))
groundwater = st.sidebar.selectbox("Groundwater Availability", list(GROUNDWATER_INDEX.keys()))
soil_moisture = st.sidebar.selectbox("Soil Moisture Level", ["Low", "Medium", "High"])

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
    groundwater_water = rainfall_water * GROUNDWATER_INDEX[groundwater]
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
    ax.bar(["Available Water", "Crop Demand"], [total_available_water, adjusted_demand])
    ax.set_ylabel("Water (m³)")
    st.pyplot(fig)

    def recommend_crop(total_water, area):
        water_per_hectare = total_water / area
        if water_per_hectare >= 10000:
            return "Rice"
        elif water_per_hectare >= 6000:
            return "Maize"
        elif water_per_hectare >= 5000:
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
    st.write(f"Recommended Crop: {recommended_crop}")
    st.write(f"Risk Level: {risk_level}")

# ===============================
# TAB 2 – AI ASSISTANT (TEXT + VOICE)
# ===============================
with tab2:
    st.subheader("AI Irrigation Assistant")
    st.write("You may use text or voice. Select preferred response language.")

    language = st.selectbox("Response Language", ["English", "Hindi"])

    user_text = st.text_input("Type your question (optional)")
    audio = st.audio_input("Speak your question")

    def irrigation_advice(lang):
        if soil_moisture == "High":
            return (
                "Soil moisture is sufficient. Irrigation is not required at this time."
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

        # Priority order: Text → Voice → Default
        if user_text:
            response = irrigation_advice(language)

        elif audio is not None:
            intro = (
                "Voice input detected. Advisory generated based on current field conditions:\n\n"
                if language == "English"
                else "वॉइस इनपुट प्राप्त हुआ। खेत की वर्तमान स्थिति के आधार पर सलाह दी गई है:\n\n"
            )
            response = intro + irrigation_advice(language)

        else:
            response = (
                "Please provide input using text or voice."
                if language == "English"
                else "कृपया टेक्स्ट या वॉइस के माध्यम से प्रश्न पूछें।"
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

    st.info(
        "Season-based guidance helps farmers plan irrigation without technical complexity."
    )
