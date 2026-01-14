import streamlit as st
import matplotlib.pyplot as plt

# ===============================
# STATIC DATA (EMBEDDED)
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
# PAGE SETUP
# ===============================

st.set_page_config(
    page_title="Agricultural Water Budgeting Tool",
    layout="wide"
)

st.title("🌾 Agricultural Efficiency – Precision Irrigation Tool")

st.caption(
    "Inspired by **Israel’s precision irrigation and water-efficient agriculture practices**, "
    "adapted for scalable deployment in India."
)

st.write(
    "This decision-support system recommends the **right amount of water at the right time** "
    "using water budgeting, simulated sensor inputs, and circular water-use principles."
)

# ===============================
# SIDEBAR – IMPLEMENTATION STATUS
# ===============================

st.sidebar.success("🔄 Current Mode: Phase 1 – Decision Support (Sensor Simulated)")
st.sidebar.caption(
    "Phase 2: IoT Sensor Integration\n\n"
    "Phase 3: Village / Regional Water Planning"
)

# ===============================
# SIDEBAR INPUTS
# ===============================

st.sidebar.header("🌱 Field & Sensor Inputs")

location = st.sidebar.selectbox("Location", list(RAINFALL_DATA.keys()))
crop = st.sidebar.selectbox("Crop Type", list(CROP_WATER_REQUIREMENT.keys()))
season = st.sidebar.selectbox("Season", ["Kharif", "Rabi"])

area = st.sidebar.number_input(
    "Farm Area (hectares)",
    min_value=0.1,
    value=1.0
)

irrigation = st.sidebar.selectbox(
    "Irrigation Method",
    list(IRRIGATION_FACTOR.keys())
)

groundwater = st.sidebar.selectbox(
    "Groundwater Availability",
    list(GROUNDWATER_INDEX.keys())
)

soil_moisture = st.sidebar.selectbox(
    "Soil Moisture Level (Sensor Input)",
    ["Low", "Medium", "High"]
)

# ===============================
# WATER AVAILABILITY
# ===============================

rainfall_mm = RAINFALL_DATA[location]
rainfall_water = rainfall_mm * area * 10
groundwater_water = rainfall_water * GROUNDWATER_INDEX[groundwater]

total_available_water = rainfall_water + groundwater_water

# ===============================
# CROP WATER DEMAND
# ===============================

crop_wr = CROP_WATER_REQUIREMENT[crop]
irrigation_efficiency = IRRIGATION_FACTOR[irrigation]

base_crop_demand = crop_wr * area * 10 * irrigation_efficiency

# ===============================
# SENSOR-BASED ADJUSTMENT
# ===============================

if soil_moisture == "High":
    moisture_factor = 0.6
elif soil_moisture == "Medium":
    moisture_factor = 0.8
else:
    moisture_factor = 1.0

adjusted_crop_demand = base_crop_demand * moisture_factor

# ===============================
# WATER BUDGET
# ===============================

water_balance = total_available_water - adjusted_crop_demand

if water_balance > 0:
    status = "SURPLUS"
elif water_balance == 0:
    status = "BALANCED"
else:
    status = "DEFICIT"

# ===============================
# DISPLAY METRICS
# ===============================

st.subheader("💧 Water Budget Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Available Water (m³)", round(total_available_water, 2))
col2.metric("Crop Water Demand (m³)", round(adjusted_crop_demand, 2))
col3.metric("Water Balance (m³)", round(water_balance, 2))

if status == "SURPLUS":
    st.success("Status: WATER SURPLUS")
elif status == "BALANCED":
    st.warning("Status: WATER BALANCED")
else:
    st.error("Status: WATER DEFICIT")

# ===============================
# PRECISION IRRIGATION ADVISORY
# ===============================

st.subheader("⏱ Precision Irrigation Advisory (Israel-Inspired)")

if soil_moisture == "Low":
    timing_msg = "Immediate irrigation recommended to prevent crop stress."
elif soil_moisture == "Medium":
    timing_msg = "Irrigate within the next 2–3 days based on weather outlook."
else:
    timing_msg = "No irrigation required at present. Monitor soil moisture."

st.info(timing_msg)

# ===============================
# CIRCULAR WATER USE METRICS
# ===============================

baseline_demand = crop_wr * area * 10  # Traditional flood irrigation baseline
water_saved = baseline_demand - adjusted_crop_demand
saving_percent = (water_saved / baseline_demand) * 100

