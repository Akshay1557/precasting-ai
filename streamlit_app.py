import streamlit as st
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Concrete Cycle Time Optimizer", layout="wide")

st.title("🏗️ AI-Based Concrete Demoulding Cycle Time Optimizer")

# =====================================================
# USER INPUTS (SIDEBAR)
# =====================================================

st.sidebar.header("Input Parameters")

required_strength = st.sidebar.number_input(
    "Required Demoulding Strength (MPa)",
    min_value=1.0,
    max_value=60.0,
    value=25.0
)

avg_temperature = st.sidebar.number_input(
    "Average Curing Temperature (°C)",
    min_value=0.0,
    max_value=60.0,
    value=30.0
)

humidity = st.sidebar.slider(
    "Relative Humidity (0 to 1)",
    min_value=0.0,
    max_value=1.0,
    value=0.7
)

wind_speed = st.sidebar.number_input(
    "Wind Speed (m/s)",
    min_value=0.0,
    max_value=20.0,
    value=2.0
)

# =====================================================
# MATERIAL DATABASE
# =====================================================

ultimate_strength = 50
datum_temp = -10

mix_designs = {
    "standard_mix": 0.012,
    "high_early_strength": 0.020,
    "eco_mix": 0.009
}

curing_methods = {
    "normal_curing": {"cost_per_hr": 50, "temp_boost": 1.0},
    "steam_curing": {"cost_per_hr": 120, "temp_boost": 1.4},
    "accelerated_chemical": {"cost_per_hr": 90, "temp_boost": 1.2}
}

# =====================================================
# HYDRATION MODEL
# =====================================================

def maturity(temp, time):
    return (temp - datum_temp) * time

def hydration_strength(time, temp, rate):
    M = maturity(temp, time)
    return ultimate_strength * (1 - math.exp(-rate * M))

# =====================================================
# ENVIRONMENT MODEL
# =====================================================

def environmental_factor(humidity, wind):
    humidity_effect = 1 + 0.4 * (1 - humidity)
    wind_effect = 1 + 0.05 * wind
    return humidity_effect * wind_effect

def adjusted_strength(time, temp, rate, humidity, wind):
    base = hydration_strength(time, temp, rate)
    env_penalty = environmental_factor(humidity, wind)
    return base / env_penalty

# =====================================================
# MACHINE LEARNING MODEL
# =====================================================

time_data = np.array([4, 8, 12, 18, 24, 36, 48]).reshape(-1,1)
strength_data = np.array([5, 12, 18, 26, 32, 40, 46])

ml_model = RandomForestRegressor()
ml_model.fit(time_data, strength_data)

def ml_strength(time):
    return ml_model.predict([[time]])[0]

# =====================================================
# HYBRID MODEL
# =====================================================

def final_strength(time, temp, rate, humidity, wind):
    physics = adjusted_strength(time, temp, rate, humidity, wind)
    data = ml_strength(time)
    return 0.6 * physics + 0.4 * data

# =====================================================
# SIMULATION ENGINE
# =====================================================

results = []

for mix, rate in mix_designs.items():
    for curing, data in curing_methods.items():

        effective_temp = avg_temperature * data["temp_boost"]

        time = 1
        while final_strength(time, effective_temp, rate, humidity, wind_speed) < required_strength:
            time += 0.5
            if time > 72:
                break

        cost = time * data["cost_per_hr"]

        results.append({
            "Mix": mix,
            "Curing": curing,
            "Cycle_Time_hr": round(time,2),
            "Cost": round(cost,2)
        })

df = pd.DataFrame(results)

# =====================================================
# OPTIMIZATION
# =====================================================

df["time_norm"] = (df["Cycle_Time_hr"] - df["Cycle_Time_hr"].min()) / (
    df["Cycle_Time_hr"].max() - df["Cycle_Time_hr"].min()
)

df["cost_norm"] = (df["Cost"] - df["Cost"].min()) / (
    df["Cost"].max() - df["Cost"].min()
)

df["Score"] = 0.6*df["time_norm"] + 0.4*df["cost_norm"]
best = df.loc[df["Score"].idxmin()]

# =====================================================
# DISPLAY RESULTS
# =====================================================

st.subheader("📊 All Scenarios")
st.dataframe(df)

st.subheader("🏆 Optimal Strategy")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Best Mix", best["Mix"])
col2.metric("Curing Method", best["Curing"])
col3.metric("Cycle Time (hr)", best["Cycle_Time_hr"])
col4.metric("Cost", f"₹ {best['Cost']}")

# =====================================================
# VISUALIZATION
# =====================================================

st.subheader("📈 Cost Comparison")

fig1, ax1 = plt.subplots()
ax1.bar(df["Mix"] + " + " + df["Curing"], df["Cost"])
plt.xticks(rotation=45)
plt.ylabel("Cost")
st.pyplot(fig1)

st.subheader("⏱ Cycle Time Comparison")

fig2, ax2 = plt.subplots()
ax2.bar(df["Mix"] + " + " + df["Curing"], df["Cycle_Time_hr"])
plt.xticks(rotation=45)
plt.ylabel("Cycle Time (hr)")
st.pyplot(fig2)

# Strength Curve
st.subheader("📈 Strength Development Curve (Optimal Strategy)")

best_rate = mix_designs[best["Mix"]]
best_temp = avg_temperature * curing_methods[best["Curing"]]["temp_boost"]

time_range = np.linspace(0,50,100)
strength_curve = [
    final_strength(t,best_temp,best_rate,humidity,wind_speed)
    for t in time_range
]

fig3, ax3 = plt.subplots()
ax3.plot(time_range, strength_curve)
ax3.axhline(required_strength)
ax3.set_xlabel("Time (hr)")
ax3.set_ylabel("Strength (MPa)")
st.pyplot(fig3)
