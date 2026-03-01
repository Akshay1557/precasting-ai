import streamlit as st
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Precasting-AI | CREATECH 2026",
    layout="wide"
)

st.title("🏗️ Precasting-AI")
st.subheader("AI-Based Concrete Demoulding Cycle Time Optimizer")

# -----------------------------------------------------
# SIDEBAR INPUTS
# -----------------------------------------------------

st.sidebar.header("🔧 Input Parameters")

required_strength = st.sidebar.number_input(
    "Required Demoulding Strength (MPa)",
    min_value=1.0,
    max_value=60.0,
    value=25.0
)

avg_temperature = st.sidebar.number_input(
    "Average Curing Temperature (°C)",
    min_value=-10.0,
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

# -----------------------------------------------------
# CONSTANTS & DATABASE
# -----------------------------------------------------

ultimate_strength = 50
datum_temp = -10

mix_designs = {
    "Standard Mix": 0.012,
    "High Early Strength": 0.020,
    "Eco Mix": 0.009
}

curing_methods = {
    "Normal Curing": {"cost_per_hr": 50, "temp_boost": 1.0},
    "Steam Curing": {"cost_per_hr": 120, "temp_boost": 1.4},
    "Accelerated Chemical": {"cost_per_hr": 90, "temp_boost": 1.2}
}

# -----------------------------------------------------
# PHYSICS MODEL
# -----------------------------------------------------

def maturity(temp, time):
    return (temp - datum_temp) * time

def hydration_strength(time, temp, rate):
    M = maturity(temp, time)
    return ultimate_strength * (1 - math.exp(-rate * M))

def environmental_factor(humidity, wind):
    humidity_effect = 1 + 0.4 * (1 - humidity)
    wind_effect = 1 + 0.05 * wind
    return humidity_effect * wind_effect

def adjusted_strength(time, temp, rate, humidity, wind):
    base = hydration_strength(time, temp, rate)
    env_penalty = environmental_factor(humidity, wind)
    return base / env_penalty

# -----------------------------------------------------
# MACHINE LEARNING MODEL
# -----------------------------------------------------

time_data = np.array([4, 8, 12, 18, 24, 36, 48]).reshape(-1,1)
strength_data = np.array([5, 12, 18, 26, 32, 40, 46])

ml_model = RandomForestRegressor()
ml_model.fit(time_data, strength_data)

def ml_strength(time):
    return ml_model.predict([[time]])[0]

# -----------------------------------------------------
# HYBRID MODEL
# -----------------------------------------------------

def final_strength(time, temp, rate, humidity, wind):
    physics = adjusted_strength(time, temp, rate, humidity, wind)
    data = ml_strength(time)
    return 0.6 * physics + 0.4 * data

# -----------------------------------------------------
# SIMULATION
# -----------------------------------------------------

results = []

for mix, rate in mix_designs.items():
    for curing, data in curing_methods.items():

        effective_temp = avg_temperature * data["temp_boost"]

        time = 1
        found = False

        while time <= 72:
            strength = final_strength(time, effective_temp, rate, humidity, wind_speed)
            if strength >= required_strength:
                found = True
                break
            time += 0.5

        if found:
            cost = time * data["cost_per_hr"]
            results.append({
                "Mix": mix,
                "Curing": curing,
                "Cycle_Time_hr": round(time, 2),
                "Cost": round(cost, 2)
            })

df = pd.DataFrame(results)

# -----------------------------------------------------
# CHECK IF NO SOLUTION
# -----------------------------------------------------

if df.empty:
    st.error("❌ No feasible solution found within 72 hours. Try adjusting inputs.")
    st.stop()

# -----------------------------------------------------
# SAFE NORMALIZATION
# -----------------------------------------------------

time_range = df["Cycle_Time_hr"].max() - df["Cycle_Time_hr"].min()
cost_range = df["Cost"].max() - df["Cost"].min()

if time_range == 0:
    df["time_norm"] = 1
else:
    df["time_norm"] = (
        df["Cycle_Time_hr"] - df["Cycle_Time_hr"].min()
    ) / time_range

if cost_range == 0:
    df["cost_norm"] = 1
else:
    df["cost_norm"] = (
        df["Cost"] - df["Cost"].min()
    ) / cost_range

df["Score"] = 0.6 * df["time_norm"] + 0.4 * df["cost_norm"]

if df["Score"].isna().all():
    st.error("❌ Unable to compute optimal strategy.")
    st.stop()

best = df.loc[df["Score"].idxmin()]

# -----------------------------------------------------
# DISPLAY RESULTS
# -----------------------------------------------------

st.subheader("📊 All Scenarios")
st.dataframe(df)

st.subheader("🏆 Optimal Strategy")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Best Mix", best["Mix"])
col2.metric("Curing Method", best["Curing"])
col3.metric("Cycle Time (hr)", best["Cycle_Time_hr"])
col4.metric("Cost (₹)", best["Cost"])

# -----------------------------------------------------
# VISUALIZATION
# -----------------------------------------------------

st.subheader("📈 Cost Comparison")

fig1, ax1 = plt.subplots()
ax1.bar(df["Mix"] + " + " + df["Curing"], df["Cost"])
plt.xticks(rotation=45)
plt.ylabel("Cost (₹)")
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

time_range_plot = np.linspace(0, 72, 100)
strength_curve = [
    final_strength(t, best_temp, best_rate, humidity, wind_speed)
    for t in time_range_plot
]

fig3, ax3 = plt.subplots()
ax3.plot(time_range_plot, strength_curve)
ax3.axhline(required_strength)
ax3.set_xlabel("Time (hr)")
ax3.set_ylabel("Strength (MPa)")
st.pyplot(fig3)
