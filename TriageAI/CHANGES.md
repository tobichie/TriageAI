# 📋 TriageAI — Change & Architecture Update

**Last updated:** 2026-09-19

This document describes everything that was added or changed on top of the
original prototype. It is the single source of truth for the current state of
the deployed application. The main [README.md](README.md) has been updated in
the affected sections and points here for the details.

> ⚠️ TriageAI remains a **clinical decision-support prototype, not a medical
> device**. Thresholds and rules are non-validated prototype values. Every
> result requires human clinical review.

---

## 🗺️ What changed at a glance

| Area | Before | Now |
|------|--------|-----|
| Persistence | Only raw patient data stored | Full triage result + name + status + timestamps stored per encounter |
| Patient identity | none | `name` field (stored locally, **never sent to the AI**) |
| Dashboard API | `GET /patients` only | Full read / update / delete + status + statistics |
| Frontend | Single assessment screen | Three views: **Assess**, **Board**, **Records** |
| Nurse input | Number fields only | Pain **sliders**, symptom **quick-pick chips**, name field |
| Shift overview | none | **Triage board** sorted by urgency with live wait timers |
| Re-assessment | broken | Works — pre-fills the intake form from a stored patient |
| Theme | Light only | **Light / dark toggle** (night shift), persisted per device |
| Reboot safety | containers did not restart | `restart: unless-stopped` on all services |
| Services | frontend + backend | frontend + backend + **dashboard** + **PostgreSQL** |

---

## 🗄️ Data model & persistence

Previously the `/triage` endpoint stored only raw patient data (age, symptoms,
vitals, clinical context). The triage *result* was thrown away, so no overview
or board was possible.

Now every assessment persists the **complete encounter** in the `patients`
table ([backend/db/db.py](backend/db/db.py)):

``` text
patients
├── id
├── name                 ← NEW (identifier, never sent to the AI)
├── age
├── symptoms (JSON)
├── vital_signs (JSON)
├── clinical_context
├── triage_group         ← NEW (1–5, deterministic result)
├── treatment_priority   ← NEW
├── color                ← NEW (Manchester colour)
├── max_wait_minutes     ← NEW
├── reevaluation_minutes ← NEW
├── red_flags (JSON)     ← NEW
├── relevant_factors (JSON) ← NEW
├── requires_human_review   ← NEW
├── triage_result (JSON)    ← NEW (full result for the detail view)
├── ai_severity          ← NEW (independent AI priority)
├── ai_reason            ← NEW
├── ai_explanation       ← NEW
├── status               ← NEW (waiting | in_treatment | done)
├── created_at           ← NEW
└── updated_at           ← NEW
```

### Migration

`initialize_database()` runs on backend startup and is **idempotent**. It
creates the table if needed and adds any missing columns in place
(`ALTER TABLE ... ADD COLUMN IF NOT EXISTS`), so an existing database is
upgraded without losing data.

### New model field

`PatientData` ([backend/app/models/patient.py](backend/app/models/patient.py))
gained an optional `name` field. `TriageResponse` gained `patient_id` so the
frontend knows which stored row an assessment produced.

---

## 🌐 Backend API

### Main API (port 8000)

- `POST /triage` — unchanged contract, but now **stores the full result** and
  returns `patient_id`. New rows are created **only** here.
- `GET /health` — unchanged.

### Dashboard API (port 8001, behind nginx at `/dashboard-api/`)

