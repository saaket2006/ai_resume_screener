# AI Resume Screening & Candidate Ranking System

An end-to-end AI-powered system designed to analyze candidate resumes against a job description and automatically rank them based on skill relevance, experience, and keyword similarity using Natural Language Processing (NLP) and Machine Learning techniques.

---

### 🌐 Live Website: (https://ai-resume-screener-69d23.web.app/)

---

## ✨ Features

### 🧾 Core Functionality

* **Professional Footer**
  Persistent dashboard footer with copyright information and developer credits.

* **Multi-Format Document Parsing**
  Seamlessly extracts text from **PDF** and **DOCX** files.

* **Candidate Information Extraction**
  Leverages **Regex** and **NLP heuristics** to extract:

  * Candidate names
  * Email addresses
  * Phone numbers
  * Social/profile links
    from unstructured resume content.


### 🧠 Intelligent Scoring Engine

A powerful ranking system that goes beyond basic keyword matching:

* **Skill Relevance (50%)**
  Uses *TF-IDF* and *Cosine Similarity* for deep technical alignment.

* **Experience (25%)**
  Automatically detects and scales years of experience.

* **Education (15%)**
  Heuristic-based degree classification (*PhD, Master’s, Bachelor’s*).

* **Projects (10%)**
  Evaluates practical experience through project analysis.


### 📊 Explainability & Transparency

* **Detailed Score Breakdown**
  Expand any candidate to view:

  * Animated progress bars
  * Weighted scoring contributions
  * Clear evaluation insights


### 📈 Dynamic Visual Dashboard

* **Animated Score Bars**
  Horizontal charts with intuitive color grading:

  * 🟢 High match
  * 🟡 Moderate match
  * 🔴 Low match

* **Attribute Badges**
  Quick insights into:

  * Experience
  * Education
  * Project strength

* **Skill Highlights**
  Clear distinction between:

  * ✅ Matched skills
  * ❌ Missing skills


### 🔐 Authentication & Security

* **Firebase Authentication**

  * Email/Password login with real-time validation
  * Google OAuth (one-click sign-in)

* **Secure Session Management**
  Uses `browserSessionPersistence` for automatic logout on tab close.


### 👤 User Profile Management

* Interactive profile menu with hover/click support
* Instant display name updates


### 📱 Responsive Design

* **Mobile & Tablet Optimized**

  * Table → Card layout transformation for better readability
  * Clean and modern UI across all devices

* **Touch-Friendly Design**
  All elements follow the **48px touch target standard**.

* **Fluid Scaling**
  Viewport-aware layout ensures a consistent experience on any screen size.


### ⚙️ Backend & Performance

* **FastAPI Backend**
  High-performance, async-ready REST API.

* **Structured Logging**
  Tracks:

  * Job description skill extraction
  * Resume processing lifecycle
  * Score breakdowns
  * Ranking results
  * Total processing time

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
   git clone https://github.com/saaket2006/ai_resume_screener.git
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

## Evaluation

Examine `notebooks/evaluation.ipynb` to explore the vector space model, demonstrating how the raw text data is transformed into TF-IDF numerical matrices and how Cosine Similarity calculates spatial relevance between document vectors.

2.  **Environment Variables:** Configure necessary environment variables in your cloud dashboard.
3.  **CORS:** Update the `allow_origins` in `backend/main.py` with your production frontend URL.
4.  **Deploy Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
