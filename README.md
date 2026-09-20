# 🏥 TriageAI

> **An explainable clinical triage decision-support prototype combining a deterministic rule-based triage engine with independent AI-assisted assessment and supplementary knowledge retrieval.**

Built for the **Munich Hackathon 2026**.

---

## ⚠️ Important Disclaimer

TriageAI is a **prototype for clinical decision support**.

It is **not a medical device** and must not be used as a replacement for professional medical judgment.

The system:

- Does not diagnose patients
- Does not prescribe or recommend treatment
- Does not autonomously make clinical decisions
- Does not replace healthcare professionals
- Does not guarantee compliance with the official Manchester Triage System

**All assessments require human clinical review.**

---

# 🎯 Problem

Clinical triage requires healthcare professionals to rapidly evaluate patients with different levels of urgency.

Relevant information may include:

- Patient age
- Reported symptoms
- Symptom severity
- Symptom duration
- Vital signs
- Clinical context

Triage decisions must be made using incomplete and potentially complex information.

TriageAI explores how a combination of:

- Structured patient data
- Deterministic and inspectable rules
- Independent AI-assisted assessment
- Supplementary knowledge retrieval
- Explainable output

can support a more transparent clinical decision-support workflow.

---

# 🧠 Solution / Project Goal

TriageAI deliberately separates its deterministic and AI-assisted components.

The system contains:

1. A **deterministic rule-based triage engine**
2. An **independent AI assessment**
3. An **AI-generated explanation of the deterministic result**
4. An optional **supplementary knowledge base**

The core architectural principle is:

> **AI output does not override the deterministic triage result.**

The deterministic engine remains responsible for producing the deterministic suggested triage group. The AI components provide an additional perspective and explanation.

This separation makes it possible to:

- Inspect deterministic rule findings
- Identify which rules contributed to a result
- Produce reproducible deterministic results
- Compare deterministic and AI-assisted assessments
- Identify potential information not represented by the current deterministic rules
- Keep supplementary retrieved information separate from deterministic evidence

The exact AI provider and model are implementation-specific. See:
- [Featherless implementation](TriageFeatherless/README-FEATHERLESS.md)
- [OpenAI implementation](TriageAI/README-OPENAI.md)

---

# 🆕 Current Build

The September 2026 build expanded the original prototype with:

| Area | Current implementation |
|------|------------------------|
| Persistence | Full triage result + name + status + timestamps stored per encounter |
| Patient identity | `name` field, stored locally and never sent to the AI |
| Dashboard API | Full read / update / delete + status + statistics |
| Frontend | Three views: **Assess**, **Board**, **Records** |
| Nurse input | Pain sliders, symptom quick-pick chips, name field |
| Shift overview | Triage board sorted by urgency with live wait timers |
| Re-assessment | Pre-fills the intake form from a stored patient |
| Theme | Light / dark toggle, persisted per device |
| Reboot safety | `restart: unless-stopped` on services |
| Services | Frontend + backend + dashboard + PostgreSQL |

---

# ✨ Current Features

## Workflow & Dashboard

- Every assessment is persisted: patient data and triage result
- Patient name / identifier is stored locally and never sent to the AI
- Triage board with patients sorted by urgency
- Colour-coded urgency and live waiting time
- Overdue indicator
- Patient status workflow: `waiting → in_treatment → done`
- Records / admin view with view, edit, delete, re-assess and statistics
- Re-assessment pre-fills the intake form
- Light / dark mode toggle for night shifts

## Deterministic Triage Engine

- Five-level triage priority system
- Structured patient input
- Patient age
- Symptom evaluation
- Symptom normalization
- Symptom aliases
- Symptom severity evaluation
- Symptom duration evaluation
- Vital-sign evaluation
- Red-flag evaluation
- Missing-information detection
- Structured rule findings
- Triggered-rule reporting
- Relevant-factor reporting
- Priority resolution
- Protocol name and version information
- Human-review requirement

## AI-Assisted Components

The AI layer is intentionally independent from the deterministic engine.

It provides:

- Independent AI-assisted assessment
- Separate AI-generated reasoning
- AI explanation of the deterministic result
- AI / deterministic assessment comparison
- Structured validation of AI assessment output
- Potential identification of information not represented by the current deterministic rules

The provider, model, authentication and retrieval configuration are implementation-specific.

---

## 🗒️ Note 

Where supported by the configured AI provider, repeated structured requests may benefit from prompt caching, reducing repeated processing and potentially improving response latency.
![cache_hits.png](demo/cache_hits.png)

