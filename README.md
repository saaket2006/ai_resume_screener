# ResumeAI - AI Hiring Intelligence Platform

An end-to-end, high-performance AI Hiring Intelligence Platform designed to analyze, score, rank, and explain candidate resumes against target job descriptions. Built on top of FastAPI and a multi-agent semantic orchestration pipeline, ResumeAI transforms traditional keyword-parsing into a robust, context-aware visual screening experience.

---

### 🌐 Live Website: [https://ai-resume-screener-69d23.web.app/](https://ai-resume-screener-69d23.web.app/)

---

## ✨ Core Features & Platform Layers

### 🎨 Modern SaaS Visual Experience
* **Global Dark Emerald Theme**: Designed with custom slate background grids, glowing gradients, rounded layouts, glassmorphism card panels, and emerald (`#10b981`) accents governed by CSS custom variables.
* **GSAP-Driven Animation Engine**: Features smooth letter-by-letter fade-and-blur headline reveals, scroll-driven storytelling timelines, and stacking sticky card decks outlining core features.
* **HTML Dashboard Mockup**: An interactive hero visual mockup built from HTML elements featuring mouse coordinate tilts, progress metrics, and floating badge panels.
* **Simulated Run Playground**: A simulated environment letting visitors test the PDF extraction, token classification, and semantic matching engines.
* **AI Processing Pipeline Overlay**: Redesigned loading screen featuring a full-screen Speed-Line layout. Displays the live status of the active pipeline stage:
  `Resume Uploaded` → `Resume Parsing` → `Skill Extraction` → `Semantic Matching` → `Multi-Agent Analysis` → `Candidate Ranking` → `Explainability`
  with states: Completed (✓), Active (⬤), and Pending (○).

### ⚙️ Event-Driven Orchestration Pipeline
ResumeAI carries request context via an `AnalysisContext` object carrying `request_id`, performance timings, and profile metadata across 6 decoupled stages:
1. **Resume Text Extraction**: Decodes layouts from PDF and DOCX files.
2. **Skill Extraction**: spaCy Named Entity Recognition and custom regex-based heuristic tokens.
3. **Semantic Matching**: Resolves aliases, acronyms (e.g. `K8s` ↔ `Kubernetes`), technology hierarchies, and industry namespaces (`future.medical`, `future.finance`).
4. **Adaptive Scoring**: Computes component scores based on the selected recruiter profile coefficients.
5. **Explanation Building (XAI)**: Generates detailed, presentation-independent reports containing reasons points were awarded or deducted.
6. **Persistence Stage**: Commits records transactionally to the relational database.

### 🧠 Adaptive Scoring Profiles
Recruiters can customize matching coefficients dynamically. Component weights are resolved per profile:
* **Backend Developer**: Skills 45% | Experience 30% | Education 10% | Projects 15%
* **DevOps Engineer**: Skills 45% | Experience 30% | Education 5% | Projects 20%
* **AI Engineer**: Skills 50% | Experience 20% | Education 20% | Projects 10%
* **Fresh Graduate**: Skills 30% | Experience 10% | Education 30% | Projects 30%
* **General Software Engineer**: Skills 50% | Experience 25% | Education 15% | Projects 10%

### 🔄 Resume Versioning & Comparison Reliability
Candidates can upload multiple versions of their resume to track score improvements:
* **Natural Score Gains**: Progress timeline highlights improvements using natural terms (e.g. `Resume Improved: +18 points`).
* **Comparison Reliability Check**: Automatically compares versions to check consistency of the context. Renders a clear checklist detailing:
  - `✓ Same Job Description` (or `✗ Different Job Description`)
  - `✓ Same Profile` (or `✗ Different Profile`)
  - `✓ Same Engine Version` (or `✗ Different Engine Version`)
  resulting in a `HIGH ⭐` or `LOW ⚠` reliability badge.

### 📋 Recommendation Lifecycle
Provides candidates with prioritized steps to improve their resumes. Tracks transitions using a lifecycle status state machine:
* `ACTIVE`: Default suggestions awaiting user action.
* `COMPLETED`: Triggered once a candidate implements the recommendation.
* `DISMISSED`: Dismissed by the candidate.
* `EXPIRED`: Suppressed by subsequent scans.

