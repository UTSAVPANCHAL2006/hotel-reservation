import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="Hotel Reservation Predictor",
    page_icon="🏨",
    layout="centered"
)

# Custom CSS for rich aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }
    .prediction-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .status-canceled {
        color: #dc3545;
        font-weight: bold;
        font-size: 24px;
    }
    .status-not-canceled {
        color: #28a745;
        font-weight: bold;
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏨 Hotel Reservation Predictor")
st.markdown("Enter reservation details below to predict the booking status.")

# Form for input
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        lead_time = st.number_input("Lead Time (days)", min_value=0, value=26)
        no_of_special_requests = st.number_input("Number of Special Requests", min_value=0, value=0)
        avg_price_per_room = st.number_input("Avg Price Per Room", min_value=0.0, value=161.0)
        arrival_month = st.slider("Arrival Month", 1, 12, 10)
        arrival_date = st.slider("Arrival Date", 1, 31, 17)
        
    with col2:
        market_segment_type = st.selectbox("Market Segment Type", 
                                         ['Aviation', 'Complementary', 'Corporate', 'Offline', 'Online'], 
                                         index=4)
        no_of_week_nights = st.number_input("Number of Week Nights", min_value=0, value=1)
        no_of_weekend_nights = st.number_input("Number of Weekend Nights", min_value=0, value=2)
        type_of_meal_plan = st.selectbox("Type of Meal Plan", 
                                      ['Meal Plan 1', 'Meal Plan 2', 'Meal Plan 3', 'Not Selected'], 
                                      index=0)
        room_type_reserved = st.selectbox("Room Type Reserved", 
                                       ['Room_Type 1', 'Room_Type 2', 'Room_Type 3', 'Room_Type 4', 'Room_Type 5', 'Room_Type 6', 'Room_Type 7'], 
                                       index=0)

    submit_button = st.form_submit_button(label="Predict Booking Status")

if submit_button:
    # Prepare payload
    payload = {
        "lead_time": lead_time,
        "no_of_special_requests": no_of_special_requests,
        "avg_price_per_room": avg_price_per_room,
        "arrival_month": arrival_month,
        "arrival_date": arrival_date,
        "market_segment_type": market_segment_type,
        "no_of_week_nights": no_of_week_nights,
        "no_of_weekend_nights": no_of_weekend_nights,
        "type_of_meal_plan": type_of_meal_plan,
        "room_type_reserved": room_type_reserved
    }
    
    try:
        # Call FastAPI backend
        response = requests.post("http://localhost:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            status = result["booking_status"]
            prob = result["probability"]
            
            st.markdown("---")
            st.subheader("Prediction Analysis")
            
            # Show probability bar
            st.write(f"Confidence Level: **{prob:.1%}**")
            st.progress(prob)

            if status == "Canceled":
                st.markdown(f'<div class="prediction-card"><span class="status-canceled">Predicted Status: {status}</span></div>', unsafe_allow_html=True)
                st.error("Caution: This reservation is likely to be canceled.")
            else:
                st.markdown(f'<div class="prediction-card"><span class="status-not-canceled">Predicted Status: {status}</span></div>', unsafe_allow_html=True)
                st.success("Safe: This reservation is likely to be honored.")
        else:
            st.error(f"Error: Unable to get prediction from backend. (Status Code: {response.status_code})")
            st.info("Make sure the FastAPI server is running at http://localhost:8000")
            
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to the FastAPI backend. Please ensure it is running.")
