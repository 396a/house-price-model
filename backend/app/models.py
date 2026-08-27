from pydantic import BaseModel, Field, field_validator

class PredictionRequest(BaseModel):
    location: str = Field(..., description="Property location")
    carpet_area_sqft: float = Field(..., gt=0, description="Carpet area in square feet")
    floor_num: int = Field(..., ge=-1, description="Floor number (-1 for basement, 0 for ground)")
    bathroom: int = Field(..., ge=0, description="Number of bathrooms")
    balcony: int = Field(..., ge=0, description="Number of balconies")
    car_parking: int = Field(..., ge=0, description="Number of car parking spots")
    furnishing: str = Field(..., description="Furnishing status: Furnished, Semi-Furnished, Unfurnished")
    transaction: str = Field(..., description="Transaction type: New Property, Resale")
    ownership: str = Field(..., description="Ownership type")
    facing: str = Field(..., description="Property facing direction")
    
    @field_validator('furnishing')
    def validate_furnishing(cls, v):
        allowed = ['Furnished', 'Semi-Furnished', 'Unfurnished']
        if v not in allowed:
            raise ValueError(f'furnishing must be one of {allowed}')
        return v
    
    @field_validator('transaction')
    def validate_transaction(cls, v):
        allowed = ['New Property', 'Resale']
        if v not in allowed:
            raise ValueError(f'transaction must be one of {allowed}')
        return v

class PredictionResponse(BaseModel):
    predicted_price: float
    status: str = "success"