🌾 Agricultural Water Budgeting Tool

An offline-first decision support system that helps farmers and agri-planners decide how much water to use, whether a crop is safe, and what better options exist when water is limited.

🚀 Live Prototype

👉 Live Streamlit App:
https://agricultural-water-budgeting-tool-aiclt2dqoba4hxjtx2yrxx.streamlit.app/

(Note: The prototype works without real-time internet data and demonstrates logic using offline datasets.)

❓ What Problem Does This Solve?

Agriculture often suffers from inefficient water usage because farmers do not know:

How much water is actually available

Whether a chosen crop is suitable for that water level

What action to take when water is insufficient

This leads to:

Over-irrigation and groundwater depletion

Crop stress and yield loss

Poor planning decisions based on guesswork

💡 What This Tool Does

This project converts water data into clear farming decisions.

It:

Estimates available water (rainfall + groundwater)

Calculates crop water demand

Compares both to generate a water budget

Classifies the situation as:

✅ Safe

⚠️ Manageable Risk

❌ Not Viable

Suggests alternative crops when water is insufficient

🧠 How It Helps Farmers

Instead of showing only numbers, the tool answers practical questions:

Can I safely grow this crop?

How much water should I actually use?

Should I reduce irrigation or change crops?

Key Farmer Benefits

Prevents over-irrigation

Reduces crop failure risk

Encourages water-efficient farming

Works in low-connectivity rural areas

🛠️ How to Use the Prototype

Open the Live Prototype link

Select:

Location

Crop type

Farm area (hectares)

Irrigation method

Groundwater availability

View results:

Available water

Crop water demand

Recommended water usage

Clear decision (Safe / Risk / Not Viable)

Follow the farmer guidance shown on screen

If crop is not viable, check suggested alternative crops

📊 Outputs You Will See

Water Budget Summary

Recommended irrigation limit

Clear decision explanation

Bar chart (Available vs Required vs Recommended water)

Pie chart (Rainfall vs Groundwater contribution)

Alternative crop suggestions (when needed)

🌱 Why This Project Is Different

Focuses on decisions, not just dashboards

Gives one clear action path (no confusing advice)

Fully offline-capable

Farmer-first, not engineer-first

Simple, explainable, and practical

🧩 Tech Stack

Language: Python
UI: Streamlit
Visualization: Matplotlib
Logic: Rule-based, explainable
Data: Static offline datasets

▶️ Run Locally
pip install -r requirements.txt
streamlit run app.py
