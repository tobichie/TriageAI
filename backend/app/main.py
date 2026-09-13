from app.api.routes.health import (
    router as health_router
)

from app.api.routes.triage import (
    router as triage_router
)

import os

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware
)


allowed_origins = (
    os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173"
    ).split(",")
)


app = FastAPI(
    title="TriageAI",
    description=(
        "Prototype clinical triage decision-support system"
    ),
    version="0.1.0"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=allowed_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(
    health_router
)

app.include_router(
    triage_router
)


@app.get("/")
def root():

    return {
        "message": (
            "TriageAI API is running"
        )
    }