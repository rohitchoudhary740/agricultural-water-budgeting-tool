import streamlit as st
import matplotlib.pyplot as plt
import time
import re

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

location = st.sidebar.selectbox("Location", list(RAINFALL_DATA.keys()))
season = st.sidebar.selectbox("Crop Season", ["Kharif", "Rabi"])
crop = st.sidebar.selectbox("Selected Crop", list(CROP_WATER_REQUIREMENT.keys()))
area = st.sidebar.number_input("Farm Area (hectares)", min_value=0.1, value=1.0)
irrigation = st.sidebar.selectbox("Irrigation Method", list(IRRIGATION_FACTOR.keys()))
groundwater = st.sidebar.selectbox("Groundwater Availability", list(GROUNDWATER_INDEX.keys()))
soil_moisture = st.sidebar.selectbox("Soil Moisture", ["Low", "Medium", "High"])

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

    moisture_factor = 0.6 if soil_moisture == "High" else 0.8 if soil_moisture == "Medium" else 1.0
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
    st.write(f"Recommended Crop: {recommended_crop}")
    st.write(f"Risk Level: {risk_level}")

# ===============================
# TAB 2 – CLEAN BILINGUAL AI
# ===============================
with tab2:
    st.subheader("AI Irrigation Assistant")
    st.write("Ask using text or voice. English and Hindi are supported.")

    user_text = st.text_input("Type your question")
    audio = st.audio_input("Speak your question")

    def is_hindi(text):
        return bool(re.search(r'[\u0900-\u097F]', text))

    def ai_response(text, lang):
        t = text.lower()

        if any(k in t for k in ["water", "irrigation", "paani"]):
            if soil_moisture == "High":
                return (
                    "Soil moisture is sufficient. Irrigation is not required now."
                    if lang == "en"
                    else "मिट्टी में पर्याप्त नमी है। अभी सिंचाई की आवश्यकता नहीं है।"
                )
            elif soil_moisture == "Medium":
                return (
                    "Soil moisture is moderate. Irrigate in 1–2 days."
                    if lang == "en"
                    else "मिट्टी में मध्यम नमी है। 1–2 दिन में सिंचाई करें।"
                )
            else:
                return (
                    "Soil is dry. Immediate irrigation is required."
                    if lang == "en"
                    else "मिट्टी सूखी है। तुरंत सिंचाई आवश्यक है।"
                )

        if any(k in t for k in ["crop", "fasal"]):
            return (
                f"The recommended crop is {recommended_crop}."
                if lang == "en"
                else f"अनुशंसित फसल {recommended_crop} है।"
            )

        if any(k in t for k in ["risk", "nuksan"]):
            return (
                f"Current agricultural risk level is {risk_level}."
                if lang == "en"
                else f"वर्तमान कृषि जोखिम स्तर {risk_level} है।"
            )

        return (
            "Please ask about water, crop, or risk."
            if lang == "en"
            else "कृपया पानी, फसल या जोखिम से संबंधित प्रश्न पूछें।"
        )

    if st.button("Get Advice"):
        with st.spinner("Processing request..."):
            time.sleep(1)

        if user_text:
            lang = "hi" if is_hindi(user_text) else "en"
            response = ai_response(user_text, lang)

        elif audio is not None:
            response = (
                "Voice input received. Advisory generated based on current field parameters."
                if soil_moisture != "Low"
                else "Voice input received. Field conditions indicate irrigation requirement."
            )

        else:
            response = "Please provide input using text or voice."

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