st.subheader("♻ Circular Water Use Impact")

col4, col5 = st.columns(2)
col4.metric("Water Saved (m³)", round(water_saved, 2))
col5.metric("Water Saved (%)", round(saving_percent, 2))

st.caption(
    "Optimizing irrigation reduces unnecessary groundwater extraction and "
    "supports circular and sustainable water use."
)

# ===============================
# VISUALIZATION
# ===============================

st.subheader("📊 Water Availability vs Demand")

fig, ax = plt.subplots()
ax.bar(
    ["Available Water", "Precision Crop Demand"],
    [total_available_water, adjusted_crop_demand]
)
ax.set_ylabel("Water (m³)")
ax.set_title("Agricultural Water Budget Analysis")

st.pyplot(fig)

# ===============================
# DECISION SUPPORT
# ===============================

st.subheader("📌 Decision Support Recommendations")

if status == "DEFICIT":
    st.write("- Shift to drip or sprinkler irrigation")
    st.write("- Reduce irrigation frequency using soil moisture feedback")
    st.write("- Prefer low water-intensive crops")
    st.write("- Plan groundwater recharge measures")

elif status == "SURPLUS":
    st.write("- Current irrigation plan is efficient")
    st.write("- Excess water can support groundwater recharge")
    st.write("- Continue monitoring soil moisture")

else:
    st.write("- Maintain current irrigation schedule")
    st.write("- Monitor rainfall and soil conditions")

# ===============================
# SENSOR DISCLAIMER
# ===============================

import streamlit as st
import random
import time

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Smart Irrigation AI Assistant",
    layout="wide"
)

st.title("🌱 Smart Irrigation Assistant for Farmers")
st.caption("Sensor-Based Irrigation | Agriculture Hackathon Demo")

# -------------------------
# SIMULATED SENSOR DATA
# -------------------------
def get_sensor_data():
    return {
        "soil_moisture": random.randint(20, 80),   # %
        "temperature": random.randint(20, 40),     # °C
        "humidity": random.randint(30, 90),        # %
        "rain_forecast": random.choice(["Yes", "No"])
    }

data = get_sensor_data()

# -------------------------
# MODE SELECTION
# -------------------------
mode = st.radio(
    "Choose how you want to use the system:",
    ["📊 View Sensor Statistics", "🤖 AI Assistant (Text / Voice)"]
)

# =====================================================
# OPTION A: STATISTICS VIEW
# =====================================================
if mode == "📊 View Sensor Statistics":
    st.header("📊 Current Field Conditions")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Soil Moisture (%)", data["soil_moisture"])
    col2.metric("Temperature (°C)", data["temperature"])
    col3.metric("Humidity (%)", data["humidity"])
    col4.metric("Rain Expected", data["rain_forecast"])

    st.info(
        "ℹ️ Farmers who are comfortable with numbers can view sensor data directly. "
        "Others may use the AI assistant for simple guidance."
    )

# =====================================================
# OPTION B: AI ASSISTANT
# =====================================================
else:
    st.header("🤖 AI Irrigation Assistant")

    st.write("Ask your question by typing or speaking. Example: *Aaj paani dena chahiye?*")

    # TEXT INPUT
    user_text = st.text_input("⌨️ Type your question (optional)")

    # VOICE INPUT
    audio = st.audio_input("🎤 Speak your question")

    if st.button("Get AI Advice"):
        with st.spinner("AI Assistant is analyzing field conditions..."):
            time.sleep(1)

        # SIMPLE DECISION LOGIC
        if data["soil_moisture"] > 60:
            response = (
                "Mitti mein nami kaafi hai. "
                "Aaj paani dene ki zarurat nahi hai."
            )
        elif data["rain_forecast"] == "Yes":
            response = (
                "Barish ke chances hain. "
                "Aaj paani mat dijiye."
            )
        else:
            response = (
                "Mitti sookhi hai. "
                "Aaj shaam ko thoda paani dena behtar rahega."
            )

        st.success("🤖 AI Assistant Advice")
        st.write(response)

        st.caption(
            "🔊 Voice-based interaction is demonstrated using microphone input. "
            "Speech understanding and multilingual support can be enhanced in future phases."
        )

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption(
    "This is a demonstration prototype. "
    "Sensor values are simulated, and AI decisions are rule-based for hackathon demonstration purposes."
)
