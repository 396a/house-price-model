import pandas as pd
import json
import os
from app.models import PredictionRequest

LOCATIONS_PATH = os.getenv("LOCATIONS_PATH", "./locations.json")
try:
    with open(LOCATIONS_PATH, 'r') as f:
        VALID_LOCATIONS = json.load(f)
except:
    VALID_LOCATIONS = []

def prepare_features(request: PredictionRequest) -> pd.DataFrame:
    location = request.location
    if location not in VALID_LOCATIONS:
        location = 'other'
    
    data = {
        'carpet_area_sqft': [request.carpet_area_sqft],
        'floor_num': [request.floor_num],
        'bathroom': [request.bathroom],
        'balcony': [request.balcony],
        'car_parking': [request.car_parking],
        'location_grouped': [location],
        'Furnishing': [request.furnishing],
        'Transaction': [request.transaction],
        'Ownership': [request.ownership],
        'facing': [request.facing]
    }
    
    df = pd.DataFrame(data)
    return df