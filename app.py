import streamlit as st
import matplotlib.pyplot as plt

# ===============================
# STATIC DATA (EMBEDDED)
# ===============================

# Average seasonal rainfall (mm)
RAINFALL_DATA = {
    "Indore": 800,
    "Bhopal": 1000,
    "Nagpur": 900
}

# Crop water requirement per season (mm)
CROP_WATER_REQUIREMENT = {
    "Rice": 1200,
    "Wheat": 450,
    "Soybean": 500,
    "Maize": 600
}

# Irrigation efficiency factors
IRRIGATION_FACTOR = {
    "Flood": 1.0,
    "Sprinkler": 0.75,
    "Drip": 0.6
}

# Groundwater availability index
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

st.title("🌾 Agricultural Efficiency – Sensor-Ready Water Budgeting Tool")
st.write(
    "A decision-support system to apply the **right amount of water at the right time** "
    "using water budgeting and simulated sensor inputs."
)

# ===============================
# SIDEBAR INPUTS
# ===============================

st.sidebar.header("🌱 Field & Sensor Inputs")

location = st.sidebar.selectbox(
    "Location",
    list(RAINFALL_DATA.keys())
)

crop = st.sidebar.selectbox(
    "Crop Type",
    list(CROP_WATER_REQUIREMENT.keys())
)

season = st.sidebar.selectbox(
    "Season",
    ["Kharif", "Rabi"]
)

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

# ---- Simulated Sensor Input ----
soil_moisture = st.sidebar.selectbox(
    "Soil Moisture Level (Sensor Input)",
    ["Low", "Medium", "High"]
)

# ===============================
# WATER AVAILABILITY CALCULATION
# ===============================

rainfall_mm = RAINFALL_DATA[location]

# 1 mm rainfall over 1 hectare = 10 cubic meters
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
# IRRIGATION TIMING ADVISORY
# ===============================

st.subheader("⏱ Irrigation Timing Recommendation")

if soil_moisture == "Low":
    timing_msg = "Irrigate immediately to avoid crop stress."
elif soil_moisture == "Medium":
    timing_msg = "Irrigate within the next 2–3 days."
else:
    timing_msg = "No irrigation required at present."

st.info(timing_msg)

# ===============================
# WATER SAVINGS METRIC
# ===============================

baseline_demand = crop_wr * area * 10  # Flood irrigation baseline
water_saved = baseline_demand - adjusted_crop_demand
saving_percent = (water_saved / baseline_demand) * 100

st.subheader("💦 Irrigation Efficiency Impact")
st.metric("Estimated Water Saved (%)", round(saving_percent, 2))

# ===============================
# VISUALIZATION
# ===============================

st.subheader("📊 Water Availability vs Demand")

fig, ax = plt.subplots()
ax.bar(
    ["Available Water", "Crop Demand"],
    [total_available_water, adjusted_crop_demand]
)
ax.set_ylabel("Water (m³)")
ax.set_title("Agricultural Water Budget")

st.pyplot(fig)

# ===============================
# DECISION SUPPORT
# ===============================

st.subheader("📌 Decision Support Recommendations")

if status == "DEFICIT":
    st.write("- Switch to drip or sprinkler irrigation")
    st.write("- Reduce irrigation frequency")
    st.write("- Consider low water-intensive crops")
    st.write("- Plan groundwater recharge measures")

elif status == "SURPLUS":
    st.write("- Current irrigation plan is safe")
    st.write("- Opportunity for groundwater recharge")
    st.write("- Continue monitoring soil moisture")

else:
    st.write("- Maintain current irrigation schedule")
    st.write("- Monitor rainfall and soil conditions")

# ===============================
# SENSOR DISCLAIMER
# ===============================

st.info(
    "🔌 **Sensor-Ready Architecture:** "
    "Soil moisture and rainfall values are simulated in this prototype. "
    "In real deployment, inputs will be ingested directly from IoT soil sensors "
    "and automated weather stations."
)
