import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


st.set_page_config(
    page_title="Agricultural Water Budgeting Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)


RAIN_FALL = {
    "Indore": 800,
    "Bhopal": 1000,
    "Nagpur": 900,
    "Pune": 750
}

CROP_WATER_REQ = {
    "Rice": 1200,
    "Wheat": 450,
    "Soybean": 500,
    "Maize": 600,
    "Millet": 350
}

IRRIGATION_EFF = {
    "Flood": 1.0,
    "Sprinkler": 0.75,
    "Drip": 0.6
}

GROUNDWATER_LEVEL = {
    "Low": 0.2,
    "Medium": 0.4,
    "High": 0.6
}


st.title("🌾 Agricultural Water Budgeting Tool")
st.markdown(
    """
    A **decision-support system** that helps farmers understand  
    **how much water they should use**, whether a crop is **safe**, **risky**,  
    or **not suitable**, and what **better options** exist when water is limited.
    """
)

st.divider()

st.sidebar.header("🌱 Farm Details")

location = st.sidebar.selectbox("📍 Location", list(RAIN_FALL.keys()))
crop = st.sidebar.selectbox("🌾 Crop", list(CROP_WATER_REQ.keys()))
area = st.sidebar.number_input("📐 Farm Area (hectares)", min_value=0.1, value=1.0)
irrigation = st.sidebar.selectbox("🚿 Irrigation Method", list(IRRIGATION_EFF.keys()))
groundwater = st.sidebar.selectbox("💧 Groundwater Availability", list(GROUNDWATER_LEVEL.keys()))


rain_mm = RAIN_FALL[location]
rain_water = rain_mm * area * 10

groundwater_water = rain_water * GROUNDWATER_LEVEL[groundwater]
available_water = rain_water + groundwater_water

crop_demand = (
    CROP_WATER_REQ[crop]
    * area
    * 10
    * IRRIGATION_EFF[irrigation]
)

balance = available_water - crop_demand


if balance >= 0:
    recommended_usage = crop_demand
    shortage_ratio = 0
    decision = "SAFE"
elif abs(balance) / crop_demand <= 0.25:
    recommended_usage = available_water
    shortage_ratio = abs(balance) / crop_demand
    decision = "MANAGEABLE RISK"
else:
    recommended_usage = available_water
    shortage_ratio = abs(balance) / crop_demand
    decision = "NOT VIABLE"


st.subheader("💧 Water Budget Summary")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Available Water (m³)", f"{available_water:,.0f}")
m2.metric("Crop Water Demand (m³)", f"{crop_demand:,.0f}")
m3.metric("Recommended Usage (m³)", f"{recommended_usage:,.0f}")
m4.metric("Water Balance (m³)", f"{balance:,.0f}")

st.divider()


st.subheader("Farmer Decision & Explanation")

if decision == "SAFE":
    st.success(
        f"""
         **Safe to cultivate**

        - Available water is sufficient for this crop  
        - You can safely use **up to {recommended_usage:,.0f} m³**  
        - Continue normal irrigation practices
        """
    )

elif decision == "MANAGEABLE RISK":
    st.warning(
        f"""
        **Manageable water risk**

        - Water is slightly less than required  
        - Reduce irrigation by **{shortage_ratio*100:.1f}%**  
        - Maximum safe usage: **{recommended_usage:,.0f} m³**  
        - Prefer drip or sprinkler irrigation
        """
    )

else:
    st.error(
        f"""
         **Not suitable with current water availability**

        - Water is insufficient for this crop  
        - High risk of crop stress or yield loss  
        - Action required: change crop or reduce cultivated area
        """
    )


st.subheader("📊 Water Planning Comparison")

fig1, ax1 = plt.subplots()
ax1.bar(
    ["Available Water", "Crop Demand", "Recommended Usage"],
    [available_water, crop_demand, recommended_usage]
)
ax1.set_ylabel("Water (m³)")
ax1.set_title("How Available Water Compares With Crop Needs")

st.pyplot(fig1)


st.subheader("🌧️ Water Source Contribution")

fig2, ax2 = plt.subplots()
ax2.pie(
    [rain_water, groundwater_water],
    labels=["Rainfall", "Groundwater"],
    autopct="%1.1f%%",
    startangle=90
)
ax2.axis("equal")

st.pyplot(fig2)


if decision == "NOT VIABLE":
    st.subheader("🌱 Better Crop Options for This Water Level")

    suitable_crops = []
    for c, req in CROP_WATER_REQ.items():
        demand = req * area * 10 * IRRIGATION_EFF[irrigation]
        if demand <= available_water:
            suitable_crops.append(c)

    if suitable_crops:
        st.success(
            "Based on available water, these crops are **safer choices**:\n\n"
            + ", ".join(suitable_crops)
        )
    else:
        st.warning(
            "No crop is fully safe with the current water level.\n"
            "Consider reducing farm area or improving irrigation efficiency."
        )


st.info(
    "This offline-first prototype converts water data into **clear farming decisions**, "
    "making it suitable for real-world agricultural planning and hackathons."
)
