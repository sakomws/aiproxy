# app/routers/predict.py

import logging
import openai
from fastapi import APIRouter, HTTPException
from app.config import Config
from app.models import TextPayload
from app.managers.weight_manager import WeightManager
from app.services.rate_limiting import check_rate_limit
from app.services.usage_monitoring import check_cost_limit, update_cost_usage, current_usage_cost
from app.services.scoring import select_best_model

router = APIRouter()

# WeightManager instance
# (In real usage, you'd pass it in via dependency injection or global reference)
weights_manager = WeightManager()

@router.post("/predict")
async def predict(payload: TextPayload):
    # 1) Rate limit
    check_rate_limit()

    # 2) Select best model
    best_model = select_best_model(weights_manager, payload.text)
    chosen_model = best_model["name"]
    model_cost = best_model.get("cost_text", 0.1)

    # 3) Check cost limit (with fallback logic)
    try:
        check_cost_limit(model_cost)
    except HTTPException as e:
        if Config.FALLBACK_MODEL:
            logging.warning("Cost limit reached; trying fallback model.")
            # Fallback is handled in the final code example by searching the registry again
            # For simplicity, just switch to fallback model here:
            if chosen_model != Config.FALLBACK_MODEL:
                chosen_model = Config.FALLBACK_MODEL
                model_cost = 0.05  # Hypothetical cheaper cost
            else:
                # If fallback == chosen model, re-raise the exception
                raise e
        else:
            raise e

    # 4) Invoke the chosen model
    #    Distinguish between OpenAI or Groq
    reply = ""
    if chosen_model.startswith("gpt-") or chosen_model.startswith("text-"):
        # OpenAI model
        try:
            response = openai.ChatCompletion.create(
                model=chosen_model,
                messages=[{"role": "user", "content": payload.text}]
            )
            reply = response["choices"][0]["message"]["content"]
        except openai.error.OpenAIError as oe:
            logging.error(f"OpenAI API error: {oe}")
            raise HTTPException(status_code=502, detail="OpenAI API call failed.")
    elif chosen_model.startswith("groq-"):
        # Hypothetical Groq model call
        reply = f"[Groq mock inference for {chosen_model}] => {payload.text}"
    else:
        # Unknown or not integrated
        reply = f"[Unknown model invocation for {chosen_model}] => {payload.text}"

    # 5) Update usage cost
    update_cost_usage(model_cost)

    return {
        "chosen_model": chosen_model,
        "result": reply,
        "current_usage_cost": current_usage_cost
    }
