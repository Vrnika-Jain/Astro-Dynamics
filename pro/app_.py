import streamlit as st
from datetime import datetime
import numpy as np
from mission_planning.launch_window import calculate_launch_window
from mission_planning.rendezvous import rendezvous
from orbital_mechanics.hohmann_transfer import hohmann_transfer
from orbital_mechanics.kepler_orbit import kepler_orbit
from orbital_mechanics.perturbations import atmospheric_drag, gravitational_perturbation
from trajectory_optimization.lamberts_problem import lamberts_problem
from trajectory_optimization.low_thrust import low_thrust_trajectory
from utils import constants
from utils import conversions

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-image: url('https://wallpapers.com/images/hd/space-mission-4012-x-2224-wallpaper-f7b82t1zk9gf5nmk.jpg');  /* Replace with your own URL */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #F5F5F5;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.8);
        color: #F5F5F5;
    }
    .stSidebar {
        background-image: url('https://wallpapers.com/images/hd/space-mission-4012-x-2224-wallpaper-f7b82t1zk9gf5nmk.jpg');  /* Replace with your own URL */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        padding: 10px;
        border-radius: 10px;
        color: #2B2442;
        filter: blur(30px); 
    }
    .sidebar .sidebar-content h2 {
    color: rgb(43, 36, 66); /* Sidebar headings */
    }
    h1 {
        color: rgb(255, 255, 255); /* White color for titles */
    }
    h2, h3 {
        color: rgb(106, 233, 247); /* DodgerBlue color for headings */
    }
    .data {
    color: rgb(255, 165, 0); /* Orange color for data */
    }
    .small-text {
        color: rgb(175, 150, 255);  /* Small text above sliders */
    }
    .slider-text {
        color: rgb(80, 10, 194);  /* Text color above sliders */
    }
    body {
        background-color: #6c809e; /* Dark background color */
        color: white; /* Text color */
    }
    .stButton button {
        background-color: rgb(30, 144, 255);  /* DodgerBlue background color */
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
    }
    .stButton button:hover {
        background-color: white;
        color: rgb(74, 10, 194);
        border: 2px solid rgb(30, 144, 255);
    }
    .stTextInput>div>div>input {
        background-color: #333;
        color: rgb(245, 245, 245);
        border: 1px solid rgb(30, 144, 255);
        border-radius: 5px;
    }
    .stDateInput>div>div>input {
        background-color: #333;
        color: rgb(245, 245, 245);
        border: 1px solid rgb(30, 144, 255);
        border-radius: 5px;
    }
    .stSlider>div>div>div>div {
        background-color: rgb(30, 144, 255);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for user inputs
st.sidebar.title("Mission Planning Parameters")
st.sidebar.write("Note: Changes are reflected on the right hand side w.r.t. the labels.")
departure_date = st.sidebar.date_input("Departure Date", datetime(2024, 7, 20))
target_date = st.sidebar.date_input("Target Date", datetime(2024, 8, 15))
launch_window_days = st.sidebar.slider("Launch Window (Days)", 1, 14, 7)

# Calculate launch window
launch_window_start, launch_window_end = calculate_launch_window(departure_date, target_date, launch_window_days)

st.sidebar.title("Orbital Mechanics Parameters")
initial_orbit_radius = st.sidebar.number_input("Initial Orbit Radius (km)", value=7000)
final_orbit_radius = st.sidebar.number_input("Final Orbit Radius (km)", value=14000)
phase_angle = st.sidebar.slider("Phase Angle (degrees)", 0, 360, 30)

# Calculate Hohmann transfer
delta_v1, delta_v2 = hohmann_transfer(initial_orbit_radius, final_orbit_radius)

st.sidebar.title("Lambert's Problem Parameters")
r1 = st.sidebar.text_input("Initial Position Vector (comma-separated)", "5000, 10000, 2100")
r2 = st.sidebar.text_input("Final Position Vector (comma-separated)", "-14600, 2500, 7000")
tof = st.sidebar.number_input("Time of Flight (seconds)", value=3600)

# Parse input vectors
r1 = [float(x) for x in r1.split(',')]
r2 = [float(x) for x in r2.split(',')]

# Calculate Lambert's problem solution
v1, v2 = lamberts_problem(r1, r2, tof)

# Main app content
st.title("Mission Planning Dashboard")

st.header("Launch Window Calculation")
st.write(f"**Launch Window Start:** {launch_window_start}")
st.write(f"**Launch Window End:** {launch_window_end}")

st.header("Orbital Mechanics")
st.write(f"**Hohmann Transfer Delta-v1:** {delta_v1:.3f} km/s")
st.write(f"**Hohmann Transfer Delta-v2:** {delta_v2:.3f} km/s")

st.header("Lambert's Problem Solution")
st.write(f"**Initial Velocity Vector:** {v1}")
st.write(f"**Final Velocity Vector:** {v2}")

st.header("Interactive Plots")
st.subheader("Kepler Orbit Calculation")
semi_major_axis = st.slider("Semi-Major Axis (km)", 1000, 20000, 7000)
eccentricity = st.slider("Eccentricity", 0.0, 1.0, 0.1)
true_anomaly = st.slider("True Anomaly (degrees)", 0, 360, 45)

# Calculate Kepler orbit
true_anomaly_rad = np.radians(true_anomaly)
radius = kepler_orbit(semi_major_axis, eccentricity, true_anomaly_rad)

st.write(f"**Radius at True Anomaly {true_anomaly}°:** {radius:.2f} km")
