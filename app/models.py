# app/models.py

from pydantic import BaseModel

class TextPayload(BaseModel):
    text: str

class WeightsPayload(BaseModel):
    alpha1: float
    alpha2: float
    alpha3: float
    alpha4: float
    alpha5: float
    alpha6: float