"""
Main application entry point for FastAPI service.

This script sets up the FastAPI app, configures CORS middleware using allowed origins
from environment variables, and includes the API router.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from routes import router

load_dotenv()

# Read allowed origins and split by comma
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Optional: strip whitespace from each origin
origins = [origin.strip() for origin in origins if origin.strip()]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
app.include_router(router)

