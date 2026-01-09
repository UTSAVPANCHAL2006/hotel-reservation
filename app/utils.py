import joblib
import pandas as pd
import os

# Mappings from training data
MAPPINGS = {
    'type_of_meal_plan': {'Meal Plan 1': 0, 'Meal Plan 2': 1, 'Meal Plan 3': 2, 'Not Selected': 3},
    'room_type_reserved': {'Room_Type 1': 0, 'Room_Type 2': 1, 'Room_Type 3': 2, 'Room_Type 4': 3, 'Room_Type 5': 4, 'Room_Type 6': 5, 'Room_Type 7': 6},
    'market_segment_type': {'Aviation': 0, 'Complementary': 1, 'Corporate': 2, 'Offline': 3, 'Online': 4},
}

MODEL_PATH = "artifacts/models/lgbm_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def preprocess_input(data: dict) -> pd.DataFrame:
    # Convert string categories to codes using MAPPINGS
    processed_data = data.copy()
    for col, mapping in MAPPINGS.items():
        if col in processed_data:
            processed_data[col] = mapping.get(processed_data[col], -1)
    
    # Create DataFrame in the exact order as training features
    # Order: lead_time, no_of_special_requests, avg_price_per_room, arrival_month, arrival_date, market_segment_type, no_of_week_nights, no_of_weekend_nights, type_of_meal_plan, room_type_reserved
    feature_order = [
        'lead_time', 'no_of_special_requests', 'avg_price_per_room', 'arrival_month', 
        'arrival_date', 'market_segment_type', 'no_of_week_nights', 
        'no_of_weekend_nights', 'type_of_meal_plan', 'room_type_reserved'
    ]
    
    df = pd.DataFrame([processed_data])[feature_order]
    return df
