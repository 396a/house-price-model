from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import joblib
import pandas as pd
import json
import os
from dotenv import load_dotenv
from app.models import PredictionRequest, PredictionResponse
from app.services.preprocessing import prepare_features

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "..\models\house_price.pkl")
LOCATIONS_PATH = os.getenv("LOCATIONS_PATH", ".\locations.json")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        model = None
    
    try:
        with open(LOCATIONS_PATH, 'r') as f:
            locations = json.load(f)
            print(f"✅ Loaded {len(locations)} locations")
    except Exception as e:
        print(f"❌ Failed to load locations: {e}")
    
    yield

app = FastAPI(
    title="House Price Prediction API",
    description="Predict house prices using machine learning",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "House Price Prediction API",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/locations", tags=["Locations"])
async def get_locations():
    try:
        with open(LOCATIONS_PATH, 'r') as f:
            locations = json.load(f)
        return {"locations": locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    try:
        features = prepare_features(request)
        prediction = model.predict(features)[0]
        return PredictionResponse(
            predicted_price=float(prediction),
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))