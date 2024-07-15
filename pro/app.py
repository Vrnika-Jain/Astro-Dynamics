from mission_planning.launch_window import calculate_launch_window
from mission_planning.rendezvous import rendezvous
from trajectory_optimization.lamberts_problem import lamberts_problem
from trajectory_optimization.low_thrust import low_thrust_trajectory
from orbital_mechanics.kepler_orbit import kepler_orbit
from orbital_mechanics.hohmann_transfer import hohmann_transfer
from orbital_mechanics.perturbations import atmospheric_drag, gravitational_perturbation
from utils.constants import MU_EARTH
from utils.conversions import degrees_to_radians
import streamlit as st

def main():
    # Add a background image to the entire page
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://i.pinimg.com/736x/e4/b6/71/e4b6716681fdac4a0ad3eae975484ecb.jpg");
        background-size: cover;
    }
    </style>
    '''

    # Display the background image
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Title and Sidebar
    st.title("Astrodynamics Application")
    st.sidebar.header("Select Functionality")

    # Functionality selection
    functionality = st.sidebar.selectbox(
        "Choose a functionality",
        ("Calculate Launch Window", "Calculate Rendezvous Maneuver", "Calculate Lambert's Problem", "Calculate Low-Thrust Trajectory")
    )

    # Launch Window Calculation
    if functionality == "Calculate Launch Window":
        st.subheader("Launch Window Calculation")
        departure_date = st.date_input("Enter Departure Date")
        target_date = st.date_input("Enter Target Date")
        launch_window_days = st.number_input("Launch Window Duration (days)", min_value=1, value=7)

        if st.button("Calculate"):
            launch_window_start, launch_window_end = calculate_launch_window(departure_date, target_date, launch_window_days)
            st.write(f"Launch window: {launch_window_start} to {launch_window_end}")

    # Rendezvous Maneuver Calculation
    elif functionality == "Calculate Rendezvous Maneuver":
        st.subheader("Rendezvous Maneuver Calculation")
        initial_orbit_radius = st.number_input("Initial Orbit Radius (km)", min_value=1)
        target_orbit_radius = st.number_input("Target Orbit Radius (km)", min_value=1)
        phase_angle = st.number_input("Phase Angle (degrees)", min_value=0, max_value=360, value=30)

        if st.button("Calculate"):
            delta_v1, delta_v2, time_to_wait = rendezvous(initial_orbit_radius, target_orbit_radius, phase_angle)
            st.write(f"Delta-v for the first burn: {delta_v1:.3f} km/s")
            st.write(f"Delta-v for the second burn: {delta_v2:.3f} km/s")
            if time_to_wait > 0:
                st.write(f"Time to wait for correct phase angle: {time_to_wait / 3600:.2f} hours")

    # Lambert's Problem Calculation
    elif functionality == "Calculate Lambert's Problem":
        st.subheader("Lambert's Problem Calculation")
        r1_x = st.number_input("Initial Position X (km)", value=5000)
        r1_y = st.number_input("Initial Position Y (km)", value=10000)
        r1_z = st.number_input("Initial Position Z (km)", value=2100)
        r2_x = st.number_input("Final Position X (km)", value=-14600)
        r2_y = st.number_input("Final Position Y (km)", value=2500)
        r2_z = st.number_input("Final Position Z (km)", value=7000)
        tof = st.number_input("Time of Flight (seconds)", min_value=1, value=3600)

        if st.button("Calculate"):
            r1 = [r1_x, r1_y, r1_z]
            r2 = [r2_x, r2_y, r2_z]
            v1, v2 = lamberts_problem(r1, r2, tof)
            st.write(f"Initial velocity: {v1} km/s")
            st.write(f"Final velocity: {v2} km/s")

    # Low-Thrust Trajectory Calculation
    elif functionality == "Calculate Low-Thrust Trajectory":
        st.subheader("Low-Thrust Trajectory Calculation")
        r0_x = st.number_input("Initial Position X (km)", value=7000)
        r0_y = st.number_input("Initial Position Y (km)", value=0)
        r0_z = st.number_input("Initial Position Z (km)", value=0)
        v0_x = st.number_input("Initial Velocity X (km/s)", value=0)
        v0_y = st.number_input("Initial Velocity Y (km/s)", value=7.8)
        v0_z = st.number_input("Initial Velocity Z (km/s)", value=0)
        thrust = st.number_input("Thrust (N)", value=0.01)
        isp = st.number_input("Specific Impulse (s)", value=3000)
        mass = st.number_input("Initial Mass (kg)", value=500)
        t_span = (0, st.number_input("Time Span (seconds)", min_value=1, value=86400))

        if st.button("Calculate"):
            r0 = [r0_x, r0_y, r0_z]
            v0 = [v0_x, v0_y, v0_z]
            trajectory = low_thrust_trajectory(r0, v0, thrust, isp, mass, t_span)
            st.write(f"Final position: {trajectory.y[:3, -1]} km")
            st.write(f"Final velocity: {trajectory.y[3:6, -1]} km/s")
            st.write(f"Final mass: {trajectory.y[6, -1]} kg")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Created with ❤️ by Vrnika Jain")

