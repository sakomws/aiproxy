# app/routers/weights.py

import logging
from fastapi import APIRouter, Depends
from app.models import WeightsPayload
from app.config import Config
from app.managers.weight_manager import WeightManager
from fastapi import HTTPException, status

router = APIRouter()
weights_manager = WeightManager()

def verify_api_key(api_key: str):
    """
    Simple dependency to verify an API key for weight updates.
    """
    if api_key != Config.API_KEY_FOR_UPDATES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

@router.post("/update_weights")
async def update_weights(
    weights: WeightsPayload,
    api_key: str = Depends(verify_api_key)
):
    weights_manager.set_weights(
        weights.alpha1,
        weights.alpha2,
        weights.alpha3,
        weights.alpha4,
        weights.alpha5,
        weights.alpha6
    )
    logging.info(f"Updated weights: {weights}")

    return {
        "message": "Weights updated successfully",
        "new_weights": weights
    }
