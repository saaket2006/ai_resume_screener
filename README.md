# AI Resume Screening & Candidate Ranking System

An end-to-end AI-powered system designed to analyze candidate resumes against a job description and automatically rank them based on skill relevance, experience, and keyword similarity using Natural Language Processing (NLP) and Machine Learning techniques.

## Features

- **Multi-Format Document Parsing:** Automatically extracts text from uploaded PDF and DOCX files.
- **Candidate Information Extraction:** Uses Regex and NLP heuristics to dynamically mine Candidate Names, Emails, Phone Numbers, and Social Links directly from unstructured resume text.
- **Advanced Weighted Scoring:** A sophisticated ranking engine that goes beyond simple keyword matching:
    - **Skill Relevance (50%):** TF-IDF and Cosine Similarity for deep technical overlap.
    - **Experience (25%):** Automated years-of-experience detection and scaling.
    - **Education (15%):** Heuristic degree level analysis (PhD, Master, Bachelor).
    - **Projects (10%):** Evaluation of practical portfolio and project prevalence.
- **Dynamic Visual Dashboard:** Premium UI featuring:
    - **Animated Score Bars:** Horizontal charts with dynamic color grading (Green/Yellow/Red).
    - **Attribute Badges:** Instant visibility into Experience, Education, and Project scale.
    - **Glowing Highlights:** Visual differentiation of Matched vs. Missing technical skills.
- **FastAPI Backend:** High-performance, async-ready REST API.
- **Modern Web Interface:** A pristine vanilla HTML/CSS/JS frontend with glassmorphism, background mesh animations, and responsive design.

## Project Structure

```text
├── backend/
│   ├── main.py                 # FastAPI Application Handlers
│   └── services/               # Core NLP, Extraction, and Scoring Logic
├── frontend/
│   ├── index.html              # UI Structure
│   ├── style.css               # Premium Styling & Animations
│   └── app.js                  # Frontend State & API Integration
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
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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

1. Open the UI.
2. Paste **any** Job Description (e.g., "Looking for a Python backend engineer with FastAPI and NLP experience..."). The pipeline mathematically reacts to whatever keywords you provide. Keep the Job Description as descriptive as possible about the role to increase the accuracy and efficiency of the process.
3. Upload the resumes of candidates which are to be ranked.
4. Click **Rank Candidates** and observe the highly accurate similarities and highlighted skill gaps, along with the dynamically acquired candidate contact information!

## Evaluation

Examine `notebooks/evaluation.ipynb` to explore the vector space model, demonstrating how the raw text data is transformed into TF-IDF numerical matrices and how Cosine Similarity calculates spatial relevance between document vectors.
