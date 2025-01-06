# app/services/usage_monitoring.py

from fastapi import HTTPException, status
from app.config import Config

# In-memory global usage cost
current_usage_cost = 0.0

def check_cost_limit(model_cost: float) -> None:
    """
    Check if adding this model's cost would exceed the monthly budget.
    """
    global current_usage_cost
    projected_cost = current_usage_cost + model_cost
    if projected_cost > Config.MAX_MONTHLY_BUDGET:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Cost limit exceeded. Please upgrade your plan or reduce usage."
        )

def update_cost_usage(model_cost: float) -> None:
    global current_usage_cost
    current_usage_cost += model_cost