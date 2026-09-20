# TriageAI — Featherless AI Implementation

This README documents only the **Featherless-specific implementation** of TriageAI.

For the problem, architecture, deterministic triage engine, frontend, database, security model, limitations and general development roadmap, see the [main README](README.md).

---

# 🤖 Featherless AI Integration

This implementation uses **Featherless AI** as the AI provider.

The configured medical-reasoning model is:

```text
EpistemeAI/Reasoning-Medical0.1-27B
```

The model is used for:

- Independent AI-assisted assessment
- Medical reasoning
- AI-generated explanation of the deterministic result
- Identifying potentially relevant information not represented by the current deterministic rules

The deterministic engine remains authoritative for the deterministic triage group.

> **The Featherless model cannot override the deterministic triage result.**

## Problem

Unfortunately many of the larger models are very in demand which leads to low availability which causes the assessment to fail.
If it keeps failing, switch the model to one such as "Qwen/Qwen2.5-7B-Instruct" or any other that suits you and is available.


---

# 🧠 Medical Reasoning Model

The Featherless build changes the AI layer from a general-purpose language-model integration to a model specifically developed for medical reasoning.

The purpose is to provide a reasoning-oriented second perspective on the structured patient information and the deterministic triage result.

The AI layer is intended to:

- Analyze supplied symptoms, vital signs, age and clinical context
- Produce an independent severity assessment
- Provide reasoning for that assessment
- Explain the deterministic engine's result
- Highlight potentially relevant information that may not be represented by the current deterministic rules

Using a medical-reasoning model does **not** mean that TriageAI is clinically validated. The output remains AI-generated and requires qualified human review.

---

# 🔌 Featherless API

The application communicates directly with the Featherless Chat Completions API.

The provider and model are configured in the backend.

Authentication is supplied through:

```env
FEATHERLESS_KEY=your_api_key
```

The current model is:

```text
EpistemeAI/Reasoning-Medical0.1-27B
```

If the configured model is temporarily unavailable or at capacity, Featherless can return an error. This is an external model-service limitation and does not change the deterministic triage engine's rules.

---

# 🔍 Supplementary Knowledge Retrieval

The Featherless implementation **does not currently use a vector store for supplementary knowledge retrieval**.

The provided dataset was designed to supply additional clinical information to the AI. In this implementation, the medical-reasoning model is intended to provide the relevant reasoning directly.

Adding the provided dataset to the current medical-reasoning workflow would increase the amount of context that must be processed without being part of the current implementation.

For this reason, the Featherless build relies on the medical-reasoning model directly rather than supplementing it with the provided vector-store dataset.

This does **not** mean retrieval-augmented generation is inherently unsuitable for TriageAI. A curated, authoritative and sufficiently complementary knowledge base could provide value in a future implementation, particularly for information that is not adequately represented in the model or needs to be kept current.

---

# ⚙️ Environment Configuration

Create a `.env` file in the project root.

Featherless-specific configuration:

```env
FEATHERLESS_KEY=your_api_key
```

The shared PostgreSQL and CORS configuration remains the same as described in the main README:

```env
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://<host_ip>:5173

POSTGRES_DB=triageai
POSTGRES_USER=triageai
POSTGRES_PASSWORD=change_me
DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```

Never commit the Featherless API key to Git.

---

# 📦 Running the Featherless Build

From the repository root:

```bash
docker compose up -d --build
```

Check the services:

```bash
docker compose ps
```

Follow backend logs:

```bash
docker compose logs -f backend
```

The rest of the application startup, frontend access and Docker workflow are documented in the [main README](README.md).

---

# 🗂️ Featherless-Specific Changes

The September 2026 Featherless build introduced the provider-specific changes below:

```text
backend/
  app/explainability/service.py
      └── Featherless AI + medical-reasoning model

```

The main provider-specific change is the AI service integration. The rest of the project remains shared with the OpenAI implementation.

---

# ⚠️ Provider-Specific Considerations

### External model availability

The application depends on the configured Featherless model being available through the provider.

A provider-side availability or capacity error does not alter the deterministic triage engine.

### Prompt hardening

The prompts in `backend/app/explainability/prompts.py` are not currently hardened against prompt injection or other prompt-engineering techniques.

### Clinical context size

The `Clinical Context` field currently accepts unrestricted text. Large inputs can increase token consumption and processing time.

A future implementation should introduce maximum input lengths and additional validation or truncation.

---

# 🗒️ Implementation Note

Where supported by the configured AI provider, repeated structured requests may benefit from prompt caching, reducing repeated processing and potentially improving response latency.

---

# 🔄 Featherless vs. Shared Architecture

The provider-specific path is:

```text
Patient Data
      │
      ├──────────────────────┐
      │                      │
      ▼                      ▼
Deterministic Engine    Featherless AI
      │                      │
      ▼                      ▼
Deterministic Result    Independent AI Assessment
      │                      │
      └──────────┬───────────┘
                 │
                 ▼
             Comparison
                 │
                 ▼
            Human Review
```

The Featherless AI result remains supplementary and cannot replace the deterministic result.
