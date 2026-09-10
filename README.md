# Entrepreneur Mitra (उद्यमी मित्र)
## SIH26092: AI-Driven Scheme Matching for Marginalized Entrepreneurs
**Ministry:** Ministry of Social Justice and Empowerment (MoSJE)  
**Department:** Department of Social Justice and Empowerment  
**Theme:** Smart Automation  
**Platform:** Next-Gen Full-Stack Web & PWA Platform (FastAPI + SQLAlchemy 2.0 + Supabase PostgreSQL + Accessible GovTech UI)

---

## 1. Executive Summary & Golden Architecture

**Entrepreneur Mitra** is an authentic, voice-first, multilingual government scheme access and financial onboarding platform engineered for marginalized, rural, and first-time entrepreneurs (SC, OBC, Safai Karamcharis, and Divyangjan).

### The Golden Pipeline of Entrepreneur Mitra
```text
User Information (Voice in Hindi/English/Hinglish or Form Input)
      ↓
Structured Entrepreneur Profile & Attribute Trust Hierarchy
      ↓
Deterministic Government Scheme Rules (Zero LLM Hallucination)
      ↓
Statutory Eligibility Facts (Traceable PASS / FAIL / UNKNOWN Criteria)
      ↓
6-Part Transparent Match Ranking (100% Deterministic Weighted Model)
      ↓
Explainable AI (Translates Pre-Evaluated Traces into Plain Hindi/Hinglish/English)
      ↓
Financial Affordability Engine (Concessional Reducing-Balance EMI & DTI)
      ↓
Geo-Spatial Partner Router (Verified SCAs, District Lead Banks, and RRBs)
      ↓
Application Copilot & DigiLocker Requester Integration
```

> [!IMPORTANT]
> **Strict Zero-Hallucination Rule**: The LLM is **never** permitted to decide or fabricate government scheme eligibility. Eligibility is evaluated exclusively by deterministic rules grounded in statutory guidelines published by MoSJE, NBCFDC, NSFDC, NSKFDC, and DEPwD. The AI layer serves solely to eliminate language, literacy, and navigation barriers.

---

## 2. Core Capabilities & Architectural Integrations

1. **Deterministic 6-Factor Matching Engine**:
   - Computes transparent weighted score:
     - **35%**: Eligibility Completeness
     - **25%**: Purpose & Enterprise Fit
     - **15%**: Financial Loan Fit
     - **10%**: Geography & Scope Fit
     - **10%**: Document Readiness
     - **5%**: User Category Preference
   - **Ineligibility Cap**: If a mandatory condition fails, the scheme score is hard-capped (<= 30%) and clearly marked as `NOT_ELIGIBLE`.

2. **100% Zero-Leak Multilingual Internationalization (EN, HI, Hinglish)**:
   - Complete localized dictionaries (`en.json`, `hi.json`, `hinglish.json`).
   - When English is selected: **0% Devanagari text** anywhere across navbar, onboarding, hero, metrics, cards, sliders, partner locator, DigiLocker dialogs, toasts, and API explanation traces.
   - Persistent language choice saved in `localStorage`.

3. **DigiLocker Requester Integration & Trust Hierarchy**:
   - Provider abstraction: `SandboxDigiLockerProvider` (authoritative demo mode for hackathon evaluation) and `ProductionDigiLockerProvider` (MeitY OAuth 2.0 requester).
   - Strict honesty: Explicitly labelled `[Demo / Sandbox Mode]` when operating without live MeitY production credentials.
   - Enforces 7-level Document Trust Hierarchy:
     1. DigiLocker Issuer-Backed (Highest Trust)
     2. Departmental Portal API
     3. Validated Upload (SHA-256 Checksum)
     4. Administrative Manual Review
     5. OCR Extraction (Candidate data requiring human confirmation)
     6. Self-Declared Information (Lowest Trust)
     7. Expired / Rejected

4. **Expanded Authentic Scheme Catalog (11 Schemes)**:
   - Verified statutory citations, published interest rates (4% to 8.5%), moratorium terms (3 to 18 months), loan ceilings, and official portal links:
     1. `NBCFDC-GTL-001`: NBCFDC General Term Loan (GTL)
     2. `NBCFDC-SWARNIMA-002`: New Swarnima Scheme for Women (Zero margin money)
     3. `NBCFDC-MAHILA-003`: Mahila Samriddhi Yojana (Micro-finance for Women SHGs)
     4. `NSFDC-TL-004`: NSFDC Regular Term Loan Scheme (Scheduled Castes)
     5. `NSFDC-LVY-005`: NSFDC Laghu Vyavasay Yojana (SC Micro-credit)
     6. `NSKFDC-GTL-006`: NSKFDC General Term Loan (Safai Karamcharis / Manual Scavengers)
     7. `NSKFDC-MAHILA-007`: NSKFDC Mahila Adhikarita Yojana
     8. `DEPWD-SWAVALAMBAN-008`: Divyangjan Swavalamban Scheme (Differently-abled entrepreneurs)
     9. `STANDUP-INDIA-001`: Stand-Up India Scheme (SC/ST & Women greenfield enterprises)
     10. `PM-DAKSH-001`: PM-DAKSH Yojana (Skill + Enterprise linkage)
     11. `PMEGP-KVIC-011`: Prime Minister's Employment Generation Programme (35% rural subsidy)

