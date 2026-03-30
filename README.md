# AI Resume Screening & Candidate Ranking System

An end-to-end AI-powered system designed to analyze candidate resumes against a job description and automatically rank them based on skill relevance, experience, and keyword similarity using Natural Language Processing (NLP) and Machine Learning techniques.

---

### 🌐 Live Website: (https://ai-resume-screener-69d23.web.app/)

---

## Features

- **Multi-Format Document Parsing:** Automatically extracts text from uploaded PDF and DOCX files.
- **Candidate Information Extraction:** Uses Regex and NLP heuristics to dynamically mine Candidate Names, Emails, Phone Numbers, and Social Links directly from unstructured resume text.
- **Advanced Weighted Scoring:** A sophisticated ranking engine that goes beyond simple keyword matching:
    - **Skill Relevance (50%):** TF-IDF and Cosine Similarity for deep technical overlap.
    - **Experience (25%):** Automated years-of-experience detection and scaling.
    - **Education (15%):** Heuristic degree level analysis (PhD, Master, Bachelor).
    - **Projects (10%):** Evaluation of practical portfolio and project prevalence.
- **Explainability & Score Breakdown:** Click any candidate row to expand a detail panel showing:
    - **Per-Component Score Bars:** Visual breakdown of Skill Match, Experience, Education, and Projects scores with animated progress bars and weight labels.
    - **Final Score Summary:** Weighted composite score displayed prominently.
    - **Skill Match Highlights:** Matched skills (green) and Missing skills (red) tags for instant gap analysis.
- **Backend Logging:** Structured request lifecycle logging with timestamps — tracks JD skill extraction, per-resume processing, score breakdowns, ranking results, and total processing time.
- **Dynamic Visual Dashboard:** Premium UI featuring:
    - **Animated Score Bars:** Horizontal charts with dynamic color grading (Green/Yellow/Red).
    - **Attribute Badges:** Instant visibility into Experience, Education, and Project scale.
    - **Glowing Highlights:** Visual differentiation of Matched vs. Missing technical skills.
- **Firebase Authentication:** Secure user access with:
    - **Email/Password Sign-In:** Standard credential-based login with real-time password complexity validation.
    - **Google Sign-In:** One-click OAuth authentication.
    - **Secure Session Management:** Uses `browserSessionPersistence` for session-based security (auto-logout on tab close).
- **Profile Management:** Dynamic user profile menu with hover/click support and the ability to update display names instantly.
- **Mobile & Tablet Friendly:** Fully responsive design:
    - **Table-to-Card Layout:** On mobile, dense results tables are converted into beautiful, digestible candidate cards.
    - **Optimized Touch Targets:** All buttons and inputs meet the 48px touch-friendly standard.
    - **Fluid Scaling:** Viewport-aware layout ensures a premium experience across all device sizes.
- **FastAPI Backend:** High-performance, async-ready REST API.

## Project Structure

```text
├── backend/
│   ├── main.py                 # FastAPI Application Handlers
│   └── services/               # Core NLP, Extraction, and Scoring Logic
├── frontend/
│   ├── index.html              # UI Structure & Auth Modal
│   ├── style.css               # Premium Styling, Animations & Responsive UI
│   └── app.js                  # Firebase Integration, UI Logic & Animations
├── firebase.json               # Firebase Hosting Configuration
├── .firebaserc                 # Firebase Project Link
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
└── notebooks/
    └── evaluation.ipynb        # Jupyter Notebook for scoring evaluation
```

## Setup & Local Development

1. **Clone and Setup Virtual Environment:**
   ```bash
   git clone <https://github.com/saaket2006/ai_resume_screener.git>
   cd ai_resume_screener
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The system will automatically download the required `en_core_web_sm` spaCy model upon first run).*

3. **Run the Backend API:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The API will be live at `http://127.0.0.1:8000`.

4. **Launch the Frontend:**
   Simply open `frontend/index.html` in your web browser, or serve it via a local static server:
   ```bash
   # From the root directory
   npx serve frontend/
   # OR
   python -m http.server -d frontend 3000
   ```

## Demonstration

1. Open the UI and complete the **Security Login**.
2. Paste **any** Job Description (e.g., "Looking for a Python backend engineer with FastAPI and NLP experience..."). The pipeline mathematically reacts to whatever keywords you provide.
3. Upload the resumes (PDF/DOCX) of candidates to be ranked.
4. Click **Rank Candidates** and observe the highly accurate similarities and highlighted skill gaps!
5. **Click any candidate row** to expand the score breakdown panel.
6. Check the **backend terminal** for detailed structured logs showing the full scoring pipeline and timing.

## Evaluation

Examine `notebooks/evaluation.ipynb` to explore the vector space model, demonstrating how the raw text data is transformed into TF-IDF numerical matrices and how Cosine Similarity calculates spatial relevance between document vectors.

## Deployment Guide

### Frontend (Firebase Hosting)

1.  **Install Firebase CLI:** `npm install -g firebase-tools`
2.  **Login to Firebase:** `firebase login`
3.  **Deploy:** `firebase deploy --only hosting`
    Your app will be live at `https://<your-project-id>.web.app`.

### Backend (Railway / Render / Google Cloud Run)

The FastAPI backend can be deployed to any cloud provider that supports Python/Uvicorn:

1.  **Prepare for Deployment:** Ensure your `requirements.txt` contains all dependencies.
2.  **Environment Variables:** Configure necessary environment variables in your cloud dashboard.
3.  **CORS:** Update the `allow_origins` in `backend/main.py` with your production frontend URL.
4.  **Deploy Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