## Performance Improvement

The frontend currently waits for both the **AI Assessment** and the **Engine Assessment** to complete before displaying any results. This unnecessarily increases the perceived duration of the triage process.

This can (I'm not doing it) be changed so that the **Engine Assessment is displayed immediately once it is available**, while the AI Assessment continues processing in the background.

---

## Known Vulnerabilities

### Prompt Engineering

The prompts defined in `backend/app/explainability/prompts.py` are currently not hardened against prompt injection or other prompt-engineering techniques.

This could potentially allow users to manipulate the model into generating responses unrelated to the intended triage process. Prompt hardening, stricter input handling, and clear model instructions should be implemented to reduce this risk.

### Clinical Context Overload

The **Clinical Context** field currently accepts an unrestricted number of characters. This allows users to submit excessively large amounts of text, which can unnecessarily increase token consumption and processing time.

A maximum input length should be introduced to prevent excessive token usage and ensure consistent performance. Additional validation or truncation mechanisms may also be considered.

---
# 🚀 Quick Start

## Prerequisites

You need:

-   Docker Desktop
-   Git
-   The required AI service credentials

Make sure Docker Desktop is running before starting the project.

## 1. Clone the Repository

``` bash
git clone https://github.com/tobichie/TriageAI.git
cd TriageAI/TriageAI OR TriageFeatherless
```

## 2. Configure Environment Variables

Create a `.env` file in the project root.

Example:

``` env
FEATHERLESS_KEY=your_api_key OR OPENAI_API_KEY=your_api_key
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://<host_ip>:5173

# PostgreSQL (used by backend + dashboard)
POSTGRES_DB=triageai
POSTGRES_USER=triageai
POSTGRES_PASSWORD=change_me
DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```
If allowed origins are not configured only the localhost will be able to reach the service.

If no vector store ID is configured, the service can continue without
attaching the vector-store file-search tool.

### API URL configuration

The frontend reaches the backend and dashboard through two base URLs, both of
which default to a **relative path**:

| Variable | Default | Used by |
|----------|---------|---------|
| `VITE_API_URL` | `/api` | Main API (`POST /triage`) |
| `VITE_DASHBOARD_API_URL` | `/dashboard-api` | Dashboard API (records, board, stats) |

**Recommended (default): relative paths.**
The frontend uses relative API URLs so requests stay on the same origin:

- `VITE_API_URL=/api`
- `VITE_DASHBOARD_API_URL=/dashboard-api`

In the current hosted setup, the nginx reverse proxy maps the site's
`/api/` path to the backend service on port `8000` and `/dashboard-api/` to the
dashboard API on port `8001`. This is why the frontend can use relative paths
instead of hard-coding backend hostnames or ports.

For direct local development, the equivalent path routing is provided by the
Vite proxies defined in `frontend/vite.config.js`.

Because the API paths are same-origin in the hosted setup, the browser sends
requests to the same domain as the frontend.

**Optional override: absolute URL (bypass the proxy).**
If you ever want the frontend to talk to the backend directly (no proxy), set
absolute URLs in `frontend/.env` and rebuild the frontend:

```env
VITE_API_URL=/api
VITE_DASHBOARD_API_URL=/dashboard-api
ALLOWED_ORIGINS=<yourdomain/ip+port>
```

In this mode the request is cross-origin, so you must add the frontend origin to
`ALLOWED_ORIGINS` (CORS), and Basic Auth on `/api` no longer applies
automatically. Prefer the relative default unless you have a specific reason.

> Never commit API keys or secrets to Git.

## 3. Build and Start TriageAI

From either the TriageAI or TriageFeatherless directory depending on which is in use:

``` bash
docker compose up -d --build
```

## 4. Check the Containers

``` bash
docker compose ps
```

## 5. Open the Application

Frontend:

``` text
http://localhost:5173
```

Backend API:

``` text
http://localhost:8000
```

Swagger UI:

``` text
http://localhost:8000/docs
```

ReDoc:

``` text
http://localhost:8000/redoc
```

------------------------------------------------------------------------

# 🛑 Stopping TriageAI

``` bash
docker compose down
```

------------------------------------------------------------------------

# 🔄 Rebuilding After Changes

When source files or Docker configuration have changed:

``` bash
docker compose up -d --build
```

------------------------------------------------------------------------

# 📜 Viewing Logs

View logs:

``` bash
docker compose logs
```

Follow logs:

``` bash
docker compose logs -f
```

View backend logs:

``` bash
docker compose logs -f backend
```

View frontend logs:

``` bash
docker compose logs -f frontend
```

------------------------------------------------------------------------

# 🔄 How an Assessment Works

```text
1. Patient information is submitted
              ↓
2. Structured input is validated
              ↓
3. Deterministic triage engine evaluates the data
              ↓
4. Missing information and safety status are evaluated
              ↓
5. Independent AI assessment is generated
              ↓
6. Supplementary knowledge may be retrieved when supported/configured
              ↓
7. AI explanation explains the deterministic result
              ↓
8. Deterministic and AI assessments are compared
              ↓
9. Results are presented for human review
```

---

# 📥 Structured Patient Information

TriageAI accepts structured patient information including:

- Name / identifier (optional; stored locally, never sent to the AI)
- Age
- Symptoms
- Symptom severity
- Symptom duration
- Heart rate
- Systolic blood pressure
- Diastolic blood pressure
- Oxygen saturation
- Clinical context

A symptom contains structured information such as:

```json
{
  "name": "chest pain",
  "severity": 5,
  "duration_minutes": 20
}
```

Severity is represented on a numerical scale:

```text
1 → lowest severity
10 → highest severity
```

---

# ⚙️ Deterministic Triage Engine

The deterministic engine evaluates patient information using predefined Python rules.

Its purpose is to produce a reproducible and inspectable result.

The engine evaluates categories including:

```text
Patient Data
│
├── Symptoms
│   ├── Name normalization
│   ├── Aliases
│   ├── Critical symptoms
│   ├── Very urgent symptoms
│   ├── Urgent symptoms
│   ├── Severity
│   └── Duration
│
├── Vital Signs
│   ├── Oxygen saturation
│   ├── Heart rate
│   └── Blood pressure
│
├── Red Flags
│
└── Missing Information
```

---

# 🚦 Five-Level Triage System

TriageAI currently uses a five-level priority system:

```text
Group 1 → Immediate
Group 2 → Very Urgent
Group 3 → Urgent
Group 4 → Normal
Group 5 → Not Urgent
```

The system also associates groups with:

- Treatment priority
- Colour
- Maximum wait time
- Reevaluation interval

Group `1` represents the highest urgency.

Group `5` represents the lowest urgency.

---

# 🧾 Rule Findings

The deterministic engine produces structured rule findings.

A finding can contain:

```text
rule_id
category
description
observed_value
threshold
comparison
suggested_group
```

This information makes the deterministic result inspectable and explainable.

Example:

```text
Rule:
SYMPTOM_CHEST_PAIN_URGENT

Observed value:
5

Threshold:
5

Comparison:
5 >= 5

Suggested group:
3
```

The exact rule findings depend on the submitted patient data and currently implemented rules.

---

# 🫁 Vital Signs and Red Flags

The deterministic engine evaluates available vital signs:

- Oxygen saturation
- Heart rate
- Blood pressure

The engine also contains a separate red-flag evaluation component.

Triggered findings are represented as structured rule findings and can contribute to priority resolution.

---

# ❓ Missing Information

The system evaluates whether important structured information is missing.

The current missing-information logic checks for information including:

- Age
- Symptoms
- Heart rate
- Systolic blood pressure
- Diastolic blood pressure
- Oxygen saturation

Missing information contributes to the assessment's safety information.

---

# 🤖 Independent AI Assessment

TriageAI generates an independent AI-assisted assessment.

The AI receives structured patient information and produces a structured result such as:

```json
{
  "severity": 3,
  "reason": "Short explanation based on the available information."
}
```

The returned AI result is validated before being returned by the service.

> **The AI assessment does not replace or override the deterministic engine.**

---

# 🧠 AI Explanation

The AI explanation component explains the deterministic engine result.

It uses structured context including:

```text
Patient Data

Deterministic Engine Result
├── Protocol information
├── Suggested group
├── Treatment priority
├── Color
├── Wait information
├── Rule findings
├── Triggered rules
├── Red flags
└── Relevant factors

Safety Information
├── Missing information
├── Assessment status
├── Safety warnings
└── Human-review requirement
```

The explanation is intended to clarify:

- What patient information was provided
- Which deterministic rules were triggered
- Why structured rules were triggered
- How findings contributed to the deterministic result
- Relevant factors
- Missing information
- Safety warnings

---

# ⚠️ Potential Issues Not Recognized by the Deterministic Engine

The AI explanation component may identify potentially relevant information that does not appear to have triggered a deterministic rule.

Such observations must be clearly labelled:

> **Potential issue not recognized by the deterministic engine.**

This does **not** mean that:

- A diagnosis was made
- An additional deterministic rule was triggered
- The AI changed the deterministic result

Instead, this mechanism is intended to support:

- Human clinical review
- Identification of potential gaps in the deterministic rule system
- Future deterministic rule development

---

# 🔒 Why the AI Cannot Override the Engine

The deterministic engine and AI are intentionally separated.

```text
Patient Data
     │
     ├──────────────────────┐
     │                      │
     ▼                      ▼
Deterministic Engine      AI Assessment
     │                      │
     ▼                      ▼
Deterministic Result      Supplementary Result
     │                      │
     └──────────┬───────────┘
                │
                ▼
            Comparison
                │
                ▼
            Human Review
```

The AI does not:

- Modify deterministic rules
- Trigger deterministic rules
- Change rule findings
- Override the deterministic triage group
- Become the authoritative deterministic result

---

# 🔀 Assessment Comparison

The frontend compares:

```text
Deterministic Suggested Group

vs.

Independent AI Suggested Group
```

If both values match:

```text
Both assessments align
```

If they differ:

```text
Assessment disagreement
Human review is required.
```

The comparison is informational.

A disagreement does not automatically modify either assessment.

---

# 🌐 Backend API

TriageAI uses a FastAPI backend.

When running locally:

```text
Swagger UI
http://localhost:8000/docs
```

```text
ReDoc
http://localhost:8000/redoc
```

## Main API — port 8000

- `POST /triage` — runs the deterministic engine + independent AI assessment, stores the full encounter, and returns the result plus `patient_id`
- `GET /health`

New patient rows are created only through `/triage`.

## Dashboard API — port 8001

Read / update / delete only — there is intentionally no create endpoint.

```text
GET    /patients?include_done=true
GET    /patients/{id}
PUT    /patients/{id}
PATCH  /patients/{id}/status
DELETE /patients/{id}
GET    /stats
```

Board ordering is by `triage_group` ascending (1 = most urgent, NULLs last), then `created_at` ascending (longest wait first).

---

# ⚛️ Frontend

The frontend is built with React and Vite. It has three views plus a light / dark mode toggle.

```text
TriageAI
│
├── Assess
│   ├── Name / identifier
│   ├── Age
│   ├── Symptoms
│   ├── Vital Signs
│   ├── Clinical Context
│   └── Result and explanation
│
├── Board
│   ├── Patients sorted by urgency
│   ├── Live waiting time
│   └── Status flow
│
└── Records
    ├── Statistics
    ├── View · Edit · Delete
    └── Re-assess
```

Shared priority / formatting logic lives in `frontend/src/triage.js`.

Re-assess loads stored patient data back into the intake form and switches to the Assess view; submitting produces a fresh assessment through `/triage`.

### 🌙 Dark mode

The light/dark choice is stored per device using `localStorage` and defaults to the operating-system preference.

---

# 🐳 Docker

TriageAI uses Docker Compose to run four services:

```text
TriageAI
│
├── frontend    Port 5173   Vite frontend
├── backend     Port 8000   FastAPI
├── dashboard   Port 8001   FastAPI dashboard API
└── postgres    Port 5432   PostgreSQL 17
```

The services use `restart: unless-stopped`.

The frontend depends on the backend; backend and dashboard depend on PostgreSQL.

---

# 📱 Accessing TriageAI From Another Device

The frontend must be able to reach the backend from the device being used.

For network access, the configured backend address must be reachable from the device accessing the frontend.

For example:

```text
http://YOUR_SERVER_IP:8000
```

The FastAPI CORS configuration must also allow the frontend origin.

This is especially important when accessing the application from:

- A phone
- Another computer
- A different host on the local network

---

# 🧪 Current Safety Model

TriageAI separates different kinds of information:

```text
┌──────────────────────────────────────┐
│        PATIENT INFORMATION           │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│     DETERMINISTIC RULE ENGINE        │
│                                      │
│ • Reproducible                       │
│ • Inspectable                        │
│ • Rule-based                         │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│      DETERMINISTIC RESULT            │
└──────────────────┬───────────────────┘
                   │
                   │ Cannot be overridden
                   ▼
┌──────────────────────────────────────┐
│         AI COMPONENTS                │
│                                      │
│ • Independent assessment             │
│ • Explanation                        │
│ • Supplementary observations         │
└──────────────────────────────────────┘
```

Supplementary knowledge, when enabled by an implementation, remains separate from deterministic evidence.

---

# 🔒 Security and Reliability Considerations

TriageAI is a prototype.

Important areas for continued improvement include:

- Input-length restrictions
- Prompt-injection resistance
- Authentication and authorization
- API rate limiting
- Request logging and monitoring
- Error handling
- AI output validation
- More comprehensive automated testing
- More comprehensive deterministic rule coverage
- Validation of knowledge sources
- Access control for knowledge-base content

These areas should be addressed before considering deployment beyond a prototype environment.

---

# ⚠️ Current Limitations

TriageAI is under active prototype development.

## Prototype Rule Coverage

The deterministic rule system does not represent every possible clinical presentation.

Absence of a deterministic finding does not mean that a patient presentation is clinically insignificant.

A logic review (2026-09) documented these specific limitations:

- **Unmatched input defaults to group 5 (Not Urgent).** If no rule fires, the engine returns the least-urgent group. Example: `"face drooping, slurred speech"` with severity 9 resolves to group 5 because those words are not in the symptom dictionary.
- **Symptom recognition is dictionary-bound and thin**; several important presentations are not represented and `URGENT_SYMPTOMS` is an empty placeholder.
- **The red-flag layer is a placeholder**; the `red_flags` list is almost always empty because critical symptoms are categorised as `SYMPTOM`.
- **Age is collected but not used** in the deterministic logic.
- Diastolic BP is collected but not evaluated.
- `INCOMPLETE` triggers on any missing vital.
- Symptom severity is not range-checked.

## Privacy

The patient **name** is stored locally and returned to the frontend only. It is never sent to the AI.

`clinical_context` is free text and **is** sent to the AI, so names typed into clinical context would be transmitted.

## AI Output

AI output can differ from deterministic output.

The AI is therefore treated as an independent supplementary component rather than the authoritative deterministic decision-maker.

## Clinical Use

The system is not validated for real-world clinical deployment.

It must not be used as an autonomous triage system.

---

# 🧭 Development Philosophy

TriageAI prioritizes:

```text
Safety
   ↓
Deterministic Transparency
   ↓
Explainability
   ↓
Structured Data
   ↓
AI Assistance
```

The goal is not to allow an AI model to make an opaque clinical decision.

Instead, the project explores how AI can operate alongside a transparent deterministic system.

The deterministic engine should remain:

- Inspectable
- Testable
- Reproducible
- Expandable

AI and retrieved knowledge should remain clearly separated from deterministic evidence.

---

# 🗂️ Current Project Structure

The current build is organized around:

```text
TriageAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── explainability/
│   │   └── models/
│   ├── db/
│   └── tests/
├── dashboard/
├── frontend/
│   └── src/
├── demo/
├── dataset/
├── docker-compose.yml
└── README*.md
```

The exact provider-specific files and configuration are documented in the implementation READMEs.

---

# 🚀 Future Development

Potential future improvements include:

## Deterministic Engine

- Expanded symptom coverage
- Expanded vital-sign rules
- More structured red flags
- Additional contextual rules
- Improved rule coverage

## Knowledge Retrieval

- Expanded and validated knowledge sources
- Metadata filtering
- Retrieval evaluation
- Retrieval quality testing
- Clearer source attribution

## AI Components

- Additional AI providers
- Provider abstraction
- Improved structured output handling
- Prompt hardening
- Evaluation against representative test cases

## Testing

- Unit tests for individual rules
- Integration tests
- API tests
- Regression tests
- AI-output validation tests
- Retrieval tests

## Frontend

- Improved network configuration
- Environment-based API configuration
- Improved error messages
- Improved assessment history
- Better source visibility for retrieved supplementary information

---

# 🖼️ Demonstration

Example screenshots are stored in `demo/`, including:

- Assessment with moderately severe chest pain
- Assessment with chest pain and shortness of breath
- AI explanation
- Assessment with clinical context
- Multiple explicit symptoms and high heart rate
- Matching AI and deterministic assessments

---

# 🛡️ Core Principle

> **The deterministic engine produces the deterministic triage result. AI assistance and supplementary knowledge retrieval may provide additional context, but they do not override that result.**

---

# 📚 Implementation Documentation

TriageAI currently has two AI implementations:

- **[Featherless AI implementation](README-FEATHERLESS.md)** — Featherless API with `EpistemeAI/Reasoning-Medical0.1-27B`
- **[OpenAI implementation](README-OPENAI.md)** — OpenAI API with optional vector-store retrieval

The shared README documents the project itself; the implementation READMEs document only provider-specific configuration and behaviour.