Completely implemented ([dashboard/main.py](dashboard/main.py)). There is
intentionally **no create endpoint** — records are only created by `/triage`.

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/patients?include_done=true` | All patients, ordered by urgency then wait time |
| `GET`  | `/patients/{id}` | One patient |
| `PUT`  | `/patients/{id}` | Update name / age / symptoms / vitals / clinical context |
| `PATCH`| `/patients/{id}/status` | Set `waiting` / `in_treatment` / `done` |
| `DELETE`| `/patients/{id}` | Delete a record |
| `GET`  | `/stats` | Counts: total, waiting, in_treatment, done, by priority group |

Board ordering: `triage_group` ascending (1 = most urgent, NULLs last), then
`created_at` ascending (longest wait first).

---

## ⚛️ Frontend

Rebuilt around three views (top-bar navigation). Shared priority/formatting
logic lives in [frontend/src/triage.js](frontend/src/triage.js); dashboard
calls in [frontend/src/services/dashboardApi.js](frontend/src/services/dashboardApi.js).

### 1. Assess — nurse intake ([PatientForm.jsx](frontend/src/components/PatientForm.jsx))

- **Name** and **age** fields.
- **Pain / severity sliders** (0–10) with live labels — faster than typing.
- **Quick-pick symptom chips** (chest pain, shortness of breath, …) that add a
  symptom in one tap.
- Vital signs with clear units, free-text clinical context.
- Result panel ([AssessmentResult.jsx](frontend/src/components/AssessmentResult.jsx)):
  colour-coded priority banner, **"Why this priority"** (the explainability
  factors), red flags, independent **AI second opinion** and an
  agreement/disagreement indicator, collapsible detailed AI explanation.

### 2. Board — shift handover ([Board.jsx](frontend/src/components/Board.jsx))

- All patients as cards, **sorted by urgency**, Manchester colour stripe.
- **Live waiting time vs. target wait**, with an **"overdue"** highlight.
- One-tap status flow: `Start treatment` → `Mark done` → `Reopen`.
- Filters (Active / All / Done), auto-refresh, waiting count badge.

### 3. Records — admin ([Records.jsx](frontend/src/components/Records.jsx))

- Statistic tiles (total / waiting / in treatment / done).
- Patient list + detail view.
- **Edit** (name, age, clinical context), **Delete**, and **Re-assess**.

### Re-assessment

"Re-assess" (from Board or Records) loads the stored patient data back into the
intake form and switches to the Assess view (as designed: it "pulls up the
assessment site and preloads the data"). Submitting produces a fresh assessment
through `/triage`.

### 🌙 Dark mode

A light/dark toggle in the top bar ([App.jsx](frontend/src/App.jsx)) for night
shifts. The choice is stored per device (`localStorage`) and defaults to the
operating system preference. Priority colours stay vivid in both themes.
Implemented as an accessible `role="switch"`; dark tokens live in
[frontend/src/index.css](frontend/src/index.css).

---

## 🐳 Deployment / infrastructure

[docker-compose.yml](docker-compose.yml) now runs **four** services:

``` text
TriageAI
├── frontend    Port 5173   (Vite dev server; hot-reload volume on src)
├── backend     Port 8000   (FastAPI /triage, /health)
├── dashboard   Port 8001   (FastAPI dashboard API, internal only)
└── postgres    Port 5432   (PostgreSQL 17, named volume postgres_data)
```

- **`restart: unless-stopped`** on all services → the app comes back up
  automatically after a server reboot.
- Frontend bind-mounts `src`, `index.html`, `vite.config.js` for live reload.
- [frontend/vite.config.js](frontend/vite.config.js) has dev-server proxies for
  `/api` and `/dashboard-api` so the app also works when the Vite server is hit
  directly. In production these paths are proxied by nginx before Vite sees
  them, so the proxies do not affect production routing.
- nginx exposes three locations behind HTTPS + Basic Auth: `/` (frontend),
  `/api/` (backend), `/dashboard-api/` (dashboard).

### Environment variables ([.env](.env))

``` env
OPENAI_API_KEY=...
VECTOR_STORE_ID=...              # optional
ALLOWED_ORIGINS=https://triageai.munichtechexpo.paulmusch.de
POSTGRES_DB=triageai
POSTGRES_USER=triageai
POSTGRES_PASSWORD=...
DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```

`frontend/.env.production` uses `VITE_API_URL=/api` (relative, so it works
behind the domain).

---

## 🔒 Privacy — patient name is never sent to the AI

The `name` field is stored locally (PostgreSQL) and returned to the frontend
(same origin) only. It is **not** included in either OpenAI request:

- `build_ai_assessment_context()` and `build_explanation_context()`
  ([backend/app/explainability/service.py](backend/app/explainability/service.py))
  send only `age`, `symptoms`, `vital_signs` and `clinical_context`.
- OpenAI is the only external egress in the backend; `patient.name` is not
  referenced in any app code path.

This is locked in by a regression test
([backend/tests/test_privacy.py](backend/tests/test_privacy.py)) that fails if a
distinctive name ever appears in an AI payload.

> ⚠️ Residual risk: `clinical_context` is free text and **is** sent to the AI.
> If staff type a real name into that box, it would be transmitted. Consider a
> UI warning or server-side redaction.

---

## 🧠 Logic evaluation — known limitations

A review of the deterministic engine surfaced these points (ranked). They are
documented here so they are not forgotten; none have been changed yet.

1. **Unmatched input defaults to group 5 (Not Urgent).** When no rule fires,
   `get_most_urgent_group()` returns `NOT_URGENT`. Verified example: a symptom
   text `"face drooping, slurred speech"` with severity 9 (a classic stroke)
   resolves to **group 5**, because those words are not in the dictionary.
   "Unknown" is effectively treated as "not urgent". Recommended fix: a distinct
   "not classified — review manually" state instead of the least-urgent group.
2. **Symptom recognition is dictionary-bound and thin.** Covered: critical
   (`unconsciousness`, `cardiac_arrest`, `seizure`), very urgent
   (`severe_bleeding`, `severe_breathing_difficulty`), severity-based
   (`chest_pain`, `headache`, `abdominal_pain`, `shortness_of_breath`,
   `palpitations`); `URGENT_SYMPTOMS` is an empty placeholder. Missing: stroke,
   sepsis, anaphylaxis, meningitis signs, psychiatric/suicidality, etc.
3. **Red-flag layer is a placeholder.** `evaluate_red_flags()` only matches the
   literal `"example_critical_symptom"`; real critical symptoms are categorised
   as `SYMPTOM`, so the `red_flags` list is almost always empty.
4. **Age is collected but unused in the deterministic logic** (no
   paediatric/geriatric thresholds); it is only passed to the AI.
5. Minor: diastolic BP is collected but never evaluated; `INCOMPLETE` status
   triggers on any missing vital (mixes data-completeness with urgency); the
   more robust `normalize_symptom_name` is bypassed in the main path;
   `Symptom.severity` is not range-checked (0–10 slider allows 0).

---

## 🗂️ New & changed files

``` text
backend/
  app/models/patient.py            edited   + name field
  app/models/triage_response.py    edited   + patient_id
  app/api/routes/triage.py         edited   store full assessment
  db/db.py                         rewritten schema, migration, CRUD, stats
  tests/test_privacy.py            new      name-not-sent-to-AI guard
