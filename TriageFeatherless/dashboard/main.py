from typing import Optional
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db.db import (
    VALID_STATUSES,
    delete_patient,
    get_patient,
    get_stats,
    list_patients,
    set_status,
    update_patient,
)


# --------------------------------------------------
# Application
# --------------------------------------------------

app = FastAPI(
    title="TriageAI Dashboard API",
    description="Read/update/delete API for TriageAI patient records.",
    version="0.2.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Request models
# --------------------------------------------------

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    symptoms: Optional[list] = None
    vital_signs: Optional[dict] = None
    clinical_context: Optional[str] = None


class StatusUpdate(BaseModel):
    status: str


# --------------------------------------------------
# Root / health
# --------------------------------------------------

@app.get("/")
def root():
    return {"message": "TriageAI Dashboard API is running"}


# --------------------------------------------------
# Statistics
# --------------------------------------------------

@app.get("/stats")
def stats():
    return get_stats()


# --------------------------------------------------
# Patients (read)
# --------------------------------------------------

@app.get("/patients")
def get_patients(include_done: bool = True):
    return list_patients(include_done=include_done)


@app.get("/patients/{patient_id}")
def read_patient(patient_id: int):
    patient = get_patient(patient_id)

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


# --------------------------------------------------
# Patients (update)
#
# Note: there is intentionally no "create" endpoint here.
# New rows are only created by the main /triage endpoint.
# --------------------------------------------------

@app.put("/patients/{patient_id}")
def edit_patient(patient_id: int, changes: PatientUpdate):
    if get_patient(patient_id) is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    updated = update_patient(
        patient_id,
        changes.model_dump(exclude_none=True),
    )

    return updated


@app.patch("/patients/{patient_id}/status")
def change_status(patient_id: int, payload: StatusUpdate):
    if payload.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. Expected one of: "
                + ", ".join(sorted(VALID_STATUSES))
            ),
        )

    if get_patient(patient_id) is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return set_status(patient_id, payload.status)


# --------------------------------------------------
# Patients (delete)
# --------------------------------------------------

@app.delete("/patients/{patient_id}")
def remove_patient(patient_id: int):
    deleted = delete_patient(patient_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"deleted": patient_id}
