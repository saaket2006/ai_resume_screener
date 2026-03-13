---
description: How the AI Resume Screener works and how to test it
---

# AI Resume Screener & Candidate Ranking System Workflow

This document explains the end-to-end process of the AI Resume Screener, detailing how a job description is compared against candidate resumes to produce an intelligent ranking.

## 1. The Core Objective
Recruiters often receive hundreds of resumes for a single role. The objective of this system is to ingest a **Job Description (JD)** and multiple **Resumes (PDF or Word Documents)**, computationally "read" them, and return a ranked list indicating which candidates are the strongest match based strictly on the text and skills.

## 2. System Architecture & Flow
The process follows these steps:

1. **Document Ingestion:** The user provides the JD and uploads resume files via the frontend interface.
2. **Text Extraction:** Forms of binary data (PDF/DOCX) are decoded into raw, plain text by `PyPDF2` and `python-docx` respectively.
3. **NLP Preprocessing:** The raw text is cleaned using Natural Language Processing (via `spaCy`).
    *   **Lowercasing:** Standardizes all text (e.g., `Python` becomes `python`).
    *   **Stopword Removal:** Strips out filler words like "and", "the", "a", which carry no technical relevance.
    *   **Lemmatization:** Reduces words to their base form (e.g., `developed` becomes `develop`).
4. **Skill Extraction:** A custom heuristic scans the cleaned text and identifies technical skills (like `AWS`, `FastAPI`, `scikit-learn`), categorizing them into:
    *   *Matched Skills* (found in both JD and Resume)
    *   *Missing Skills* (found in JD, but missing from Resume)
5. **Vectorization & Similarity Scoring:** 
    *   The system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to mathematically score words based on how frequently they appear in a resume versus how common they are across *all* resumes. This converts the documents into a mathematical "Space" or "Vector Matrix".
    *   It then uses **Cosine Similarity** to calculate the angle between the Job Description vector and each Resume vector. The closer the angle is to 0, the more similar the texts are, yielding a higher percentage score.

---

## 3. Practical Example & Testing

The system supports **ANY Job Description** you provide! You are not limited to the pre-written examples. The TF-IDF vectorizer dynamically maps the unique terms of whichever JD you paste into the system at runtime, calculating real-time similarities against the uploaded resumes.

Follow these steps to run a practical test of the system locally.

### Start the Server Core
1. Open up a terminal in your project root structure (`g:\Projects\Launched\ai_resume_screener`).
2. Activate your virtual environment and run the backend.
```bash
venv\Scripts\activate.bat
cd backend
uvicorn main:app --reload
```

### Accessing the Interface
// turbo
3. Serve the frontend. In a new terminal tab at the project root, run:
```bash
python -m http.server -d frontend 3000
```
Navigate to `http://localhost:3000` in your web browser.

### Running a Test Scenario
1. **The Job Description**: In the text area, paste *any* job description you find online, or try the following backend-focused example:
   > *We are looking for a Web Development engineer with strong Python, FastAPI, and NLP experience. Must know scikit-learn and spaCy. Cloud deployment experience using Docker and AWS is a huge plus.*
     
2. **The Resumes**: In the file upload zone, upload the three mock realistic resumes located in `g:\Projects\Launched\ai_resume_screener\data`:
   * `resume_1_realistic_ai.docx` (Highly detailed AI/Software candidate—Saaket. Strong match for the JD above with Python, FastAPI, AWS, scikit-learn)
   * `resume_2_realistic_data_science.docx` (Data Scientist candidate—Elena. Medium match with Python and basic ML, but missing API/backend tooling)
   * `resume_3_realistic_frontend.docx` (Frontend Developer candidate—Marcus. Low match with no backend or Python experience, but the system will dynamically detect his implicit 'Web Development' skills like HTML and React!)

3. **Results**: Click **Rank Candidates**.
   * You will see the system gracefully extract the Candidate's Name, Email, and Phone directly from the raw resume text.
   * `Saaket Baldawa` will calculate as Rank #1 with a remarkably high score, accurately mirroring the backend JD requirements.
   * The new **Semantic Expansion** engine will detect 'Web Development' in the JD and automatically scan for the presence of specific web tools (HTML, CSS, React, etc.) across all candidates!
   * You can visually inspect the exact missing skills that the system flagged.
