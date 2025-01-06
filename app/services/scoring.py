# app/services/scoring.py

import openai
from fastapi import HTTPException
from app.managers.weight_manager import WeightManager
from app.services.model_registry import model_registry

def compute_input_complexity(text: str) -> float:
    """
    Simple approach:
    - 1.0 if text >= 1000 chars; else text_len/1000
    """
    max_length = 1000
    length = len(text)
    return min(1.0, length / max_length)

def calculate_score(weights_manager: WeightManager, model: dict, input_text: str) -> float:
    """
    S(M_j|X) = alpha1*Acc - alpha2*Lat - alpha3*Cost
               - alpha4*Load + alpha5*Comp + alpha6*Conf
    """
    alpha1, alpha2, alpha3, alpha4, alpha5, alpha6 = weights_manager.get_weights()

    acc  = model.get("acc_text", 0.0)
    lat  = model.get("lat_text", 1.0)
    cost = model.get("cost_text", 1.0)
    load = model.get("load", 1.0)
    conf = model.get("conf_text", 0.0)
    comp = compute_input_complexity(input_text)

    return (
        alpha1 * acc
        - alpha2 * lat
        - alpha3 * cost
        - alpha4 * load
        + alpha5 * comp
        + alpha6 * conf
    )

def select_best_model(weights_manager: WeightManager, input_text: str) -> dict:
    """
    Iterate over the entire registry, find the model with the highest score.
    Raise HTTPException if no models exist.
    """
    best_model = None
    best_score = float("-inf")

    for model in model_registry:
        score = calculate_score(weights_manager, model, input_text)
        if score > best_score:
            best_score = score
            best_model = model

    if not best_model:
        raise HTTPException(status_code=500, detail="No models available.")
    return best_model