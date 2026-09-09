# Entrepreneur Mitra — Backend MVP
## SIH26092: AI-Driven Scheme Matching for Marginalized Entrepreneurs
**Organization:** Ministry of Social Justice and Empowerment (MoSJE)  
**Theme:** Smart Automation

---

## 1. Executive Summary & Golden Architecture

**Entrepreneur Mitra** is an AI-powered, voice-first government scheme access platform designed for marginalized, rural, and first-time entrepreneurs. It bridges the gap between real-life applicant situations and complex government assistance.

### The Golden Rule of Entrepreneur Mitra
```text
User Information
      ↓
Structured Profile
      ↓
Deterministic Government Rules (Zero LLM Hallucination)
      ↓
Eligibility Facts (Traceable Rule Decision)
      ↓
6-Part Transparent Match Ranking
      ↓
Explainable AI (Translates Pre-Evaluated Traces into Plain Hindi/Hinglish/English)
      ↓
Financial Affordability & Geo-Spatial Partner Router
```

> [!IMPORTANT]
> **Strict AI Boundary**: The LLM is **never** permitted to determine eligibility independently. Eligibility is computed exclusively by a deterministic rule engine evaluating official published scheme criteria (`PASS`, `FAIL`, `UNKNOWN`). The AI layer serves solely to eliminate language, literacy, and navigation barriers.

---

## 2. Key Capabilities & Problem-Statement Alignments

1. **Smart Scheme Recommender & Ranking Engine**:
   - Transparent 6-part weighted formula: 35% eligibility completeness + 25% purpose fit + 15% financial fit + 10% geography + 10% document readiness + 5% user preference.
2. **Deterministic Traceable Eligibility Engine**:
   - Traceable rules with explicit criteria outcomes: `ELIGIBLE`, `NOT_ELIGIBLE`, `PARTIALLY_ELIGIBLE`, `NEEDS_VERIFICATION`, `INSUFFICIENT_INFORMATION`.
3. **What-If Eligibility Simulator**:
   - Allows entrepreneurs to test hypothetical scenarios (*"What if my annual income is ₹2,00,000?"*) without altering their real profile.
4. **Financial Affordability Calculator**:
   - Dynamic monthly EMI calculation, tenure adjustment, moratorium holiday interest, and mandatory promoter contribution (margin money).
5. **Geo-Spatial Partner Locator & Router**:
   - Haversine great-circle distance calculation locating nearby State Channelising Agencies (SCAs), Rural Banks, and Nationalised Banks with category and fund-utilisation status.
6. **Conversational AI Interview**:
   - Natural language and voice-based dialogue that extracts structured entrepreneur profile fields iteratively.
7. **Document Intelligence & Human Confirmation**:
   - Secure file upload with checksum calculation, size limits, and OCR extraction returning candidate values with `requires_confirmation: true`.
8. **Application Copilot**:
   - Step-by-step guidance connecting discovery to verified official government application portals.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **API Framework** | **FastAPI** | High-performance async REST API with interactive OpenAPI/Swagger docs |
| **Data Validation** | **Pydantic v2** | Strict schema validation, typed models, and envelope serialization |
| **ORM & Database** | **SQLAlchemy 2.0** | Dual-mode: SQLite (local demo / testing) & PostgreSQL + PostGIS (production) |
| **Authentication** | **PyJWT + PBKDF2** | Stateless Bearer token authentication with role-based access control |
| **Voice & Speech** | **VoiceProvider Abstraction** | Modular interface compatible with Web Speech API, Whisper, and IndicConformer |
| **Testing** | **Pytest + HTTPX** | Automated integration and boundary unit test suite |
| **Containerization** | **Docker & Docker Compose** | Multi-container production deployment with PostGIS 16 |

---

## 4. Project Directory Structure

```text
entrepreneur-mitra-backend/
├── app/
│   ├── main.py                     # FastAPI app, CORS, Request ID middleware, Exception handlers
│   ├── config.py                   # Pydantic BaseSettings, configuration flags (MOCK_AI, MOCK_VOICE)
│   ├── database.py                 # SQLAlchemy engine, session maker, base model
│   ├── api/
│   │   ├── deps.py                 # Database session and JWT authentication dependencies
│   │   └── v1/
│   │       ├── router.py           # Unified v1 router
│   │       ├── auth.py             # /auth/register, /auth/login, /auth/logout, /auth/me
│   │       ├── profiles.py         # /profiles, /profiles/{id}, /profile
│   │       ├── interviews.py       # /interviews/{id}/turn, /interview/start, /interview/confirm
│   │       ├── schemes.py          # /schemes, /schemes/{id}, /schemes/{id}/application-steps
│   │       ├── eligibility.py      # /eligibility/check, /eligibility/simulate
│   │       ├── matching.py         # /matches, /matches/{id}/explanation, /matching/results
│   │       ├── calculator.py       # /calculator/emi, /calculator/affordability
│   │       ├── partners.py         # /partners/nearby (Haversine geo-distance & fund status)
│   │       ├── documents.py        # /documents, /documents/{id}/extract
│   │       ├── applications.py     # /applications, /applications/{id}
│   │       ├── saved_schemes.py    # /saved-schemes, /schemes/{id}/save
│   │       ├── alerts.py           # /alerts
│   │       ├── voice.py            # /voice/transcribe, /voice/speak
│   │       └── ai.py               # /ai/explain
│   ├── models/                     # SQLAlchemy ORM models (User, Profile, Scheme, Partner, etc.)
│   ├── schemas/                    # Pydantic v2 schemas and standard ApiResponse envelope
│   ├── services/                   # Business logic layers (Auth, Profile, Eligibility, Matching, etc.)
│   ├── rules/                      # Deterministic rule evaluator and operator comparisons
│   ├── utils/                      # Security helpers, password hashing, and custom exceptions
│   └── seed/
│       └── seed_data.py            # Authentic MoSJE / NBCFDC / Stand-Up India seed data
├── docs/
│   └── api/
│       └── openapi.json            # Exported OpenAPI specification for Frontend teams
├── tests/                          # 14 automated unit & integration test suites
├── .env.example                    # Environment template
├── requirements.txt                # Production dependencies
├── Dockerfile                      # Container build
├── docker-compose.yml              # PostgreSQL + PostGIS container definition
└── README.md
```