### 🛡️ System Resilience & Offline Support (New)
* **Localized Assets**: Removed third-party CDN latency and layout breaks. Core libraries (`gsap.min.js`, `ScrollTrigger.min.js`, `lucide.min.js`) are served locally.
* **Offline & Maintenance Banner**: Global fetch error interception displays a non-intrusive warning alert if the backend server is offline (e.g., during cold-starts on Render) or down for maintenance, auto-dismissing when connection is restored.
* **Compiled Tailwind Stylesheet**: Employs locally compiled Tailwind v4 CSS, scanning layout and script files to export a production-minified styles file, removing runtime play CDN performance hits.

---

## 📁 Project Structure

```text
├── backend/
│   ├── main.py                 # FastAPI Web Application Entrypoint
│   ├── config.py               # Settings and Environment Variables
│   ├── models/                 # SQLAlchemy Models (Scans, Profiles, Recommendations)
│   ├── routers/                # FastAPI Routers (candidate.py, recruiter.py, auth.py)
│   └── services/               # Core Pipeline Services
│       ├── policy/             # Profiles Weights Policy & Recruiter Analytics
│       ├── recommendations/    # Resume Improvement Engine (Lifecycles & Prioritization)
│       ├── semantic/           # Skill Namespace Mappers & Synonym Resolver
│       ├── xai/                # Explainable Scoring Engine
│       └── pipeline.py         # 6-Stage Decoupled Orchestration Engine
├── frontend/
│   ├── index.html              # Core HTML Structure, Landing page & Modals
│   ├── assets/
│   │   ├── css/
│   │   │   ├── design-tokens.css # Global CSS Variables & Theme Constants
│   │   │   ├── base.css          # Base Workspace Cards, Grids & Fonts
│   │   │   ├── landing.css       # Custom SaaS Layouts, Speed-Lines, & Aurora Animations
│   │   │   └── tailwind.min.css  # Local Compiled & Minified Tailwind Stylesheet
│   │   └── js/
│   │       ├── api.js            # Fetch request handler, Token injection & Offline Banner
│   │       ├── landing.js        # UI Event Bindings, Simulated Playground & FAQ Toggles
│   │       ├── animations.js     # GreenSock (GSAP) Entrance, Story & Stacking Timelines
│   │       ├── loadingOverlay.js # Full-Screen Pipeline Processing Modal
│   │       ├── app.js            # Workspace Client State & Auth Router Hooks
│   │       └── vendor/           # Localised Offline Script Libraries (GSAP, Lucide)
├── tailwind.config.js          # Tailwind CSS Scanning configurations
├── requirements.txt            # Python Dependencies
├── package.json                # Frontend Package Scripts and Build utilities
└── alembic/                    # Schema Migration histories
```

---

## 🚀 Setup & Local Development Instructions

Follow these steps to run the complete FastAPI backend and static frontend locally:

### 1. Prerequisites
- Python 3.9+
- Node.js (For local asset compiling)

### 2. Backend Environment Setup
Navigate to the project root and create a virtual environment:
```bash
# Clone the repository
git clone https://github.com/saaket2006/ai_resume_screener.git
cd ai_resume_screener

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
*(Note: Upon the first analysis invocation, the system will automatically download the necessary spaCy `en_core_web_sm` model).*

### 3. Database Configurations
The application connects to a cloud PostgreSQL (Supabase) database.

#### Supabase PostgreSQL Setup
To connect to your cloud PostgreSQL database (e.g. Supabase connection pooler), add `DATABASE_URL` to your `.env` file:
```env
DATABASE_URL="postgresql://postgres.<username>:<password>@<host>:5432/postgres"
JWT_SECRET="your-strong-randomly-generated-key"
```

#### Run Database Migrations
Run Alembic schema migrations on your database:
```bash
alembic upgrade head
```

#### Migrate SQLite to PostgreSQL
If you want to migrate legacy records from an old local SQLite database file to Supabase:
```bash
python scratch/migrate_to_supabase.py
```

### 4. Compile Tailwind CSS (Optional)
If you modify frontend utility classes, compile the minified stylesheet:
```bash
# Install CLI tool
npm install

# Run compilation
npm run build:css
```

### 5. Run the Servers

#### Run Backend Server
```bash
python -m uvicorn backend.main:app --reload
```
The API server will launch at `http://127.0.0.1:8000`. Verify API docs at `http://127.0.0.1:8000/docs`.

#### Run Frontend Server
Serve the `frontend/` directory using any local web server.

**Option A (Python):**
```bash
python -m http.server -d frontend 3000
```
Open `http://localhost:3000` in your browser.

**Option B (Node.js):**
```bash
npx serve frontend
```

