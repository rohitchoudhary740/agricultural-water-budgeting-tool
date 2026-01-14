import streamlit as st
import matplotlib.pyplot as plt
import random
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

# ===============================
# SEASON EXPLANATION (NEW)
# ===============================
SEASON_INFO = {
    "Kharif": {
        "months": "June – October",
        "rain": "High rainfall",
        "common_crops": "Rice, Soybean, Maize, Cotton",
        "irrigation_tip": "Irrigation mostly needed only when rainfall is irregular."
    },
    "Rabi": {
        "months": "October – March",
        "rain": "Low rainfall",
        "common_crops": "Wheat, Gram, Mustard",
        "irrigation_tip": "Regular irrigation required as rainfall is limited."
    }
}

# ===============================
# SIDEBAR INPUTS
# ===============================
st.sidebar.header("🌾 Farm Details")

location = st.sidebar.selectbox("📍 Location", list(RAINFALL_DATA.keys()))
season = st.sidebar.selectbox("🌦 Crop Season", ["Kharif", "Rabi"])
crop = st.sidebar.selectbox("🌱 Crop Type", list(CROP_WATER_REQUIREMENT.keys()))

area = st.sidebar.number_input(
    "📐 Farm Area (hectares)",
    min_value=0.1,
    value=1.0
)

irrigation = st.sidebar.selectbox(
    "💧 Irrigation Method",
    list(IRRIGATION_FACTOR.keys())
)

groundwater = st.sidebar.selectbox(
    "🚰 Groundwater Availability",
    list(GROUNDWATER_INDEX.keys())
)

soil_moisture = st.sidebar.selectbox(
    "🌍 Soil Moisture (Sensor Input)",
    ["Low", "Medium", "High"]
)

# ===============================
# TABS (MODERN LAYOUT)
# ===============================
tab1, tab2, tab3 = st.tabs(
    ["📊 Water Budget & Advisory", "🤖 AI Assistant", "🌾 Season Guidance"]
)

# =====================================================
# TAB 1: WATER BUDGET
# =====================================================
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

    if water_balance > 0:
        st.success("Status: WATER SURPLUS")
    elif water_balance == 0:
        st.warning("Status: WATER BALANCED")
    else:
        st.error("Status: WATER DEFICIT")

    st.subheader("📊 Water Availability vs Demand")
    fig, ax = plt.subplots()
    ax.bar(
        ["Available Water", "Precision Crop Demand"],
        [total_available_water, adjusted_demand]
    )
    ax.set_ylabel("Water (m³)")
    st.pyplot(fig)

# =====================================================
# TAB 2: AI ASSISTANT
# =====================================================
with tab2:
    st.subheader("🤖 AI Irrigation Assistant")

    st.write("Ask by typing or speaking. Example: *Aaj paani dena chahiye?*")

    user_text = st.text_input("⌨️ Type your question (optional)")
    audio = st.audio_input("🎤 Speak your question")

    if st.button("Get AI Advice"):
        with st.spinner("AI Assistant is analyzing field conditions..."):
            time.sleep(1)

        if soil_moisture == "High":
            response = "Mitti mein nami kaafi hai. Abhi paani dene ki zarurat nahi hai."
        elif soil_moisture == "Medium":
            response = "Mitti mein thodi nami hai. 1–2 din mein paani dena behtar rahega."
        else:
            response = "Mitti sookhi hai. Aaj hi paani dena zaruri hai."

        st.success("🤖 AI Assistant Advice")
        st.write(response)

        st.caption(
            "Voice-based interaction helps farmers who are not comfortable reading data or numbers."
        )

# =====================================================
# TAB 3: SEASON GUIDANCE (NEW & IMPORTANT)
# =====================================================
with tab3:
    st.subheader(f"🌦 {season} Season – Farmer Guidance")

    info = SEASON_INFO[season]

    st.markdown(f"""
    **📅 Season Duration:** {info['months']}  
    **🌧 Rainfall Pattern:** {info['rain']}  
    **🌾 Common Crops:** {info['common_crops']}  
    **💡 Irrigation Tip:** {info['irrigation_tip']}
    """)

    st.info(
        "This seasonal guidance helps farmers understand irrigation needs "
        "based on crop season rather than technical terms."
    )

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption(
    "Demonstration prototype for hackathon use. "
    "Sensor data is simulated and recommendations are advisory in nature."
)