---

## 5. Quickstart & Local Setup

### 5.1 Clone & Setup Environment
```powershell
# Navigate to project directory
cd C:\Users\diksh\.gemini\antigravity\scratch\entrepreneur-mitra-backend

# Install dependencies
pip install -r requirements.txt
```

### 5.2 Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Default settings are pre-configured for instant local zero-setup execution using SQLite.

### 5.3 Seed the Database
Populate authentic MoSJE / NBCFDC schemes, rules, benefits, and channel partners:
```powershell
python -m app.seed.seed_data
```

### 5.4 Run the Backend Server
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc Documentation: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON Contract: `http://127.0.0.1:8000/docs/api/openapi.json`

---

## 6. Running Automated Tests

Run the full pytest suite:
```powershell
pytest -v
```

All 14 unit and integration tests verify:
- Authentication & JWT token validation
- Profile attribute storage and completeness calculation
- Deterministic eligibility checks (PASS, FAIL, boundary conditions, missing fields)
- 6-part transparent matching score and ranking priority
- Loan affordability & EMI calculation with moratorium considerations
- What-If Simulator isolation (verifying no profile mutations occur)
- Geo-spatial partner distance ranking around Bijnor, UP
- Secure file upload and OCR candidate extraction
- Conversational AI interview turn extraction

---

## 7. SIH Demo Persona Walkthrough (Ramesh Kumar, Age 32)

| Time | Demo Step | Endpoint | Action & Wow Moment |
|---|---|---|---|
| **0:00** | **Start** | `POST /api/v1/interview/start` | App greets in Hindi: *"Namaste! Main Entrepreneur Mitra hoon..."* |
| **0:15** | **Voice Input** | `POST /api/v1/interviews/{id}/turn` | User speaks: *"Mujhe silai ka naya business shuru karna hai aur 3 lakh chahiye."* System extracts `tailoring`, `new`, `₹3,00,000`. |
| **0:35** | **Follow-up** | `POST /api/v1/interviews/{id}/turn` | AI prompts: *"Aap kis zila (District) mein business shuru karna chahte hain?"* |
| **0:50** | **Profile Review** | `GET /api/v1/profiles/{id}` | Displays structured profile: Business: Tailoring, Cost: ₹3L, Income: ₹2.5L, Category: SC, Location: Bijnor, UP. |
| **1:10** | **Scheme Matching** | `POST /api/v1/matches` | Returns top ranked match: **NBCFDC General Term Loan Scheme (GTL)** with **ELIGIBLE** status and match score 91. |
| **1:30** | **Traceable Explanation** | `GET /api/v1/matches/{id}/explanation` | Displays visual rule trace: Income rule (<= ₹3L) ✓, Category (SC) ✓, Purpose (Tailoring) ✓. |
| **2:00** | **Financial Calculator** | `POST /api/v1/calculator/emi` | Principal: ₹3,00,000, 5% interest, 5 years, 6 months moratorium. Projects EMI of ₹6,211/mo and 5% promoter margin (₹15,000). |
| **2:30** | **Document Intelligence**| `POST /api/v1/documents` | Uploads Income Certificate; OCR extracts ₹2,50,000 and prompts user confirmation. |
| **3:00** | **What-If Simulator** | `POST /api/v1/eligibility/simulate` | Simulates income change and demonstrates hypothetical result without corrupting real data. |
| **3:30** | **Nearby Partner Router**| `GET /api/v1/partners/nearby` | Displays nearest channel partner: State Bank of India MSME Desk, Bijnor (distance < 5 km) with fund status: AVAILABLE. |
| **4:00** | **Application Copilot** | `GET /api/v1/schemes/{id}/application-steps`| Step-by-step checklist guiding the entrepreneur to official government portal (`nbcfdc.gov.in`). |

---

## 8. Frontend Integration Guidance

Frontend developers should use:
- **Base URL**: `http://localhost:8000/api/v1`
- **Standard Envelope**:
  ```json
  {
    "success": true,
    "data": { ... },
    "error": null,
    "meta": { "request_id": "req_..." }
  }
  ```
- **Static Contract File**: [docs/api/openapi.json](file:///C:/Users/diksh/.gemini/antigravity/scratch/entrepreneur-mitra-backend/docs/api/openapi.json)
