import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
import random
from datetime import timedelta

# ==================================================
# FUNCTION: NEAR REAL-TIME RAINFALL (IMD DAILY CSV)
# ==================================================
def get_recent_rainfall_mp(district, days=7):
    try:
        df = pd.read_csv("daily_rainfall_mp.csv")

        df["Date"] = pd.to_datetime(df["Date"])
        df["Avg_rainfall"] = pd.to_numeric(df["Avg_rainfall"], errors="coerce")

        df = df[df["State"] == "Madhya Pradesh"]

        latest_date = df["Date"].max()
        cutoff_date = latest_date - timedelta(days=days)

        recent = df[
            (df["District"] == district) &
            (df["Date"] >= cutoff_date)
        ]

        if recent.empty:
            return 0.0

        return round(recent["Avg_rainfall"].sum(), 2)

    except Exception:
        return 0.0


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(page_title="Smart Irrigation & Water Budgeting", layout="wide")
st.title("Smart Irrigation & AI Assistant for Farmers")
st.caption("Near real-time rainfall + CGWB groundwater + soil moisture sensing")

# ==================================================
# LOAD DATA FILES
# ==================================================
daily_df = pd.read_csv("daily_rainfall_mp.csv")
gw_df = pd.read_csv("gov_groundwater_mp.csv")

# District list (safe intersection)
districts = sorted(
    set(daily_df["District"].unique())
    .intersection(set(gw_df["District"].unique()))
)

# ==================================================
# STATIC CONFIG
# ==================================================
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

GW_MAP = {
    "Safe": 0.6,
    "Semi-critical": 0.4,
    "Critical": 0.2,
    "Over-exploited": 0.1
}

SEASON_INFO = {
    "Kharif": {
        "months": "June – October",
        "rain": "High rainfall",
        "tip": "Irrigation needed only if rainfall is irregular."
    },
    "Rabi": {
        "months": "October – March",
        "rain": "Low rainfall",
        "tip": "Regular irrigation required."
    }
}

# ==================================================
# SIDEBAR INPUTS
# ==================================================
st.sidebar.header("Farm Details")

location = st.sidebar.selectbox("District", districts)
season = st.sidebar.selectbox("Season", ["Kharif", "Rabi"])
crop = st.sidebar.selectbox("Crop", list(CROP_WATER_REQUIREMENT.keys()))
area = st.sidebar.number_input("Farm Area (hectares)", min_value=0.1, value=1.0)
irrigation = st.sidebar.selectbox("Irrigation Method", list(IRRIGATION_FACTOR.keys()))

# ==================================================
# GROUNDWATER STATUS (CGWB)
# ==================================================
gw_row = gw_df[gw_df["District"] == location]

if not gw_row.empty:
    gw_status = gw_row.iloc[0]["Groundwater_Status"]
    groundwater_factor = GW_MAP.get(gw_status, 0.3)
    st.sidebar.write(f"Groundwater Status: **{gw_status}**")
else:
    groundwater_factor = 0.3
    st.sidebar.warning("Groundwater data unavailable. Using safe default.")

# ==================================================
# SOIL MOISTURE INPUT
# ==================================================
soil_mode = st.sidebar.radio("Soil Moisture Source", ["Live Sensor (Simulated)", "Manual"])

if soil_mode == "Manual":
    soil_moisture = st.sidebar.selectbox("Soil Moisture Level", ["Low", "Medium", "High"])
else:
    if "sensor" not in st.session_state:
        st.session_state.sensor = "Medium"

    if st.sidebar.button("Fetch Sensor Reading"):
        st.session_state.sensor = random.choice(["Low", "Medium", "High"])

    soil_moisture = st.session_state.sensor
    st.sidebar.write(f"Live Soil Moisture: **{soil_moisture}**")

# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3 = st.tabs(["Water Budget", "AI Assistant", "Season Guidance"])

# ==================================================
# TAB 1: WATER BUDGET
# ==================================================
with tab1:
    rainfall_mm = get_recent_rainfall_mp(location)
    st.caption("Source: IMD daily district-wise rainfall (last 7 days)")

    st.write(f"Rainfall Used (mm): **{rainfall_mm}**")

    rainfall_water = rainfall_mm * area * 10
    groundwater_water = rainfall_water * groundwater_factor
    total_available_water = rainfall_water + groundwater_water

    base_demand = (
        CROP_WATER_REQUIREMENT[crop] *
        area * 10 *
        IRRIGATION_FACTOR[irrigation]
    )

    moisture_factor = 0.6 if soil_moisture == "High" else 0.8 if soil_moisture == "Medium" else 1.0
    adjusted_demand = base_demand * moisture_factor
    water_balance = total_available_water - adjusted_demand

    c1, c2, c3 = st.columns(3)
    c1.metric("Available Water (m³)", round(total_available_water, 2))
    c2.metric("Crop Demand (m³)", round(adjusted_demand, 2))
    c3.metric("Water Balance (m³)", round(water_balance, 2))

    fig, ax = plt.subplots()
    ax.bar(["Available", "Demand"], [total_available_water, adjusted_demand])
    ax.set_ylabel("Water (m³)")
    st.pyplot(fig)

# ==================================================
# TAB 2: AI ASSISTANT
# ==================================================
with tab2:
    st.subheader("AI Irrigation Assistant")
    language = st.selectbox("Language", ["English", "Hindi"])

    if st.button("Get Advice"):
        time.sleep(1)

        if soil_moisture == "High":
            msg = "No irrigation required." if language == "English" else "अभी सिंचाई की आवश्यकता नहीं है।"
        elif soil_moisture == "Medium":
            msg = "Irrigate in 1–2 days." if language == "English" else "1–2 दिन में सिंचाई करें।"
        else:
            msg = "Immediate irrigation required." if language == "English" else "तुरंत सिंचाई आवश्यक है।"

        st.success(msg)

# ==================================================
# TAB 3: SEASON GUIDANCE
# ==================================================
with tab3:
    info = SEASON_INFO[season]
    st.markdown(f"""
    **Season Duration:** {info['months']}  
    **Rainfall Pattern:** {info['rain']}  
    **Guidance:** {info['tip']}
    """)
