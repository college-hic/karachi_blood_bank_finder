import json
import streamlit as st
from geopy.distance import geodesic

# Load Blood Bank Data
with open('blood_banks.json', 'r') as f:
    blood_banks = json.load(f)

# Page Configurations
st.set_page_config(
    page_title="Karachi Blood Bank Finder",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Background Image
page_bg = """
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("images/background.jpg");
    background-size: cover;
    background-position: center;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# App Title
st.title("🩸 Karachi Blood Bank Finder")

# Input Form
st.sidebar.header("Find Nearest Blood Bank")
user_location = st.sidebar.selectbox(
    "Select Your Location",
    ["Saddar", "Gulshan-e-Iqbal", "North Nazimabad", "Korangi", "Clifton", "Gulistan-e-Johar", "Malir", "Nazimabad", "Stadium Road", "Jamshed Town"]
)
required_blood_group = st.sidebar.selectbox(
    "Select Required Blood Group",
    ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
)

# Karachi Locations Coordinates
locations = {
    "Saddar": (24.8556, 67.0226),
    "Gulshan-e-Iqbal": (24.9333, 67.0921),
    "North Nazimabad": (24.9551, 67.0349),
    "Korangi": (24.8450, 67.1396),
    "Clifton": (24.8138, 67.0328),
    "Gulistan-e-Johar": (24.9284, 67.1281),
    "Malir": (24.9000, 67.1855),
    "Nazimabad": (24.9129, 67.0363),
    "Stadium Road": (24.8984, 67.0811),
    "Jamshed Town": (24.8785, 67.0431)
}

# User's Selected Coordinates
user_coords = locations[user_location]

# Find Nearest Blood Bank
def find_nearest_blood_bank(user_coords, required_blood_group):
    nearby_blood_banks = [
        bank for bank in blood_banks if required_blood_group in bank['available_blood_groups']
    ]
    for bank in nearby_blood_banks:
        bank['distance'] = geodesic(user_coords, tuple(bank['coordinates'])).km
    sorted_blood_banks = sorted(nearby_blood_banks, key=lambda x: x['distance'])
    return sorted_blood_banks

nearest_blood_banks = find_nearest_blood_bank(user_coords, required_blood_group)

# Display Results
if nearest_blood_banks:
    st.subheader("Nearest Blood Banks")
    for bank in nearest_blood_banks:
        st.markdown(f"""
        - **Name:** {bank['name']}
        - **Location:** {bank['location']}
        - **Contact:** {bank['contact']}
        - **Email:** {bank['email']}
        - **Available Blood Groups:** {", ".join(bank['available_blood_groups'])}
        - **Distance:** {bank['distance']:.2f} km
        """)
else:
    st.error("No blood banks found with the required blood group.")

# Footer
st.markdown("---")
st.caption("Developed by Karachi Blood Bank Finder Team.")
