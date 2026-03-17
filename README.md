# AI Resume Screening & Candidate Ranking System

An end-to-end AI-powered system designed to analyze candidate resumes against a job description and automatically rank them based on skill relevance, experience, and keyword similarity using Natural Language Processing (NLP) and Machine Learning techniques.

## Features

- **Multi-Format Document Parsing:** Automatically extracts text from uploaded PDF and DOCX files.
- **Candidate Information Extraction:** Uses Regex and NLP heuristics to dynamically mine Candidate Names, Emails, and Phone Numbers directly from unstructured resume text.
- **NLP Preprocessing:** Utilizes `spaCy` to process text (lowercasing, stopword removal, lemmatization).
- **Skill Extraction:** Basic Keyword Extraction system identifying technical skills and highlighting missing/matched skills.
- **TF-IDF & Cosine Similarity:** Employs `scikit-learn`'s `TfidfVectorizer` to map documents into vector space and `cosine_similarity` to calculate highly accurate match scores against the provided Job Description.
- **FastAPI Backend:** High-performance, async-ready REST API.
- **Modern Web Interface:** A pristine vanilla HTML/CSS/JS frontend featuring drag-and-drop file uploads, dynamic ranking tables, and glassmorphism UI.

## Project Structure

```text
├── backend/
│   ├── main.py                 # FastAPI Application
│   └── services/               # Core logic (Document extraction, NLP, Scoring)
├── frontend/
│   ├── index.html              # UI Structure
│   ├── style.css               # Styling
│   └── script.js               # API Integration Logic
├── data/                       # Sample Resumes (DOCX)
├── notebooks/
│   └── evaluation.ipynb        # Jupyter Notebook demonstrating scoring math
└── requirements.txt            # Python Dependencies
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
