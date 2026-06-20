# Staffinc Client-Fit Matching & Briefing Tool MVP

This is a full-stack monorepo MVP built to optimize Staffinc's recruitment funnel and B2B client conversion rate.

## 📌 Problem Context
Staffinc candidates pass internal recruiter screenings but historically face a low client-stage interview acceptance rate of **~25% (1 out of 4)**. Rejection reasons are typically subjective (e.g., "didn't show up well," "communication vibe mismatch"). 

This B2B tool:
1. **Profiles Clients by Vibe**: Standardizes expectations into "Consulting/Corporate" or "Startup/Scrappy" archetypes with minimum competency thresholds (using the Behavioral Anchored Rating Scale, BARS).
2. **Standardizes Vetting**: Recruiters score candidates (1-5) against these specific client thresholds with live behavioral guidance to remove subjectivity.
3. **Automates Coaching Briefs**: Instantly generates a printable candidate prep guide mapping gaps, practice questions, and tailored coaching tips.
4. **Logs Outcomes**: Closes the feedback loop by recording final decisions and updating live conversion analytics.

---

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python 3.11) + SQLAlchemy + SQLite
- **Frontend**: React + Vite + Vanilla CSS
- **Data Generation**: Faker (for mock analytics & sandbox seeding)

---

## 📂 Project Structure
```text
staffinc/
├── backend/
│   ├── app/
│   │   ├── database.py       # SQLite connection and session local
│   │   ├── models.py         # SQLAlchemy ORM models (Client, Candidate, Score, Feedback)
│   │   ├── schemas.py        # Pydantic v2 validation schemas
│   │   ├── crud.py           # Database CRUD & mismatch checking
│   │   ├── seed.py           # Static BARS questions and default anchors
│   │   ├── seed_dummy.py     # Script to generate realistic mock data
│   │   ├── brief_generator.py# Gap analysis and strategy brief builder
│   │   └── main.py           # REST endpoints and static file mount
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Shared UI (Navbar, ScoreSlider, MismatchAlert)
│   │   ├── pages/            # Page templates (ClientSetup, CandidateScoring, BriefPreview, FeedbackForm)
│   │   ├── App.jsx           # Client router
│   │   └── main.jsx          # React entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🚀 Getting Started

### 1. Environment Setup

Make sure you have Anaconda or Miniconda installed, then create and activate the environment:
```bash
# Create the conda environment
conda create -n daftar-kerja python=3.11 -y

# Activate the environment
conda activate daftar-kerja
```

### 2. Backend Installation & Seeding

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt
pip install faker

# Seed the database with realistic dummy data
python -m app.seed_dummy
```

### 3. Frontend Installation

```bash
# Navigate to frontend (from project root)
cd ../frontend

# Install node dependencies
npm install
```

---

## 💻 Running the Application

### Option A: Unified Service (Production Build)
Build the React frontend assets, and let FastAPI serve both the API and the static site:
```bash
# 1. Build frontend (generates frontend/dist/)
cd frontend
npm run build

# 2. Run backend (serves API and front-end on http://127.0.0.1:8000)
cd ../backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Option B: Split Development Server
Run Vite's dev server with Hot Module Replacement alongside the FastAPI dev server:
```bash
# Run backend (dev reload)
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run frontend dev server (in a separate terminal)
cd frontend
npm run dev
```
*(Vite is configured to automatically proxy `/api` calls to the backend running at port 8000).*

---

## 🧪 E2E Verification Script
To test the full B2B matching and briefing cycle programmatically, run:
```bash
python -m urllib.request -e http://127.0.0.1:8000/api/stats
```
Or use our custom verification test script:
```bash
# Verify client creation, vetting, brief generation, and dashboard logging
python -m app.verify_e2e
```
