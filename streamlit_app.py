import streamlit as st
import numpy as np

# Title and Description
st.title("Spray Drying Powder Yield Calculator")
st.write("This tool helps you estimate the powder collected after spray drying based on input parameters, including adjustments for drying air properties and target quantities.")

# Input Categories
st.sidebar.header("Input Parameters")

# Characteristics of Product
st.sidebar.subheader("Characteristics of Product")
solid_content = st.sidebar.number_input("Solid Content in Feed (%):", min_value=0.1, max_value=100.0, value=40.0, step=0.1) / 100
remaining_humidity = st.sidebar.number_input("Remaining Humidity in Outlet Solid (%):", min_value=0.1, max_value=100.0, value=2.0, step=0.1) / 100

# Characteristics of Drying Medium
st.sidebar.subheader("Characteristics of Drying Medium")
airflow_rate = st.sidebar.number_input("Airflow Rate (kg/h):", min_value=10.0, max_value=750.0, value=150.0, step=10.0)
drying_air_temp_input = st.sidebar.number_input("Temperature of Input Air (°C):", min_value=0, max_value=50, value=25, step=1)
drying_air_humidity = st.sidebar.number_input("Humidity of Input Air (%):", min_value=0.0, max_value=100.0, value=60.0, step=0.1) / 100
hot_air_inlet_temp = st.sidebar.number_input("Hot Air Inlet Temperature (°C):", min_value=150, max_value=300, value=180, step=1)
hot_air_outlet_temp = st.sidebar.number_input("Hot Air Outlet Temperature (°C):", min_value=70, max_value=120, value=80, step=1)

# Target Quantity
st.sidebar.subheader("Target Quantity")
target_powder_mass = st.sidebar.number_input("Target Mass of Powder to be Collected (kg):", min_value=0.1, max_value=1000.0, value=50.0, step=0.1)
yield_efficiency = st.sidebar.number_input("Yield of the Machine (%):", min_value=0.0, max_value=100.0, value=90.0, step=0.1) / 100

# Constants for air properties
R = 287.05  # Specific gas constant for dry air (J/kg·K)
Mw = 18.016  # Molar mass of water (g/mol)
Md = 28.97  # Molar mass of dry air (g/mol)
P = 101325  # Atmospheric pressure (Pa)

# Calculate saturation vapor pressure (Pa) using Antoine equation approximation for water
def saturation_vapor_pressure(temp_c):
    return 610.94 * np.exp((17.625 * temp_c) / (temp_c + 243.04))

# Calculate absolute humidity
saturation_pressure = saturation_vapor_pressure(drying_air_temp_input)
actual_vapor_pressure = saturation_pressure * drying_air_humidity
absolute_humidity = (Mw / Md) * (actual_vapor_pressure / (P - actual_vapor_pressure))

# Water content in air (kg/h)
water_in_air = airflow_rate * absolute_humidity

# Moisture in product (kg water per kg final product)
moisture_in_feed = 1/(solid_content / (1 - solid_content))
moisture_in_final_product = remaining_humidity / (1 - remaining_humidity)
water_to_dry = moisture_in_feed - moisture_in_final_product

# Simplified water evaporation rate (kg/h)
def water_evaporation_rate(Tin, Tout, airflow_rate):
    base_rate = (Tin / 3.75 - 30 + (100 - Tout) / 30 * 9)
    return base_rate * (airflow_rate / 750)

# Calculate evaporation rate
water_evap_rate = water_evaporation_rate(hot_air_inlet_temp, hot_air_outlet_temp, airflow_rate)

# Effective water evaporation rate (kg/h)
effective_water_evap_rate = water_evap_rate - water_in_air

# Final powder rate (kg/h)
powder_production_rate = effective_water_evap_rate/water_to_dry*yield_efficiency
adjusted_feed_flow_rate = powder_production_rate*(1+water_to_dry)

# Time required to reach the target quantity (h)
time_to_target = target_powder_mass / powder_production_rate if powder_production_rate > 0 else float('inf')

# Display Results
st.subheader("Results")

# Characteristics of Product Results
st.write("### Characteristics of Product")
st.write(f"Solid Content in Feed: {solid_content * 100:.2f}%")
st.write(f"Remaining Humidity in Outlet Solid: {remaining_humidity * 100:.2f}%")
st.write(f"Moisture in Feed (kg water per kg final product): {moisture_in_feed:.2f}")
st.write(f"Moisture in Final Product (kg water per kg final product): {moisture_in_final_product:.2f}")

# Characteristics of Drying Medium Results
st.write("### Characteristics of Drying Medium")
st.write(f"Airflow Rate: {airflow_rate:.2f} m³/h")
st.write(f"Temperature of Input Air: {drying_air_temp_input:.2f} °C")
st.write(f"Humidity of Input Air: {drying_air_humidity * 100:.2f}%")
st.write(f"Hot Air Inlet Temperature: {hot_air_inlet_temp:.2f} °C")
st.write(f"Hot Air Outlet Temperature: {hot_air_outlet_temp:.2f} °C")
st.write(f"Water Content in Air: {water_in_air:.2f} kg/h")
st.write(f"Absolute Humidity: {absolute_humidity:.4f} kg water/kg dry air")
st.write(f"Water Evaporation Rate: {water_evap_rate:.2f} kg/h")
st.write(f"Effective Water Evaporation Rate: {effective_water_evap_rate:.2f} kg/h")

# Target Quantity Results
st.write("### Target Quantity")
st.write(f"Target Powder Mass: {target_powder_mass:.2f} kg")
st.write(f"Yield Efficiency: {yield_efficiency * 100:.2f}%")

# Final Results
st.write("### Final results")
st.write(f"Feed Flow Rate Required: {adjusted_feed_flow_rate:.2f} kg/h")
st.write(f"Powder Production Rate: {powder_production_rate:.2f} kg/h")
st.write(f"Time to Reach Target: {time_to_target:.2f} hours")