dashboard/
  main.py                          rewritten full CRUD + status + stats
frontend/
  src/triage.js                    new      shared priority helpers
  src/App.jsx                      rewritten 3 views + dark-mode toggle
  src/App.css                      rewritten design system
  src/index.css                    edited   tokens + dark theme + toggle
  src/services/dashboardApi.js     rewritten stats + status + CRUD
  src/components/PatientForm.jsx   rewritten sliders + chips + name
  src/components/AssessmentResult.jsx  new  combined result panel
  src/components/Board.jsx         new      triage board
  src/components/Records.jsx       new      admin/records
  src/components/{Dashboard,TriageResult,AIAssessment,
    AIExplanation,AssessmentComparison}.jsx  removed (replaced)
  vite.config.js                   edited   dev proxies
docker-compose.yml                 edited   +dashboard/postgres, restart, volume
CHANGES.md                         new      this document
```

---

## ▶️ Running & rebuilding

``` bash
cd ~/TriageAI

# Start / rebuild everything
docker compose up -d --build

# After changing backend or dashboard code
docker compose up -d --build backend dashboard

# Frontend src changes hot-reload automatically (bind mount);
# config changes need a restart:
docker compose restart frontend

# Run the privacy tests
docker compose exec backend python -m pytest tests/test_privacy.py -v
```

Live: **https://triageai.munichtechexpo.paulmusch.de** (behind Basic Auth).
