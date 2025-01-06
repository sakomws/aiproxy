# app/main.py

import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config
from app.routers import predict, weights

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    openai.api_key = Config.OPENAI_API_KEY

    _app = FastAPI()
    
    # Include routers
    _app.include_router(predict.router, prefix="", tags=["Predict"])
    _app.include_router(weights.router, prefix="", tags=["Weights"])

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # or ["*"] in dev
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Health endpoint
    @_app.get("/health")
    def health():
        return {"status": "ok"}

    return _app

app = create_app()
