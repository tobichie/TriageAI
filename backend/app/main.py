# get structured data from nurse through a form
# Age: Int
# BPM: Int
# Symptoms: List
# Structured Data goes through AI and AI returns structured red flags
from fastapi import FastAPI

from app.api.routes.health import (
    router as health_router
)

from app.api.routes.triage import (
    router as triage_router
)


app = FastAPI(
    title="TriageAI",
    description=(
        "Prototype clinical triage decision-support system"
    ),
    version="0.1.0"
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
        "message": "TriageAI API is running"
    }