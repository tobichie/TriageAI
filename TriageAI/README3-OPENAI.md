# TriageAI — OpenAI Implementation

This README documents only the **OpenAI-specific implementation** of TriageAI.

For the problem, architecture, deterministic triage engine, frontend, database, security model, limitations and general development roadmap, see the [main README](README.md).

---

# 🤖 OpenAI Integration

This implementation uses the **OpenAI API** for the independent AI assessment and AI explanation components.

The AI layer is used for:

- Independent AI-assisted assessment
- AI reasoning
- AI-generated explanation of the deterministic result
- Identifying potentially relevant information not represented by the current deterministic rules
- Optional supplementary knowledge retrieval through vector search

The deterministic engine remains authoritative for the deterministic triage group.

> **The OpenAI components cannot override the deterministic triage result.**

---

# 🔍 Vector-Store Knowledge Retrieval

The OpenAI implementation supports a vector-store-backed supplementary knowledge base.

The current vector store contains:

```text
dataset/clinical-triage-sample-2026.txt
```

When configured, file search is made available to the AI components.

It applies to:

- The independent AI assessment
- The AI explanation component

The AI may use supplementary knowledge when relevant. It is not required to retrieve information for every request.

## Knowledge-Base Boundaries

The vector store is **not part of the deterministic rule engine**.

```text
                 DETERMINISTIC ENGINE
                         │
                         ▼
                 DETERMINISTIC RESULT
                         │
                         │ Cannot be modified
                         ▼
                  ┌───────────────┐
                  │ AI COMPONENTS │
                  └───────┬───────┘
                          │
                          ▼
                 SUPPLEMENTARY
                 KNOWLEDGE SEARCH
                          │
                          ▼
                    AI OBSERVATIONS
```

Retrieved information must not be represented as:

- A triggered deterministic rule
- A deterministic rule finding
- A deterministic engine decision
- A diagnosis

Supplementary information does not alter the deterministic triage group.

---

# ⚙️ Environment Configuration

Create a `.env` file in the project root.

OpenAI-specific configuration:

```env
OPENAI_API_KEY=your_api_key
VECTOR_STORE_ID=your_vector_store_id
```

The vector store is optional. If no vector store ID is configured, the service can continue without attaching the vector-store file-search tool.

The shared PostgreSQL and CORS configuration remains the same as described in the main README:

```env
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://<host_ip>:5173

POSTGRES_DB=triageai
POSTGRES_USER=triageai
POSTGRES_PASSWORD=change_me
DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```

Never commit API keys or other secrets to Git.

---

# 📦 Running the OpenAI Build

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

# 🗂️ OpenAI-Specific Changes

The OpenAI implementation differs from the Featherless build primarily in the AI service configuration and retrieval path.

The provider-specific configuration is represented by:

```text
OPENAI_API_KEY
VECTOR_STORE_ID
```

The AI service uses the OpenAI API and can expose the configured vector store to the AI components.

---

# 🧠 AI Assessment Flow

The OpenAI-specific AI path can be summarized as:

```text
Patient Data
      │
      ├─────────────────────────┐
      │                         │
      ▼                         ▼
Deterministic Engine       OpenAI AI Components
      │                         │
      ▼                         ├── Independent assessment
Deterministic Result           ├── AI explanation
      │                         └── Vector-store search
      │
      └──────────────┬──────────┘
                     │
                     ▼
                 Comparison
                     │
                     ▼
                Human Review
```

The vector-store result is supplementary information. It is not deterministic evidence and cannot change the deterministic triage group.

---

# 🗒️ Provider / Retrieval Note

The OpenAI implementation can use supplementary retrieval because the project exposes the knowledge base to the AI components through vector search.

The knowledge base is intentionally separated from the deterministic engine so that retrieved information cannot silently become a rule finding or deterministic decision.

---

# ⚠️ Provider-Specific Considerations

### API credentials

The OpenAI API key must be available to the backend through `OPENAI_API_KEY`.

### Vector-store configuration

`VECTOR_STORE_ID` is optional. Without it, the application can continue without attaching the vector-store file-search tool.

### Prompt hardening

The prompts in `backend/app/explainability/prompts.py` are not currently hardened against prompt injection or other prompt-engineering techniques.

### Clinical context size

The `Clinical Context` field currently accepts unrestricted text. Large inputs can increase token consumption and processing time.

A future implementation should introduce maximum input lengths and additional validation or truncation.

### Privacy

The patient name is deliberately excluded from the AI context. The OpenAI context builders send age, symptoms, vital signs and clinical context, but not the stored patient name.

Note that `clinical_context` is free text and is sent to the AI. A name entered into that field would therefore be transmitted.

---

# 🗒️ Implementation Note

Where supported by the configured AI provider, repeated structured requests may benefit from prompt caching, reducing repeated processing and potentially improving response latency.

---

# 🔄 OpenAI vs. Shared Architecture

The OpenAI-specific path is:

```text
Patient Data
      │
      ├─────────────────────────────┐
      │                             │
      ▼                             ▼
Deterministic Engine           OpenAI AI
      │                             │
      ▼                             ├── Independent assessment
Deterministic Result               ├── Explanation
      │                             └── Vector-store search
      │
      └───────────────┬─────────────┘
                      │
                      ▼
                  Comparison
                      │
                      ▼
                 Human Review
```

The OpenAI components remain supplementary and cannot replace the deterministic result.