5. **Financial Affordability & EMI Calculator**:
   - Concessional reducing-balance formula with moratorium holiday grace calculation, promoter margin contribution (5%), and Debt-to-Income (DTI) affordability gauge.

6. **Geo-Spatial Partner Locator**:
   - Leaflet interactive map and directory locating State Channelising Agencies (SCAs) and designated bank branches across Uttar Pradesh, Delhi, Maharashtra, Bihar, Rajasthan, and Madhya Pradesh.

7. **Database Migration to Supabase PostgreSQL**:
   - Direct SQLAlchemy 2.0 support for Supabase PostgreSQL (`postgresql://...`).
   - One-command safe migration script (`scripts/migrate_to_supabase.py`) and PostgreSQL schema DDL (`scripts/supabase_schema.sql`).
   - Zero Prisma dependency. Seamless fallback to local SQLite (`entrepreneur_mitra.db`).

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend API** | **FastAPI 0.115+** | High-performance async REST API with interactive OpenAPI docs |
| **ORM & Database** | **SQLAlchemy 2.0 + Psycopg2** | Dual-mode: SQLite (local demo) & Supabase PostgreSQL (production) |
| **Data Validation** | **Pydantic v2** | Typed schemas, request envelopes, and response models |
| **Frontend UI** | **Vanilla JS + CSS Design System** | High-performance, accessible, responsive PWA (360px to 1440px) |
| **Localization (i18n)** | **Centralized JSON Locales** | English, Hindi (हिन्दी), and Hinglish with zero text leak |
| **Maps & GIS** | **Leaflet.js + OpenStreetMap** | Geospatial partner locating and distance calculation |
| **Speech & Audio** | **Web Speech API + Waveform Canvas** | Real-time speech-to-text, voice synthesis, and audio visualizer |
| **Testing** | **Pytest (33 Automated Tests)** | Unit, API, boundary, language-leak, and migration verification |

---

## 4. Quick Start & Execution Guide

### Prerequisites
- Python 3.10+ (Recommended Python 3.12)
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/Dikshit47/Entrepreneur-Mitra.git
cd Entrepreneur-Mitra
python -m pip install -r requirements.txt
python -m pip install psycopg2-binary
```

### 2. Configure Environment (.env)
Copy `.env.example` to `.env`:
```env
APP_NAME="Entrepreneur Mitra Backend"
APP_ENV="development"
DEBUG=True
API_V1_PREFIX="/api/v1"
SECRET_KEY="sih26092-dev-secret-key-for-local-evaluation"

# Database: SQLite (default) or Supabase PostgreSQL
DATABASE_URL="sqlite:///./entrepreneur_mitra.db"
# SUPABASE_DATABASE_URL="postgresql://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres"

# DigiLocker Requester Integration
DIGILOCKER_ENVIRONMENT="sandbox" # 'sandbox' or 'production'
DIGILOCKER_CLIENT_ID=""
DIGILOCKER_CLIENT_SECRET=""
DIGILOCKER_REDIRECT_URI="http://127.0.0.1:8000/api/v1/documents/digilocker/callback"
```

### 3. Seed Database
```bash
python -m app.seed.seed_data
```

### 4. Run Server
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open your browser at:
- **Interactive Application:** `http://127.0.0.1:8000/`
- **API Documentation (Swagger):** `http://127.0.0.1:8000/docs`

### 5. Windows 1-Click Desktop Launcher
For non-technical evaluators, simply double-click:
`C:\Users\diksh\Entrepreneur-Mitra\run_mitra.bat` or the Desktop shortcut `Entrepreneur Mitra.bat`.

---

## 5. Supabase PostgreSQL Migration

To migrate existing records from SQLite to Supabase PostgreSQL:
```bash
# 1. Test in dry-run mode
python scripts/migrate_to_supabase.py --dry-run

# 2. Run migration to your Supabase PostgreSQL instance
python scripts/migrate_to_supabase.py --url "postgresql://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres"
```
Or paste the generated DDL directly in the Supabase SQL Web Editor:
`scripts/supabase_schema.sql`

---

## 6. Running Automated Tests

Run the complete test suite (33 automated tests):
```bash
python -m pytest tests/ -v
```
Verified test coverage includes:
- Authentication & JWT security (`test_auth.py`)
- Financial EMI & Moratorium calculation (`test_calculator.py`)
- DigiLocker Sandbox & Trust Hierarchy (`test_digilocker.py`, `test_digilocker_providers.py`)
- 100% Zero Language Leak validation (`test_language_leak.py`)
- Deterministic 6-part weighted scoring integrity (`test_matching_integrity.py`)
- Authentic Scheme Catalog verification (`test_schemes_catalog.py`)
- Supabase PostgreSQL dialect compatibility (`test_supabase_compat.py`)
- What-If Simulator isolation (`test_what_if.py`)

---

## 7. License & Compliance
Built for Smart India Hackathon 2026 (SIH26092) under the guidelines of the Ministry of Social Justice and Empowerment (MoSJE), Government of India. All scheme parameters are referenced directly from published statutory guidelines.
