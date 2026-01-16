import streamlit as st
import matplotlib.pyplot as plt
import time

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart Irrigation & Water Budgeting",
    layout="wide"
)

st.title("🌱 Smart Irrigation & AI Assistant for Farmers")
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
        "irrigation_tip": "Irrigation needed only if rainfall is irregular."
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
st.sidebar.header("🌾 Farm Details")

location = st.sidebar.selectbox("📍 Location", list(RAINFALL_DATA.keys()))
season = st.sidebar.selectbox("🌦 Crop Season", ["Kharif", "Rabi"])
crop = st.sidebar.selectbox("🌱 Selected Crop", list(CROP_WATER_REQUIREMENT.keys()))
area = st.sidebar.number_input("📐 Farm Area (hectares)", min_value=0.1, value=1.0)
irrigation = st.sidebar.selectbox("💧 Irrigation Method", list(IRRIGATION_FACTOR.keys()))
groundwater = st.sidebar.selectbox("🚰 Groundwater Availability", list(GROUNDWATER_INDEX.keys()))
soil_moisture = st.sidebar.selectbox("🌍 Soil Moisture (Sensor Input)", ["Low", "Medium", "High"])

# ===============================
# TABS
# ===============================
tab1, tab2, tab3 = st.tabs(
    ["📊 Water Budget & Advisory", "🤖 AI Assistant", "🌾 Season Guidance"]
)

# ===============================
# TAB 1 – WATER BUDGET
# ===============================
with tab1:
    st.subheader("💧 Water Budget Summary")

    rainfall_mm = RAINFALL_DATA[location]
    rainfall_water = rainfall_mm * area * 10
    groundwater_water = rainfall_water * GROUNDWATER_INDEX[groundwater]
    total_available_water = rainfall_water + groundwater_water

    crop_wr = CROP_WATER_REQUIREMENT[crop]
    irrigation_efficiency = IRRIGATION_FACTOR[irrigation]
    base_demand = crop_wr * area * 10 * irrigation_efficiency

    moisture_factor = 0.6 if soil_moisture == "High" else 0.8 if soil_moisture == "Medium" else 1.0
    adjusted_demand = base_demand * moisture_factor
    water_balance = total_available_water - adjusted_demand

    col1, col2, col3 = st.columns(3)
    col1.metric("Available Water (m³)", round(total_available_water, 2))
    col2.metric("Crop Water Demand (m³)", round(adjusted_demand, 2))
    col3.metric("Water Balance (m³)", round(water_balance, 2))

    if water_balance > 2000:
        st.success("Status: WATER SURPLUS")
    elif water_balance >= 0:
        st.warning("Status: WATER BALANCED")
    else:
        st.error("Status: WATER DEFICIT")

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
        risk_level = "HIGH RISK"
        risk_msg = "🚨 High risk of crop failure due to water stress."
    elif water_balance < 2000:
        risk_level = "MEDIUM RISK"
        risk_msg = "⚠️ Moderate risk. Use efficient irrigation."
    else:
        risk_level = "LOW RISK"
        risk_msg = "✅ Water availability is sufficient."

    st.subheader("🌱 Smart Crop & Risk Advisory")
    st.write(f"**Recommended Crop:** {recommended_crop}")
    st.write(f"**Risk Level:** {risk_level}")
    st.write(risk_msg)

# ===============================
# TAB 2 – BILINGUAL KEYWORD AI
# ===============================
with tab2:
    st.subheader("🤖 AI Irrigation Assistant")
    st.write("Ask in **Hindi or English** (e.g., *water*, *paani*, *crop*, *fasal*, *risk*)")

    user_text = st.text_input("⌨️ Ask your question")

    def keyword_ai_response(text):
        t = text.lower()

        # Water / Irrigation
        if any(k in t for k in ["paani", "water", "irrigation"]):
            if soil_moisture == "High":
                return (
                    "Soil moisture is high. No irrigation needed now.\n\n"
                    "मिट्टी में नमी पर्याप्त है। अभी पानी देने की जरूरत नहीं।"
                )
            elif soil_moisture == "Medium":
                return (
                    "Soil moisture is moderate. Irrigate in 1–2 days.\n\n"
                    "मिट्टी में थोड़ी नमी है। 1–2 दिन में पानी दें।"
                )
            else:
                return (
                    "Soil is dry. Immediate irrigation required.\n\n"
                    "मिट्टी सूखी है। आज ही पानी देना जरूरी है।"
                )

        # Crop Recommendation
        elif any(k in t for k in ["crop", "fasal"]):
            return (
                f"Recommended crop based on current conditions is **{recommended_crop}**.\n\n"
                f"वर्तमान स्थिति में **{recommended_crop}** सबसे उपयुक्त फसल है।"
            )

        # Risk
        elif any(k in t for k in ["risk", "nuksan", "loss"]):
            return (
                f"Current system risk level is **{risk_level}**.\n\n"
                f"वर्तमान जोखिम स्तर **{risk_level}** है।"
            )

        # Soil Moisture
        elif any(k in t for k in ["moisture", "nami"]):
            return (
                f"Soil moisture level is **{soil_moisture}**.\n\n"
                f"मिट्टी की नमी का स्तर **{soil_moisture}** है।"
            )

        # Rainfall
        elif any(k in t for k in ["rain", "barish"]):
            return (
                f"Rainfall data for {location} is used for water estimation.\n\n"
                f"{location} के वर्षा डेटा के आधार पर पानी की गणना की जाती है।"
            )

        else:
            return (
                "Please ask about water, crop, risk, moisture, or rainfall.\n\n"
                "कृपया पानी, फसल, जोखिम, नमी या बारिश से संबंधित प्रश्न पूछें।"
            )

    if st.button("Get AI Advice"):
        with st.spinner("AI is analyzing..."):
            time.sleep(1)

        if user_text:
            response = keyword_ai_response(user_text)
        else:
            response = (
                "Please type a question.\n\n"
                "कृपया प्रश्न लिखें।"
            )

        st.success("🤖 AI Advisory")
        st.write(response)

# ===============================
# TAB 3 – SEASON GUIDANCE
# ===============================
with tab3:
    st.subheader(f"🌦 {season} Season – Farmer Guidance")
    info = SEASON_INFO[season]

    st.markdown(f"""
    **📅 Duration:** {info['months']}  
    **🌧 Rainfall:** {info['rain']}  
    **🌾 Suitable Crops:** {info['common_crops']}  
    **💡 Tip:** {info['irrigation_tip']}
    """)

    st.info("Season-based guidance helps farmers plan irrigation without technical complexity.")
