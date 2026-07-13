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


### 🧠 Semantic Scoring & Normalized Skill Layer

A powerful, multi-tier ranking system that goes beyond simple keyword match lookups:

* **Normalized Skill Intelligence**
  Handles skill aliases, abbreviations, technology hierarchies, and domain families (e.g. mapping "ReactJS" to "React", or "FastAPI" under backend framework families).
  
* **Semantic Matching Engine**
  Performs deep semantic checks to resolve relationship paths and assign weighted relevance scores for candidate profile matching.

* **Weighted Attribute Breakdown**
  - **Technical Skill Matching (50%)**: Direct and resolved semantic alignments.
  - **Work Experience (25%)**: Professional tenure and relevant internship adjustments.
  - **Education Level (15%)**: PhD, Master's, Bachelor's degree tiers.
  - **Projects Focus (10%)**: Matching project count target checks.


### 🔄 Staged Analysis Pipeline (Event-Driven)

Processes resumes through a clean, linear, decoupled analysis pipeline where each stage builds on structured outputs of the previous:
1. **Resume Text Extraction**: Raw file parser.
2. **Skill Extraction**: spaCy/Regex NER.
3. **Semantic Matching**: Mapped aliases, hierarchies, and technological families.
4. **Scoring**: Computes sub-scores and TF-IDF document similarity.
5. **Explanation Building**: Assembles structured presentations.
6. **Persistence**: Saves records transactionally to the database.


### 📊 Explainable Scoring Engine (XAI)

* **Multi-Level Explanations**
  Provides presentation-independent explanations available in **Summary** and **Detailed** formats in the user interface (and **Technical** formats internally).
  
* **Structured Evidence Logging**
  Collects specific reasons points were awarded or deducted along with structured `Evidence` nodes (e.g., exact matches, alias matches, project gaps) for future extensibility.
  
* **Collapsible breakdowns**
  Features sleek, non-cluttering expandable UI sections showing overall matching summaries and detailed evidence blocks.


## 🚀 Future-Proofing Roadmap

We have planned the following lightweight abstractions to enhance the system's observability and extensibility:

1. **Pipeline Context Object**
   Transition to a lightweight `AnalysisContext` passed into each stage's `execute(context)` call, containing `request_id`, `resume_id`, `candidate_id`, timestamps, and performance metrics.
2. **Pipeline Metrics**
   Introduce structured instrumentation to record start/end times and execution durations per stage for visual performance dashboards.
3. **Pipeline Hooks**
   Define lifecycle triggers (`Before Stage`, `After Stage`, `On Error`) to plug in logging, auditing, and real-time monitoring without changing individual stage logic.
4. **Unified Configuration**
   Inject an immutable pipeline-level configuration object for cleaner dependency management.
5. **Error Recovery Tiers**
   Support configure-per-stage error actions (`Retry`, `Skip`, `Abort`) to handle transient external OCR or LLM API network disruptions.


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
