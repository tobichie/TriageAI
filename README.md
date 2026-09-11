# 🏥 TriageAI

> **An explainable clinical triage decision-support prototype combining deterministic rule-based triage with independent AI-assisted assessment.**

Built for the **Munich Hackathon 2026**.

---

# ⚠️ Important Disclaimer

TriageAI is a **hackathon prototype and clinical decision-support concept**.

It is **not a medical device** and must not be used as a replacement for professional medical judgment.

The system:

- Does not diagnose patients
- Does not prescribe treatment
- Does not autonomously make clinical decisions
- Does not replace a triage nurse or physician
- Does not guarantee compliance with the official Manchester Triage System

All results require **human clinical review**.

---

# 🎯 Problem Statement

Emergency departments can become overloaded when patients with different levels of urgency arrive at the same time.

Triage nurses must quickly evaluate:

- Symptoms
- Symptom severity
- Symptom duration
- Vital signs
- Patient age
- Additional clinical context

This process must be performed consistently, often under significant time pressure.

TriageAI explores whether a combination of:

1. **Deterministic and explainable rules**
2. **AI-assisted assessment**
3. **Structured patient input**
4. **Human clinical oversight**

can help create a faster and more transparent clinical decision-support workflow.

---

# 🧠 Project Goal

The goal of TriageAI is to create a prototype that receives structured patient information and produces:

- A deterministic suggested triage priority
- A list of triggered rules
- Relevant factors
- Red flags
- Missing information
- Safety warnings
- An independent AI assessment
- An AI-generated explanation

The most important design principle is:

> **The deterministic system and the AI should not be treated as the same source of information.**

The deterministic engine provides a reproducible and explainable result.

The AI provides an additional independent perspective.

Both outputs are displayed to support human review.

---

# ✨ Current Features

## Backend

- FastAPI REST API
- Pydantic data validation
- Structured patient data
- Deterministic triage engine
- Vital sign evaluation
- Symptom evaluation
- Symptom severity evaluation
- Symptom duration evaluation
- Missing information detection
- Rule findings
- Explainable deterministic results
- Protocol name and version tracking
- AI-assisted severity assessment
- AI-generated reasoning
- AI-generated explanation
- Human review warnings

## Frontend

- React
- Vite
- Structured patient input form
- Dynamic symptom input
- Vital sign input
- Clinical context input
- FastAPI integration
- Deterministic triage result display
- AI assessment display
- AI explanation display
- Modern card-based interface
- Expandable information sections

---

# 🏗️ Current Architecture

```text
                         ┌──────────────────┐
                         │   TRIAGE NURSE   │
                         └────────┬─────────┘
                                  │
                                  ▼
                     ┌──────────────────────┐
                     │   REACT FRONTEND     │
                     │                      │
                     │ • Age                │
                     │ • Symptoms           │
                     │ • Severity           │
                     │ • Duration           │
                     │ • Vital signs        │
                     │ • Clinical context   │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    FASTAPI BACKEND   │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │  PYDANTIC VALIDATION │
                     │                      │
                     │ • Data types         │
                     │ • Value ranges       │
                     │ • Nested models      │
                     └──────────┬───────────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
    ┌────────────────────────┐    ┌────────────────────────┐
    │ DETERMINISTIC ENGINE   │    │     AI COMPONENT       │
    │                        │    │                        │
    │ • Vital sign rules     │    │ • Independent severity │
    │ • Symptom rules        │    │ • AI reasoning         │
    │ • Severity rules       │    │ • Explanation          │
    │ • Duration rules       │    │                        │
    │ • Missing information  │    │                        │
    └────────────┬───────────┘    └────────────┬───────────┘
                 │                             │
                 ▼                             ▼
          TRIAGE RESULT                  AI ASSESSMENT
                 │                             │
                 └──────────────┬──────────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │  FRONTEND DISPLAY    │
                     │                      │
                     │ Deterministic Result │
                     │          ↔           │
                     │ Independent AI View  │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │   HUMAN REVIEW       │
                     │                      │
                     │ Nurse verifies result│
                     └──────────────────────┘

## How an Assessment works

1. Nurse enters patient information
                ↓
2. Frontend creates structured JSON
                ↓
3. FastAPI receives the request
                ↓
4. Pydantic validates the data
                ↓
5. Deterministic triage engine evaluates patient
                ↓
6. AI independently analyzes the patient
                ↓
7. Results are returned to the frontend
                ↓
8. Deterministic and AI results are displayed
                ↓
9. Human clinical review

---

## 📥 Patient Data

The system works with structured patient data.

A patient can currently contain:

- Age
- Symptoms
- Symptom severity
- Symptom duration
- Heart rate
- Oxygen saturation
- Systolic blood pressure
- Diastolic blood pressure
- Clinical context

Example:

{
  "age": 74,

  "symptoms": [
    {
      "name": "chest pain",
      "severity": 8,
      "duration_minutes": 80
    }
  ],

  "vital_signs": {
    "heart_rate": 120,
    "oxygen_saturation": 86,
    "systolic_bp": 120,
    "diastolic_bp": 80
  },

  "clinical_context": "Patient reports persistent symptoms."
}

---

Before the triage engine processes a patient, the incoming data is converted into structured Pydantic models.

HTTP Request
     │
     ▼
 Raw JSON
     │
     ▼
Pydantic Models
     │
     ├── Invalid → Validation Error
     │
     ▼
Validated PatientData
     │
     ▼
Triage Engine

---

## ⚙️ Deterministic Triage Engine

The deterministic engine is the explainable core of TriageAI.

Unlike an AI model, the deterministic engine follows predefined rules.

The same input should always produce the same result.

Same Patient Data
        +
Same Protocol Version
        +
Same Rules
        ↓
Same Result

---

The engine evaluates several categories of information.

PatientData
     │
     ▼
┌──────────────────────┐
│   TRIAGE ENGINE      │
├──────────────────────┤
│ Vital Signs          │
│ Symptoms             │
│ Symptom Severity     │
│ Symptom Duration     │
│ Missing Information  │
└──────────┬───────────┘
           │
           ▼
      Rule Findings
           │
           ▼
   Priority Resolution
           │
           ▼
      TriageResult
