# Entrepreneur Mitra Frontend (SIH26092)

**Ministry of Social Justice and Empowerment (MoSJE)**  
**Theme:** Smart Automation & Citizen Inclusion

This directory contains the modular Next.js 14 / TypeScript frontend architecture for **Entrepreneur Mitra**.

---

## 🌟 Dual Delivery Model

To ensure seamless operation on both developer workstations without Node.js and modern cloud environments (Vercel / AWS / Docker), this project offers two execution modes:

### Mode A: Instant Live Web App (No Node.js Required)
The production-quality interactive frontend is mounted directly inside the FastAPI backend under `app/static/`:
* Runs out-of-the-box on Python 3.12:
  ```bash
  uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
  ```
* Open in browser: `http://127.0.0.1:8000/`
* Features:
  - Full voice recognition & synthesis (Web Speech API) in Hindi and English
  - Live Audio Waveform Canvas
  - 1-Click SIH Persona Demo (Ramesh Kumar - OBC Carpenter)
  - 6-Factor deterministic matching engine results
  - "Why Am I Eligible? (Rule Trace)" modal with zero-hallucination verification
  - Dynamic EMI Calculator with reactive sliders and DTI gauge
  - "What-If?" hypothetical scenario simulator
  - Leaflet / OpenStreetMap Geo-Spatial Partner Locator
  - Document Vault & Simulated OCR Checklist
  - 5-Step Application Copilot

---

### Mode B: Next.js 14 TypeScript Cloud Web App
For cloud deployments (e.g. Vercel, Docker multi-stage builds):
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000`. Set `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api/v1` in `.env.local`.

---

## 🏛️ Color Palette & Design Tokens
* **Ashoka Navy:** `#0F2C59` (Primary branding)
* **Sunrise Saffron:** `#E85D04` (Call-to-Action)
* **Emerald Growth:** `#0B6E4F` (Passed criteria & High Match)
* **Parchment White:** `#F8F9FA` (Background)
* **High Contrast Mode:** WCAG 2.2 AAA compliant
