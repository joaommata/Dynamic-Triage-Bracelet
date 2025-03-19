import streamlit as st
import pandas as pd
import numpy as np

# Custom CSS for rounded patient cards
st.markdown(
    """
    <style>
        .patient-card {
            border-radius: 15px;
            padding: 15px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin: 10px;
            text-align: center;
        }
        .patient-info {
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title of the app
st.title("Patient Dashboard")

# Example patient data
data = [
    {"name": "John Doe", "age": 45, "file": "ppg_data.csv"},
    {"name": "Jane Smith", "age": 52, "file": "ppg_data.csv"},
    {"name": "Alice Johnson", "age": 38, "file": "ppg_data.csv"},
]

# Display patient cards vertically
for patient in data:
    # Load patient data
    try:
        df = pd.read_csv(patient["file"])
        ppg = df.iloc[:, 1]
    except FileNotFoundError:
        st.error(f"File not found: {patient['file']}")
        continue

    # Create a container for each patient card
    with st.container():
        st.markdown(f"""
            <div class='patient-card'>
                <div class='patient-info'>
                    <h3>{patient['name']}</h3>
                    <p>Age: {patient['age']}</p>
                </div>
                <div>
                    """, unsafe_allow_html=True)
        st.line_chart(ppg)
        st.markdown("</div></div>", unsafe_allow_html=True)