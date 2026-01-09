from pydantic import BaseModel
from typing import Literal

# Mappings from training data:
# 'type_of_meal_plan': {'Meal Plan 1': 0, 'Meal Plan 2': 1, 'Meal Plan 3': 2, 'Not Selected': 3}
# 'room_type_reserved': {'Room_Type 1': 0, 'Room_Type 2': 1, 'Room_Type 3': 2, 'Room_Type 4': 3, 'Room_Type 5': 4, 'Room_Type 6': 5, 'Room_Type 7': 6}
# 'market_segment_type': {'Aviation': 0, 'Complementary': 1, 'Corporate': 2, 'Offline': 3, 'Online': 4}

class BookingRequest(BaseModel):
    lead_time: int
    no_of_special_requests: int
    avg_price_per_room: float
    arrival_month: int
    arrival_date: int
    market_segment_type: Literal['Aviation', 'Complementary', 'Corporate', 'Offline', 'Online']
    no_of_week_nights: int
    no_of_weekend_nights: int
    type_of_meal_plan: Literal['Meal Plan 1', 'Meal Plan 2', 'Meal Plan 3', 'Not Selected']
    room_type_reserved: Literal['Room_Type 1', 'Room_Type 2', 'Room_Type 3', 'Room_Type 4', 'Room_Type 5', 'Room_Type 6', 'Room_Type 7']

class PredictionResponse(BaseModel):
    booking_status: Literal['Canceled', 'Not_Canceled']
    probability: float
