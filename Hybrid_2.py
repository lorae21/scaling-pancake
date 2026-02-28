# 1️⃣ Import libraries
import streamlit as st
import pandas as pd
import numpy as np

# 2️⃣ App Header
st.title("Nairobi Data Center Water Use & WUE Analysis")
st.markdown("""
This app calculates:
- Water consumption for a data center in **liters**
- Water savings using hybrid cooling (dry cooling when wet-bulb < 15°C)
- Equivalent number of Nairobi residents served per year
""")

# 3️⃣ User Input: IT Load in Megawatts
it_load_mw = st.number_input(
    "Enter the Data Center IT Load in Megawatts (MW)", 
    min_value=0.0, 
    value=10.0, 
    step=1.0
)

# 4️⃣ Load your dataset (CSV with Nairobi climate and WUE data)
df = pd.read_csv("Nairobi.csv")  # Replace with your actual file path

# 5️⃣ Convert wet-bulb temperature to Celsius if needed
df["wetbulb_C"] = (df["wetbulb_temperature"] - 32) * (5/9)

# 6️⃣ Hybrid WUE logic
df["WUE_hybrid"] = np.where(
    df["wetbulb_C"] < 15, 
    0.1,  # Dry cooling: liters per kilowatt-hour
    df["WUE_FixedApproachDirect(L/KWh)"]  # Evaporative cooling
)

# 7️⃣ Convert IT load to hourly energy usage in kilowatt-hours (kWh)
# 1 Megawatt (MW) = 1000 kilowatts (kW), so hourly energy = IT load in MW * 1000 kWh
hourly_energy_kwh = it_load_mw * 1000

# 8️⃣ Calculate hourly water usage in liters
df["water_original_liters"] = df["WUE_FixedApproachDirect(L/KWh)"] * hourly_energy_kwh
df["water_hybrid_liters"] = df["WUE_hybrid"] * hourly_energy_kwh

# 9️⃣ Annual totals in liters
annual_original_liters = df["water_original_liters"].sum()
annual_hybrid_liters = df["water_hybrid_liters"].sum()
annual_water_saved_liters = annual_original_liters - annual_hybrid_liters

# 10️⃣ Household equivalency (assuming 40 liters/day per resident)
people_equivalent = annual_water_saved_liters / (40 * 365)

# 11️⃣ Display results with full units
st.subheader("Annual Water Use Results")
st.write(f"Annual Water Use (Original System): {annual_original_liters:,.0f} liters")
st.write(f"Annual Water Use (Hybrid System): {annual_hybrid_liters:,.0f} liters")
st.write(f"Annual Water Saved with Hybrid Cooling: {annual_water_saved_liters:,.0f} liters")
st.write(f"Equivalent Number of Residents Supplied for One Year: {people_equivalent:,.0f} people")

# 12️⃣ Dry cooling feasibility
dry_cooling_hours = (df["wetbulb_C"] < 15).sum()
st.write(f"Number of hours per year where dry cooling is feasible: {dry_cooling_hours} hours")
st.write(f"Percentage of the year: {dry_cooling_hours / len(df) * 100:.1f}%")