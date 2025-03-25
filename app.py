import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import hashlib

# Simulated doctor credentials (in a real system, use a secure database)
DOCTORS = {
    'admin': {
        'password': hashlib.sha256('password123'.encode()).hexdigest(),
        'name': 'Dr. Admin',
        'department': 'System Administration'
    },
    'johndoe': {
        'password': hashlib.sha256('doctor456'.encode()).hexdigest(),
        'name': 'Dr. John Doe',
        'department': 'Emergency Medicine'
    },
    'janesmit': {
        'password': hashlib.sha256('nurse789'.encode()).hexdigest(),
        'name': 'Dr. Jane Smith',
        'department': 'Intensive Care'
    }
}

# Authentication function
def authenticate(username, password):
    # Hash the input password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Check if username exists and password matches
    if username in DOCTORS and DOCTORS[username]['password'] == hashed_password:
        return DOCTORS[username]
    return None

# Simulated data generation function (replace with actual data source)
def generate_patient_data(num_patients=20):
    patients = []
    triage_colors = ['Green', 'Yellow', 'Orange']
    names = [
        "Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", 
        "Ethan Hunt", "Fiona Gallagher", "George Clooney", "Hannah Montana", 
        "Ian McKellen", "Julia Roberts", "Kevin Hart", "Laura Croft", 
        "Michael Jordan", "Nina Dobrev", "Oscar Wilde", "Penelope Cruz", 
        "Quentin Tarantino", "Rachel Green", "Steve Rogers", "Tina Fey"
    ]
    
    for i in range(num_patients):
        triage_color = np.random.choice(triage_colors, p=[0.5, 0.3, 0.2])
        patient = {
            'Patient ID': f'P{i+1:03d}',
            'Name': names[i % len(names)],  # Cycle through the names list
            'Age': np.random.randint(18, 85),
            'Triage Color': triage_color,
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

# Login Page
def login_page():
    st.title("Smart Triage Bracelet Dashboard")
    st.subheader("Doctor Login")
    
    # Login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Authenticate user
        user = authenticate(username, password)
        
        if user:
            # Store user info in session state
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_info = user
            st.rerun()
        else:
            st.error("Invalid username or password")

# Logout function
def logout():
    # Clear session state
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_info = None
    st.rerun()



def load_patient_data(file_path):
    """
    Load patient data from CSV file with error handling
    """
    try:
        # Use pandas to read the CSV file
        df = pd.read_csv(file_path)
        
        # Optional: Add timestamp to show when data was last updated
        df['last_updated'] = pd.Timestamp.now()
        
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return pd.DataFrame()  # Return empty DataFrame if load fails


# Streamlit app configuration
def main():
    st.set_page_config(
        page_title="Smart Triage Bracelet Dashboard",
        page_icon=":hospital:",
        layout="wide"
    )
    
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()
        return
    
    # Add logout functionality
    st.sidebar.title("User Information")
    st.sidebar.write(f"Logged in as: {st.session_state.user_info['name']}")
    st.sidebar.write(f"Department: {st.session_state.user_info['department']}")
    
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        logout()
        return
    
    # App title
    st.title("Smart Triage Bracelet Patient Monitoring System")
    
    # Generate patient data
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = generate_patient_data()
    patient_data = st.session_state.patient_data
    
    # Calculate triage color metrics
    triage_metrics = patient_data['Triage Color'].value_counts()
    
    # Color mapping for triage status
    color_map = {
        'Green': '#4CAF50',   # Green
        'Yellow': '#FFC107',  # Amber
        'Orange': '#FF5722'   # Orange
    }
    
    # Create a row for triage metrics with color-coded styling
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        # Green patients with green styling
        st.markdown(f"""
        <div style="background-color: rgba(76, 175, 80, 0.1); 
                    border: 2px solid {color_map['Green']}; 
                    border-radius: 10px; 
                    padding: 10px; 
                    text-align: center;">
            <h3 style="color: {color_map['Green']}; margin-bottom: 5px;">Green Patients</h3>
            <div style="font-size: 2.5em; 
                        color: {color_map['Green']}; 
                        font-weight: bold;">
                {triage_metrics.get('Green', 0)}
            </div>
            <p style="color: {color_map['Green']}; margin-top: 5px;">Stable Condition</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        # Yellow patients with yellow styling
        st.markdown(f"""
        <div style="background-color: rgba(255, 193, 7, 0.1); 
                    border: 2px solid {color_map['Yellow']}; 
                    border-radius: 10px; 
                    padding: 10px; 
                    text-align: center;">
            <h3 style="color: {color_map['Yellow']}; margin-bottom: 5px;">Yellow Patients</h3>
            <div style="font-size: 2.5em; 
                        color: {color_map['Yellow']}; 
                        font-weight: bold;">
                {triage_metrics.get('Yellow', 0)}
            </div>
            <p style="color: {color_map['Yellow']}; margin-top: 5px;">Needs Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        # Orange patients with orange styling
        st.markdown(f"""
        <div style="background-color: rgba(255, 87, 34, 0.1); 
                    border: 2px solid {color_map['Orange']}; 
                    border-radius: 10px; 
                    padding: 10px; 
                    text-align: center;">
            <h3 style="color: {color_map['Orange']}; margin-bottom: 5px;">Orange Patients</h3>
            <div style="font-size: 2.5em; 
                        color: {color_map['Orange']}; 
                        font-weight: bold;">
                {triage_metrics.get('Orange', 0)}
            </div>
            <p style="color: {color_map['Orange']}; margin-top: 5px;">Critical Condition</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tracking state
    if 'selected_patient_id' not in st.session_state:
        st.session_state.selected_patient_id = None
    
    # Patient Details Section when a patient is selected
    if st.session_state.selected_patient_id:
        # Filter selected patient
        selected_patient = patient_data[patient_data['Patient ID'] == st.session_state.selected_patient_id].iloc[0]
        
        st.header(f"Patient {selected_patient['Patient ID']} Details")
        
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
        time_series_data = generate_time_series_data(st.session_state.selected_patient_id)
        
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
        
        # Add a button to go back to patient overview
        if st.button("Back to Patient Overview"):
            st.session_state.selected_patient_id = None
            st.rerun()
    
    # Patient Overview Section (shown when no patient is selected)
    else:
        st.header("Patient Overview")
        patient_grid = st.container()
        
        with patient_grid:
            # Use columns to create a responsive grid
            cols = st.columns(3)
            
            for i, (_, patient) in enumerate(patient_data.iterrows()):
                # Determine the column for this patient
                col = cols[i % 3]
                
                with col:
                    # Color mapping with slightly lighter shades for background
                    color_map_bg = {
                        'Green': '#F4FFF4',   # Lighter Green
                        'Yellow': '#FFFBE6',  # Lighter Yellow
                        'Orange': '#FFF2F0'   # Lighter Orange
                    }
                    
                    # Card-like display with consistent styling
                    card_style = f"""
                    background-color: white;
                    border: 3px solid {color_map[patient['Triage Color']]};
                    border-radius: 10px;
                    padding: 0;
                    margin-bottom: 15px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    overflow: hidden;
                    """
                    
                    # Status bar style
                    status_bar_style = f"""
                    background-color: {color_map[patient['Triage Color']]};
                    color: white;
                    padding: 10px;
                    text-align: center;
                    font-weight: bold;
                    """
                    
                    # Card content style
                    content_style = f"""
                    padding: 15px;
                    background-color: {color_map_bg[patient['Triage Color']]};
                    """
                    
                    # Use st.markdown to create a card with prominent status
                    card_html = f"""
                    <div style="{card_style}">
                        <div style="{status_bar_style}">
                            {patient['Name']} 
                        </div>
                        <div style="{content_style}">
                            <h4>{patient['Name']}</h4>
                            <p><strong>👵🏻 Age:</strong> {patient['Age']}</p>
                            <p><strong>🫀 Heart Rate:</strong> {patient['Heart Rate']} bpm</p>
                            <p><strong>🌡️ Temp:</strong> {patient['Temperature']}°C</p>
                        </div>
                    </div>
                    """
                    
                    # Button to select patient
                    selected = st.button(f"Select {patient['Name']}", 
                                         key=f"select_{patient['Patient ID']}", 
                                         type='primary', 
                                         use_container_width=True)
                    
                    # Render the card
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Handle patient selection
                    if selected:
                        st.session_state.selected_patient_id = patient['Patient ID']
                        st.rerun()

if __name__ == "__main__":
    main()