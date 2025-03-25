import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

# Simulated data generation function (replace with actual data source)
def generate_patient_data(num_patients=10):
    patients = []
    triage_colors = ['Green', 'Yellow', 'Red', 'Black']
    
    for i in range(num_patients):
        patient = {
            'Patient ID': f'P{i+1:03d}',
            'Name': f'Patient {i+1}',
            'Age': np.random.randint(18, 85),
            'Triage Color': np.random.choice(triage_colors, p=[0.5, 0.3, 0.15, 0.05]),
            'Heart Rate': np.random.randint(60, 120),
            'Temperature': round(np.random.uniform(36.0, 40.0), 1),
            'PPD Data': {
                'Respiratory Rate': np.random.randint(12, 30),
                'Oxygen Saturation': np.random.randint(85, 100),
                'Blood Pressure': f"{np.random.randint(90, 180)}/{np.random.randint(60, 110)}"
            }
        }
        patients.append(patient)
    
    return pd.DataFrame(patients)

# Generate historical time series data for plotting
def generate_time_series_data(patient_id):
    # Simulate time series data for heart rate and temperature
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=24, freq='H')
    heart_rate = np.random.normal(80, 10, 24)
    temperature = np.random.normal(37, 0.5, 24)
    
    return pd.DataFrame({
        'Timestamp': timestamps,
        'Heart Rate': heart_rate,
        'Temperature': temperature
    })

# Streamlit app configuration
def main():
    st.set_page_config(
        page_title="Smart Triage Bracelet Dashboard",
        page_icon=":hospital:",
        layout="wide"
    )
    
    # App title
    st.title("Smart Triage Bracelet Patient Monitoring System")
    
    # Generate patient data
    patient_data = generate_patient_data()
    
    # Create columns for patient cards and details
    patient_cards_col, patient_details_col = st.columns([1, 3])
    
    # Patient Cards Column
    with patient_cards_col:
        st.header("Patients")
        
        # Create a container for scrollable patient cards
        patient_container = st.container()
        
        # Track selected patient
        selected_patient_id = None
        
        # Display patient cards
        for index, patient in patient_data.iterrows():
            # Color mapping for triage status
            color_map = {
                'Green': '#4CAF50',   # Green
                'Yellow': '#FFC107',  # Amber
                'Red': '#F44336',     # Red
                'Black': '#000000'    # Black
            }
            
            # Create a card-like display for each patient
            with patient_container:
                card_style = f"""
                background-color: white;
                border: 2px solid {color_map[patient['Triage Color']]};
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
                cursor: pointer;
                """
                
                # Use st.markdown to create a clickable card
                patient_card = st.markdown(f"""
                <div style="{card_style}">
                    <h4>Patient {patient['Patient ID']}</h4>
                    <p><strong>Age:</strong> {patient['Age']}</p>
                    <p><strong>Status:</strong> <span style="color:{color_map[patient['Triage Color']]};">{patient['Triage Color']}</span></p>
                    <p><strong>Heart Rate:</strong> {patient['Heart Rate']} bpm</p>
                    <p><strong>Temp:</strong> {patient['Temperature']}°C</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add a hidden button to track selection
                if st.button(f"Select {patient['Patient ID']}", key=f"select_{patient['Patient ID']}", type='primary', use_container_width=True):
                    selected_patient_id = patient['Patient ID']
    
    # Patient Details Column
    with patient_details_col:
        # If no patient is selected, show default view
        if selected_patient_id is None:
            st.info("Please select a patient from the left panel to view detailed information.")
            return
        
        # Filter selected patient
        selected_patient = patient_data[patient_data['Patient ID'] == selected_patient_id].iloc[0]
        
        # Create columns for patient overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Patient Information")
            st.write(f"**Patient ID:** {selected_patient['Patient ID']}")
            st.write(f"**Name:** {selected_patient['Name']}")
            st.write(f"**Age:** {selected_patient['Age']}")
        
        with col2:
            st.subheader("Vital Signs")
            st.write(f"**Heart Rate:** {selected_patient['Heart Rate']} bpm")
            st.write(f"**Temperature:** {selected_patient['Temperature']}°C")
        
        with col3:
            st.subheader("Triage Classification")
            # Color-coded triage status
            color_map = {
                'Green': 'green',
                'Yellow': 'orange',
                'Red': 'red',
                'Black': 'black'
            }
            triage_color = selected_patient['Triage Color']
            st.markdown(f"**Status:** <span style='color:{color_map[triage_color]};font-weight:bold'>{triage_color}</span>", 
                        unsafe_allow_html=True)
        
        # PPD Data Section
        st.subheader("Patient Physiological Data (PPD)")
        ppd_col1, ppd_col2, ppd_col3 = st.columns(3)
        
        with ppd_col1:
            st.metric("Respiratory Rate", 
                      f"{selected_patient['PPD Data']['Respiratory Rate']} breaths/min")
        
        with ppd_col2:
            st.metric("Oxygen Saturation", 
                      f"{selected_patient['PPD Data']['Oxygen Saturation']}%")
        
        with ppd_col3:
            st.metric("Blood Pressure", 
                      selected_patient['PPD Data']['Blood Pressure'])
        
        # Time Series Visualizations
        st.subheader("Time Series Monitoring")
        time_series_data = generate_time_series_data(selected_patient_id)
        
        # Heart Rate Plot
        fig_heart_rate = px.line(
            time_series_data, 
            x='Timestamp', 
            y='Heart Rate', 
            title='Heart Rate Over Time',
            labels={'Heart Rate': 'Heart Rate (bpm)'}
        )
        st.plotly_chart(fig_heart_rate, use_container_width=True)
        
        # Temperature Plot
        fig_temperature = px.line(
            time_series_data, 
            x='Timestamp', 
            y='Temperature', 
            title='Temperature Over Time',
            labels={'Temperature': 'Temperature (°C)'}
        )
        st.plotly_chart(fig_temperature, use_container_width=True)

if __name__ == "__main__":
    main()