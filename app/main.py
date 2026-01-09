from fastapi import FastAPI, HTTPException
from app.schemas import BookingRequest, PredictionResponse
from app.utils import load_model, preprocess_input
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hotel Reservation Prediction API")

# Global variable to store the model
model = None

@app.on_event("startup")
def startup_event():
    global model
    try:
        model = load_model()
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise RuntimeError(f"Could not load model: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Reservation Prediction API. Use /predict for status prediction."}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: BookingRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    try:
        # Convert request to dict
        input_data = request.dict()
        
        # Preprocess input
        df = preprocess_input(input_data)
        
        # Predict
        prediction_code = model.predict(df)[0]
        probabilities = model.predict_proba(df)[0]
        
        # Mapping: {0: 'Canceled', 1: 'Not_Canceled'}
        status_map = {0: 'Canceled', 1: 'Not_Canceled'}
        prediction_label = status_map.get(prediction_code, "Unknown")
        
        # Get probability for the predicted class
        probability = float(probabilities[prediction_code])
        
        return PredictionResponse(
            booking_status=prediction_label,
            probability=probability
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
