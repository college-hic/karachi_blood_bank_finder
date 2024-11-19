import streamlit as st
import json
from geopy.distance import geodesic
import os

# Set page configuration
st.set_page_config(
    page_title="Karachi Blood Bank Finder",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for background image
background_path = os.path.join(os.path.dirname(__file__), "images", "background.jpg")
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("file://{background_path}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(5px);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load Blood Bank Data
with open('blood_banks.json', 'r') as f:
    blood_banks = json.load(f)

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

# App Title
st.title("🩸 Karachi Blood Bank Finder")
st.write("Find the nearest blood bank with the required blood group in Karachi.")

# Sidebar Inputs
st.sidebar.header("Search Blood Banks")
user_location = st.sidebar.selectbox(
    "Select Your Location",
    list(locations.keys())
)
required_blood_group = st.sidebar.selectbox(
    "Select Required Blood Group",
    ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
)

# Interactive Buttons
if st.sidebar.button("Search"):
    # Find Nearest Blood Banks
    user_coords = locations[user_location]

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
    st.subheader("Nearest Blood Banks")
    if nearest_blood_banks:
        for idx, bank in enumerate(nearest_blood_banks):
            with st.expander(f"{idx + 1}. {bank['name']} ({bank['distance']:.2f} km away)"):
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
else:
    st.info("Please click 'Search' to find nearby blood banks.")

# Clear Button
if st.sidebar.button("Clear"):
    st.sidebar.empty()
    st.sidebar.success("Cleared search inputs. Ready for a new search!")

# Footer
st.markdown("---")
st.caption("Developed with ❤️ by Karachi Blood Bank Finder Team.")
