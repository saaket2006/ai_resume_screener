# Codebase Audit Report

## Audit Metadata

- **Date:** 2026-09-09
- **Repository:** `saaket2006/ai_resume_screener`
- **Scope:** Complete repository (backend, frontend, knowledge_base, tests, notebooks, configuration, dependencies, database migrations, CI/CD artifacts)
- **Mode:** Read-only audit
- **Files inspected:** 87 files across all directories
- **Tests/checks executed:**
  - `.\venv\Scripts\python -m pytest` (failed: missing `httpx` in virtual environment)
  - `.\venv\Scripts\python -m pytest tests/test_recruiter.py` (failed: mock assertion mismatch)
  - `.\venv\Scripts\python -m pytest backend/tests/test_recruiter.py --noconftest` (failed: `get_recruiter_stats` mock subscript error)
  - `.\venv\Scripts\python -m pytest backend/tests/services/xai/test_evidence.py --noconftest` (passed: 5 passed)
  - `.\venv\Scripts\python -m pytest backend/tests/test_info_extractor.py backend/tests/services/test_info_extractor.py backend/tests/services/xai/test_formatter.py --noconftest` (passed: 19 passed)
  - `.\venv\Scripts\python -m alembic current` (passed: database at head `7fa1cda07226`)
  - `.\venv\Scripts\python -m alembic check` (passed: no schema drift between models and live DB)
  - `Get-ChildItem -Path frontend -Filter *.js -Recurse | ForEach-Object { node --check $_.FullName }` (passed: 100% valid JS syntax)
  - AST / Source code inspection of Python import trees and pipeline orchestration

---

# Executive Summary

A comprehensive read-only audit of the `ai_resume_screener` codebase was performed across all architectural layers. The repository implements an AI-driven resume screening and ranking platform featuring a FastAPI backend, a vanilla HTML/CSS/JS frontend with Tailwind CSS and GSAP animations, an Alembic database schema with PostgreSQL/Supabase backing, and heuristic NLP extraction.

While the user interface design, visual styling, and architectural intentions are ambitious and well-structured in parts, **the application currently suffers from critical defects that break core functionality at runtime**:

1. **Core Pipeline Truncation (AUDIT-001):** `AnalysisPipeline.run_analysis` in `backend/services/pipeline/orchestrator.py` was truncated mid-function after Stage 4. Stages 5 (Scoring), 6 (XAI Explanation), and 7 (Recommendations) are never executed, and the function implicitly returns `None`. Downstream callers crash with `AttributeError: 'NoneType' object has no attribute 'status'` on every resume screening attempt.
2. **Missing Runtime Dependency (AUDIT-002):** `httpx` is required by `llm_enhancer.py` (which is imported unconditionally by `backend.services.recommendations.__init__`) and by Starlette `TestClient` in tests. `httpx` is missing from the virtual environment `venv`, crashing imports and blocking the test suite.
3. **Broken Clone/Deployment Setup (AUDIT-003, AUDIT-004):** Both `alembic/` (all 8 migration scripts and `env.py`) and `frontend/firebase-config.js` are ignored by `.gitignore`. Any fresh clone lacks database migrations and fails to load frontend JavaScript (crashing the static ES module graph with a 404 on `firebase-config.js`).
4. **Severe Security Credential Leakage (AUDIT-005):** The workspace `.env` contains plaintext live credentials for a Supabase PostgreSQL instance (including username and password), a live Google email app password, and a production JWT secret.
5. **Catastrophic Extraction False Positives (AUDIT-006):** In `info_extractor.py`, regexes for degrees match standard English words: `"me"` matches Master of Engineering (`m.e`), `"be"` matches Bachelor of Engineering (`b.e`), and `"ms"` matches MS Excel/Office/Word. Consequently, almost all candidate resumes are erroneously classified as holding a Master's or Bachelor's degree.
6. **CORS Misconfiguration (AUDIT-007):** `ALLOWED_ORIGINS` defaults to an empty list and is not provided in `.env.example` or `.env`, causing browser cross-origin requests to be blocked by default.

---

# Severity Summary

| Severity | Count |
|---|---:|
| CRITICAL | 5 |
| HIGH | 8 |
| MEDIUM | 9 |
| LOW | 8 |
| INFO | 4 |
| **Total** | **34** |

---

# Critical Findings

* **ID:** AUDIT-001
* **Severity:** CRITICAL
* **Category:** Pipeline / Business Logic
* **Location:** `backend/services/pipeline/orchestrator.py:85-89`
* **Issue:** `AnalysisPipeline.run_analysis` is truncated mid-function after Stage 4, omitting Stages 5-7 and omitting the return statement.
* **Evidence:** Lines 85-89 end with:
  ```python
  # Stage 4: Scoring Profile Resolution
  context = await self.run_stage_with_metrics(self.profile_stage, context)
  ```
  The file ends immediately after line 89. Stages 5 (`ScoringStage`), 6 (`ExplanationBuildingStage`), and 7 (`RecommendationBuildingStage`) are never invoked, and there is no return statement. The method implicitly returns `None`. In `backend/services/screening_service.py:66`, the code executes:
  ```python
  if recommendation_result.status != "success":
  ```
  This immediately raises `AttributeError: 'NoneType' object has no attribute 'status'`.
* **Impact:** Every resume screening request in both candidate and recruiter flows crashes immediately with a 500 error.
* **Flow:** `API endpoint (/candidate/process or /recruiter/process) → screen_resumes() → pipeline.run_analysis() → returns None → screening_service.py:66 crashes`
* **Related files:** `backend/services/pipeline/orchestrator.py`, `backend/services/screening_service.py`, `backend/services/pipeline.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Restore Stages 5-7 and `return context.event` from `backend/services/pipeline.py:1011-1020` into `orchestrator.py`.

---

* **ID:** AUDIT-002
* **Severity:** CRITICAL
* **Category:** Dependency & Runtime Stability
* **Location:** `backend/services/recommendations/llm_enhancer.py:4`, `backend/services/recommendations/__init__.py:2`, `backend/tests/conftest.py:2`
* **Issue:** `httpx` is imported at top level in `llm_enhancer.py` and `conftest.py`, but is missing from the virtual environment.
* **Evidence:** Running `.\venv\Scripts\python -c "import backend.services.recommendations"` fails with:
  `ModuleNotFoundError: No module named 'httpx'`
  originating from `backend/services/recommendations/builder.py:5` which imports `llm_enhancer.py`. Running `pytest` fails test collection across `backend/tests/` with `RuntimeError: The starlette.testclient module requires the httpx package to be installed.`. While `httpx` is declared in `requirements.txt` line 25, it was never installed into the active `venv`.
* **Impact:** Any code importing the recommendations service or executing the test suite fails immediately.
* **Flow:** `import backend.services.recommendations → builder.py → llm_enhancer.py → import httpx (crash)`
* **Related files:** `backend/services/recommendations/llm_enhancer.py`, `backend/services/recommendations/builder.py`, `backend/services/recommendations/__init__.py`, `backend/tests/conftest.py`, `requirements.txt`
* **Confidence:** Confirmed
* **Suggested investigation:** Run `pip install -r requirements.txt` in the environment to install `httpx`, and make the LLM enhancer import lazy or conditional.

---

* **ID:** AUDIT-003
* **Severity:** CRITICAL
* **Category:** Database & Deployment Configuration
* **Location:** `.gitignore:27`, `alembic/`
* **Issue:** `.gitignore` line 27 contains `alembic`, completely excluding all database migrations from version control.
* **Evidence:** Running `git ls-files alembic` produces no output. Running `git status --ignored -s` lists `!! alembic/`. The repository contains 8 version migration scripts and `env.py` locally, but NONE of them are tracked in git. When this repository is cloned onto a new machine or deployment environment, the `alembic/` directory does not exist.
* **Impact:** Database migrations cannot be deployed or executed on any fresh environment, breaking the core instruction in `README.md` (`alembic upgrade head`).
* **Flow:** `git clone → alembic upgrade head → Directory alembic does not exist`
* **Related files:** `.gitignore`, `alembic.ini`, `alembic/env.py`, `alembic/versions/*`
* **Confidence:** Confirmed
* **Suggested investigation:** Remove `alembic` from `.gitignore` and commit the `alembic/` directory.

---

* **ID:** AUDIT-004
* **Severity:** CRITICAL
* **Category:** Frontend & Deployment Configuration
* **Location:** `.gitignore:36`, `frontend/firebase-config.js`, `frontend/assets/js/firebase-init.js:3`
* **Issue:** `.gitignore` line 36 excludes `frontend/firebase-config.js`, which is statically imported by all frontend pages.
* **Evidence:** In `frontend/assets/js/firebase-init.js`:
  ```javascript
  import { firebaseConfig } from "../../firebase-config.js?v=5";
  ```
  `firebase-init.js` is imported by `login.js`, which is imported by `app.js`. `app.js` is included via `<script type="module">` in `index.html`, `recruiter.html`, `candidate.html`, and `onboarding.html`. Because `firebase-config.js` is git-ignored and not committed (`git ls-files frontend/firebase-config.js` returns empty), on any clone the browser receives a 404 for `firebase-config.js`, which fails the entire ES module graph and prevents all JavaScript from executing.
* **Impact:** Complete failure of all frontend JavaScript on any cloned or deployed environment.
* **Flow:** `Browser loads page → app.js → login.js → firebase-init.js → imports missing firebase-config.js → Uncaught TypeError / Failed to load module script`
* **Related files:** `.gitignore`, `frontend/firebase-config.js`, `frontend/assets/js/firebase-init.js`, `frontend/assets/js/app.js`
* **Confidence:** Confirmed
* **Suggested investigation:** Provide a committed `frontend/firebase-config.example.js` or include a template and update setup documentation.

---

* **ID:** AUDIT-005
* **Severity:** CRITICAL
* **Category:** Security / Secrets Management
* **Location:** `.env:11-21`, `.env.example:2-8`
* **Issue:** Live cloud database credentials, live email account password, and production JWT secret committed/stored in plaintext in configuration files.
* **Evidence:**
  - `.env` line 17: `DATABASE_URL="postgresql://postgres.zdilhdnacvuvyhtuzkui:airesumescreener@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"` contains active credentials (password `airesumescreener`) to an AWS-hosted Supabase database.
  - `.env` line 11-12: `EMAIL_USER="airesumescreener@gmail.com"`, `EMAIL_PASS="rfvsmgzisfqpdbvz"` contains a plaintext 16-character Google App Password.
  - `.env` line 21: `JWT_SECRET="9df52ab86f78ea2871b6973dfd9f8c6913e2f9d863f683a45fb22060da928fbb"` contains a production-grade secret.
  - `.env.example` lines 2-8 contains real Firebase project IDs and API keys (`ai-resume-screener-69d23`).
* **Impact:** Full database read/write/drop access, ability to forge arbitrary JWT tokens and escalate to recruiter role, unauthorized access to user personal data and resumes, and potential email spam abuse.
* **Flow:** Any party with repository or workspace access can connect directly to the database and decrypt/modify all user records.
* **Related files:** `.env`, `.env.example`, `backend/config.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Immediately rotate the Supabase database password, revoke the Google App Password, generate a new JWT secret, and scrub secrets from local files.

---

# High-Severity Findings

* **ID:** AUDIT-006
* **Severity:** HIGH
* **Category:** Information Extraction / NLP
* **Location:** `backend/services/info_extractor.py:108-111`
* **Issue:** Education extraction regex matches common English words ("me", "be", "ms"), erroneously awarding advanced degrees to all candidates.
* **Evidence:**
  - Line 108: `re.search(r'\b(master|m\.?s|m\.?a|mba|m\.?tech|m\.?e)\b', text_lower)` contains `m\.?e` (which matches the pronoun "me") and `m\.?s` (which matches "ms" in "MS Excel", "MS Office").
  - Line 110: `re.search(r'\b(bachelor|b\.?s|b\.?a|b\.?tech|b\.?e|undergraduate)\b', text_lower)` contains `b\.?e` (which matches the verb "be").
  - Verification:
    - `extract_education("Contact me at test@example.com")` returns `"Master"`.
    - `extract_education("I will be graduating in 2024")` returns `"Bachelor"`.
    - `extract_education("Skills: MS Excel, Python")` returns `"Master"`.
* **Impact:** Because almost all English resumes include "me" (e.g., "Contact me", "About me") or "be", virtually every candidate is classified as holding a Master's or Bachelor's degree, completely compromising the education scoring metric (`edu_score`) and recruiter analytics.
* **Flow:** `Raw resume text → extract_education() → matched 'me' → returns 'Master' → ScoringStage awards 80-100% education score`
* **Related files:** `backend/services/info_extractor.py`, `backend/services/pipeline/stages.py`, `backend/services/scoring_service.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Require strict punctuation, word boundaries, or preceding context (e.g., `\bM\.E\.\b` or `\bB\.E\.\b` with required periods or contextual tokens like "degree in").

---

* **ID:** AUDIT-007
* **Severity:** HIGH
* **Category:** Security / API Integration
* **Location:** `backend/config.py:14-16`, `backend/main.py:84-95`
* **Issue:** Default `ALLOWED_ORIGINS` evaluates to an empty list, causing CORS middleware to reject cross-origin frontend requests.
* **Evidence:** In `backend/config.py`:
  ```python
  ALLOWED_ORIGINS: List[str] = [
      origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "").split(",") if origin.strip()
  ]
  ```
  Neither `.env` nor `.env.example` specifies `ALLOWED_ORIGINS`. By default, `settings.ALLOWED_ORIGINS` is `[]`. In `main.py`, `CORSMiddleware` is configured with `allow_origins=[]`. When a browser runs the frontend on `http://localhost:3000` and calls the backend on `http://127.0.0.1:8000`, the preflight and GET/POST requests are blocked by the browser CORS policy.
* **Impact:** Frontend application cannot connect to the backend server in default setups.
* **Flow:** `Browser fetch('http://127.0.0.1:8000/api/...') → OPTIONS preflight → CORSMiddleware blocks due to empty origin list`
* **Related files:** `backend/config.py`, `backend/main.py`, `.env.example`
* **Confidence:** Confirmed
* **Suggested investigation:** Add sensible local development defaults (e.g., `http://localhost:3000,http://127.0.0.1:3000`) and document in `.env.example`.

---

* **ID:** AUDIT-008
* **Severity:** HIGH
* **Category:** API / Recruiter Architecture
* **Location:** `backend/routers/recruiter.py`
* **Issue:** Missing endpoints to list screened candidates or retrieve individual candidate evaluation details for recruiters.
* **Evidence:** `recruiter.py` implements:
  - `POST /recruiter/process`
  - `GET /recruiter/profiles`
  - `GET /recruiter/jobs`, `POST /recruiter/jobs`, `PUT /recruiter/jobs/{id}`, `DELETE /recruiter/jobs/{id}`, `DELETE /recruiter/jobs/{id}/delete`
  - `GET /recruiter/stats`
  There is NO endpoint to retrieve candidates screened for a job description (e.g., `GET /recruiter/jobs/{id}/candidates` or `GET /recruiter/candidates/{id}`). While candidate data and scan results are saved in the database during `POST /recruiter/process`, there is no API route in the entire backend allowing recruiters to ever query or view those records again.
* **Impact:** Once the recruiter navigates away from the screening results page, candidate evaluations are lost from the UI and cannot be revisited.
* **Flow:** `Recruiter screens resumes → results displayed in memory → page refreshed → candidate records exist in DB but are unretrievable via API`
* **Related files:** `backend/routers/recruiter.py`, `frontend/assets/js/pages/recruiter.js`
* **Confidence:** Confirmed
* **Suggested investigation:** Add `GET /api/recruiter/jobs/{jd_id}/candidates` and `GET /api/recruiter/candidates/{scan_id}` endpoints.

---

* **ID:** AUDIT-009
* **Severity:** HIGH
* **Category:** Tests & Test Reliability
* **Location:** `tests/test_recruiter.py:13,19`, `backend/tests/test_recruiter.py:113,122`
* **Issue:** Recruiter stats tests fail due to mismatched database query mocks.
* **Evidence:**
  - In `tests/test_recruiter.py:13`, the test configures:
    ```python
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
    ```
    However, `get_recruiter_stats` begins by executing `db.query(...).join(...).filter(...).first()`. Because `.first()` is not mocked, it returns a `MagicMock`, resulting in `AssertionError: assert <MagicMock ...> == 0` on line 19.
  - In `backend/tests/test_recruiter.py:113`, `.all()` is mocked to return `[scan1, scan2, scan3]`. But line 313 of `recruiter.py` queries `ScanResult.analysis_metadata` (a tuple), so line 318 attempts `meta = row[0] or {}`, which raises `TypeError: 'MagicMock' object is not subscriptable`.
* **Impact:** Running recruiter tests fails 100% of the time.
* **Flow:** `pytest tests/test_recruiter.py → test_get_recruiter_stats_empty_scans FAILED`
* **Related files:** `tests/test_recruiter.py`, `backend/tests/test_recruiter.py`, `backend/routers/recruiter.py:296-318`
* **Confidence:** Confirmed (verified via pytest)
* **Suggested investigation:** Correct the mock return chains in both test files or use the in-memory SQLite fixture.

---

* **ID:** AUDIT-010
* **Severity:** HIGH
* **Category:** Tests & Test Reliability
* **Location:** `backend/tests/test_auth.py:43-44`
* **Issue:** Test calls non-existent mock assertion methods on a real SQLAlchemy session object.
* **Evidence:** In `backend/tests/test_auth.py`:
  ```python
  # Ensure add and commit are not called
  db_session.add.assert_not_called()
  db_session.commit.assert_not_called()
  ```
  `db_session` is provided by `conftest.py:db_session` as an actual SQLAlchemy `Session` (`TestingSessionLocal()`), NOT a `unittest.mock.MagicMock`. Calling `.assert_not_called()` raises `AttributeError: 'Session' object has no attribute 'assert_not_called'`.
* **Impact:** `test_signup_existing_email` cannot pass.
* **Flow:** `pytest backend/tests/test_auth.py → AttributeError on Session.assert_not_called`
* **Related files:** `backend/tests/test_auth.py`, `backend/tests/conftest.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Replace mock assertions with an actual DB query verifying no duplicate record was created: `assert db_session.query(User).filter(User.email == ...).count() == 1`.

---

* **ID:** AUDIT-011
* **Severity:** HIGH
* **Category:** Frontend ↔ Backend Contract Mismatch
* **Location:** `frontend/assets/js/pages/candidate.js:247-255`, `backend/routers/candidate.py:179-188`
* **Issue:** Candidate timeline reliability comparison accesses metadata fields that the backend endpoint never returns.
* **Evidence:** In `candidate.js`, the timeline comparison checks:
  ```javascript
  const oldestProfile = oldest.analysis_metadata?.profile_name || "General Software Engineer";
  const newestProfile = newest.analysis_metadata?.profile_name || "General Software Engineer";
  const oldestEngine = oldest.analysis_metadata?.engine_version || "v1.0.0";
  const newestEngine = newest.analysis_metadata?.engine_version || "v1.0.0";
  ```
  However, `backend/routers/candidate.py:get_candidate_resumes` constructs the response list with:
  ```python
  response_data.append({
      "id": r.id,
      "version": r.version,
      "original_filename": r.original_filename,
      "label": r.label,
      "uploaded_at": r.uploaded_at.isoformat(),
      "ats_score": score,
      "job_description_title": jd_title,
      "job_description_summary": jd_summary
  })
  ```
  `analysis_metadata` is completely omitted from the dictionary. Therefore, `oldest.analysis_metadata` is always `undefined`, and the frontend comparisons always default to `"General Software Engineer"` and `"v1.0.0"`.
* **Impact:** The "Comparison Reliability" badge shown to candidates is computed using hardcoded fallback defaults rather than actual historical analysis metadata.
* **Flow:** `GET /api/candidate/resumes → response lacks analysis_metadata → candidate.js defaults fallback strings`
* **Related files:** `backend/routers/candidate.py`, `frontend/assets/js/pages/candidate.js`
* **Confidence:** Confirmed
* **Suggested investigation:** Include necessary metadata fields (`profile_name`, `engine_version`) in the `GET /api/candidate/resumes` response.

---

* **ID:** AUDIT-012
* **Severity:** HIGH
* **Category:** Information Extraction / Document Processing
* **Location:** `backend/services/document_service.py:41-42`, `backend/config.py:25`
* **Issue:** Legacy binary `.doc` files are routed to `python-docx`, which only parses OpenXML `.docx` files.
* **Evidence:** `config.py` allows `.doc` in `ALLOWED_EXTENSIONS`. `document_service.py` executes:
  ```python
  elif filename_lower.endswith('.docx') or filename_lower.endswith('.doc'):
      return extract_text_from_docx(file_bytes)
  ```
  Inside `extract_text_from_docx`: `docx.Document(io.BytesIO(file_bytes))`. `python-docx` is strictly a zip-based OpenXML parser; passing an OLE2 binary `.doc` raises `docx.opc.exceptions.PackageNotFoundError: File is not a zip file`.
* **Impact:** Any user uploading a `.doc` file encounters an unhandled exception or 400 error.
* **Flow:** `Upload .doc file → extract_text() → extract_text_from_docx() → docx.Document() raises PackageNotFoundError`
* **Related files:** `backend/services/document_service.py`, `backend/config.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Remove `.doc` from `ALLOWED_EXTENSIONS` or incorporate a dedicated `.doc` parser (e.g., `antiword` or `catdoc`).

---

* **ID:** AUDIT-013
* **Severity:** HIGH
* **Category:** Information Extraction / Data Integrity
* **Location:** `backend/services/metadata_builder.py:43-44`, `backend/routers/candidate.py:231`
* **Issue:** Candidate extracted skills are overwritten with only matched skills, discarding unmatched candidate skills from stored metadata.
* **Evidence:** In `metadata_builder.py:43-44`:
  ```python
  "skills": {
      "extracted": candidate_result.get("matched_skills", []),  # All candidate skills
      "matched": candidate_result.get("matched_skills", []),
      "missing": candidate_result.get("missing_skills", [])
  },
  ```
  `"extracted"` is assigned `matched_skills`. Any skill present on the candidate's resume that did not match the JD is silently discarded and never stored in `analysis_metadata`. When `GET /candidate/resumes/{resume_id}` reads `meta.get("skills", {}).get("extracted")`, it only reflects matching skills.
* **Impact:** Irreversible data loss in stored candidate resume snapshots; candidate profile view cannot show the candidate's full skillset.
* **Flow:** `Resume parsed → all skills extracted → metadata_builder maps matched_skills to 'extracted' → non-matching skills dropped`
* **Related files:** `backend/services/metadata_builder.py`, `backend/routers/candidate.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Pass the full list of extracted candidate skills into `build_analysis_metadata` and populate `"extracted"` with all candidate skills.

---

# Medium-Severity Findings

* **ID:** AUDIT-014
* **Severity:** MEDIUM
* **Category:** Backend Architecture / Dead Code
* **Location:** `backend/services/pipeline.py`
* **Issue:** 42KB monolithic file `pipeline.py` shadows the modular package `backend/services/pipeline/`.
* **Evidence:** Python package resolution prioritizes `backend/services/pipeline/__init__.py`. `backend/services/pipeline.py` is a monolithic copy that is never loaded by normal package imports, yet it contains the full code for Stages 5-7 that was accidentally cut from `pipeline/orchestrator.py`.
* **Impact:** Extreme developer confusion, code desynchronization, and risk of accidental module shadowing.
* **Related files:** `backend/services/pipeline.py`, `backend/services/pipeline/`
* **Confidence:** Confirmed
* **Suggested investigation:** Verify all logic in `pipeline.py` is transferred to `pipeline/`, then delete `pipeline.py`.

---

* **ID:** AUDIT-015
* **Severity:** MEDIUM
* **Category:** Dead Code / Semantic Extraction
* **Location:** `backend/services/skill_expander.py:1-78`
* **Issue:** `skill_expander.py` is completely unreferenced by the backend application.
* **Evidence:** Grep for `skill_expander` across the entire backend yields 0 results. It is only imported in `notebooks/evaluation.ipynb` with an invalid non-package import (`from services.skill_expander...`).
* **Impact:** Dead code; semantic expansion dictionaries (`SEMANTIC_SKILL_EXPANSIONS`, `SKILL_ALIASES`) are disconnected from the live screening pipeline.
* **Related files:** `backend/services/skill_expander.py`, `notebooks/evaluation.ipynb`
* **Confidence:** Confirmed
* **Suggested investigation:** Either integrate `skill_expander` into `backend/services/semantic/` or decommission it.

---

* **ID:** AUDIT-016
* **Severity:** MEDIUM
* **Category:** Business Logic / Duplicate Scoring
* **Location:** `backend/services/scoring_service.py:53-85`, `backend/services/pipeline/stages.py:297-327`
* **Issue:** Identical scoring formulas and weight calculations are implemented twice in two different services.
* **Evidence:** Both `ScoringStage` in `stages.py` and `rank_candidates` in `scoring_service.py` independently calculate `experience_score`, `education_score`, `projects_score`, and `similarity_score`. `screening_service.py` runs the pipeline (which invokes `ScoringStage`) and then immediately passes the results to `rank_candidates`, which recalculates and overwrites the exact same values.
* **Impact:** Redundant processing and high risk of logic drift if one formula is updated without updating the other.
* **Related files:** `backend/services/scoring_service.py`, `backend/services/pipeline/stages.py`, `backend/services/screening_service.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Consolidate scoring into a single canonical service called by both pipeline and ranking.

---

* **ID:** AUDIT-017
* **Severity:** MEDIUM
* **Category:** Information Extraction / NLP
* **Location:** `backend/services/info_extractor.py:51-58`
* **Issue:** Candidate name extraction heuristic selects job titles or section headings when placed at the top of resumes.
* **Evidence:** `extract_name` iterates through the first 5 non-empty lines and returns the first line having 2 to 4 words matching `^[A-Za-z\s\-\.]+$`. When a resume starts with "SOFTWARE ENGINEER" or "FULL STACK DEVELOPER", `extract_name` returns that string as the candidate's name.
* **Impact:** Candidate names in recruiter dashboards and candidate profiles display as job titles instead of real names.
* **Related files:** `backend/services/info_extractor.py`
* **Confidence:** Confirmed (verified via Python execution)
* **Suggested investigation:** Filter against common job title keywords and utilize spaCy `PERSON` entity recognition as the primary extractor with regex as fallback.

---

* **ID:** AUDIT-018
* **Severity:** MEDIUM
* **Category:** Database / Startup Concurrency
* **Location:** `backend/services/policy/default_profiles.py:87-101`, `backend/main.py:47-55`, `Procfile:1`
* **Issue:** Startup default profile seeding creates race conditions under multi-worker Gunicorn.
* **Evidence:** `Procfile` launches 4 Gunicorn workers (`-w 4`). On startup, each worker executes `seed_default_profiles(db)` at module load time. The check `if count == 0:` is not guarded by a transaction lock, and `ScoringProfile.name` does not have a `unique` constraint. Concurrent workers can simultaneously insert duplicate default scoring profiles.
* **Impact:** Duplicate scoring profiles in database under multi-worker deployments.
* **Related files:** `backend/services/policy/default_profiles.py`, `backend/main.py`, `Procfile`
* **Confidence:** Confirmed
* **Suggested investigation:** Add a `unique=True` constraint on `ScoringProfile.name` and use `INSERT ... ON CONFLICT DO NOTHING` or Alembic data migrations for seeding.

---

* **ID:** AUDIT-019
* **Severity:** MEDIUM
* **Category:** Authentication / State Management
* **Location:** `backend/routers/auth.py:63`, `backend/routers/onboarding.py:84`
* **Issue:** User JWT role claim is not refreshed upon completing onboarding.
* **Evidence:** At login/signup, a JWT is issued containing `"role": user.role.value` (`UNASSIGNED`). When the user finishes onboarding via `POST /api/onboarding`, their role is updated in the database to `RECRUITER` or `CANDIDATE`, but `submit_onboarding` returns only `{"message": "Onboarding completed successfully."}` without issuing a refreshed JWT. The client continues using the token containing `role: UNASSIGNED` until manual re-login.
* **Impact:** Any component or downstream proxy inspecting JWT claims rather than querying the database sees a stale `UNASSIGNED` role.
* **Related files:** `backend/routers/onboarding.py`, `backend/routers/auth.py`, `frontend/assets/js/pages/onboarding.js`
* **Confidence:** Confirmed
* **Suggested investigation:** Return a new JWT token from `POST /api/onboarding` and update frontend token state.

---

* **ID:** AUDIT-020
* **Severity:** MEDIUM
* **Category:** Database / Import Side-Effects
* **Location:** `backend/database/database.py:28`
* **Issue:** Synchronous database connection test executed at top-level module import.
* **Evidence:** When `database.py` is imported, lines 25-33 execute:
  ```python
  with engine.connect() as conn:
      pass
  ```
  This creates an immediate blocking network call to the Supabase pooler during module import. If network latency is high or DNS fails, importing any module that depends on `database.py` hangs for 30-60+ seconds.
* **Impact:** Fragile imports, test collection timeouts, and slow CLI tool execution.
* **Related files:** `backend/database/database.py`
* **Confidence:** Confirmed (observed during test collection)
* **Suggested investigation:** Move the connection check to FastAPI's lifespan or startup event rather than executing at module import time.

---

* **ID:** AUDIT-021
* **Severity:** MEDIUM
* **Category:** Information Extraction / Document Processing
* **Location:** `backend/services/document_service.py:28-29`
* **Issue:** DOCX parser ignores all text contained inside tables.
* **Evidence:** `extract_text_from_docx` only loops over `doc.paragraphs`:
  ```python
  for para in doc.paragraphs:
      text += para.text + "\n"
  ```
  Text in `doc.tables` is never accessed.
* **Impact:** Resumes using tables for layout, skills matrices, or education grids have significant portions of their content omitted.
* **Related files:** `backend/services/document_service.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Iterate through `doc.tables`, extracting cell text alongside paragraph text.

---

* **ID:** AUDIT-022
* **Severity:** MEDIUM
* **Category:** Code Quality / Deprecation
* **Location:** `backend/models/models.py:15,31,45,62,63,80,93,95,109`, `backend/dependencies/auth_utils.py:30,32`
* **Issue:** `datetime.datetime.utcnow()` used throughout models and token generators.
* **Evidence:** `datetime.utcnow()` is deprecated in Python 3.12+ and returns naive UTC timestamps, leading to timezone conversion inconsistencies.
* **Impact:** Future Python version incompatibility and subtle timezone comparison bugs.
* **Related files:** `backend/models/models.py`, `backend/dependencies/auth_utils.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Replace with `datetime.datetime.now(datetime.timezone.utc)`.

---

# Low-Severity Findings

* **ID:** AUDIT-023
* **Severity:** LOW
* **Category:** Dependency Management
* **Location:** `requirements.txt:7,8,11,13,20`
* **Issue:** Unused heavy Python dependencies in `requirements.txt`.
* **Evidence:** `pandas`, `numpy`, `jinja2`, `aiosmtplib`, and `passlib[bcrypt]` are declared in `requirements.txt`, but are never imported by the active application codebase. (`bcrypt` is used directly; `passlib` is not).
* **Impact:** Unnecessary deployment image size, longer build times, and increased vulnerability surface.
* **Related files:** `requirements.txt`
* **Confidence:** Confirmed
* **Suggested investigation:** Remove unused dependencies from `requirements.txt`.

---

* **ID:** AUDIT-024
* **Severity:** LOW
* **Category:** Dependency Management
* **Location:** `package.json:3`
* **Issue:** Unused npm package `cors` in frontend manifest.
* **Evidence:** `cors: ^2.8.6` is an Express/Node.js middleware package. There is no Node.js server in the repository.
* **Impact:** Pointless dependency in `node_modules`.
* **Related files:** `package.json`
* **Confidence:** Confirmed
* **Suggested investigation:** Remove `cors` from `package.json`.

---

* **ID:** AUDIT-025
* **Severity:** LOW
* **Category:** Dead Code
* **Location:** `backend/services/policy/recruiter_policy.py:1-8`, `backend/services/skills/validator.py:3-14`, `backend/services/skills/taxonomy.py:4-24`
* **Issue:** Unused classes and uncalled functions across services.
* **Evidence:**
  - `RecruiterPolicy` is an empty class with `pass`.
  - `validate_skill_name` is never called.
  - `get_taxonomy` is never called.
* **Impact:** Code bloat and maintenance confusion.
* **Related files:** Listed above.
* **Confidence:** Confirmed
* **Suggested investigation:** Remove or integrate these stubs.

---

* **ID:** AUDIT-026
* **Severity:** LOW
* **Category:** Frontend Optimization
* **Location:** `frontend/recruiter.html:275`, `frontend/candidate.html:357`, `frontend/onboarding.html:174`
* **Issue:** `landing.js` script tag included on workspace and onboarding HTML pages.
* **Evidence:** `landing.js` contains a pathname guard (`if (pathname.endsWith('index.html') || pathname === '/')`) and does nothing on other pages. Including it generates redundant HTTP requests.
* **Impact:** Minor performance overhead.
* **Related files:** `recruiter.html`, `candidate.html`, `onboarding.html`
* **Confidence:** Confirmed
* **Suggested investigation:** Remove `<script type="module" src="assets/js/landing.js"></script>` from non-landing pages.

---

* **ID:** AUDIT-027
* **Severity:** LOW
* **Category:** Code Quality / Deprecation
* **Location:** `backend/schemas/schemas.py:32,43,54,67`, `backend/services/semantic/scorer.py:27`
* **Issue:** Pydantic V2 deprecation warnings (`orm_mode` and `.dict()`).
* **Evidence:** Pydantic outputs `UserWarning: Valid config keys have changed in V2: * 'orm_mode' has been renamed to 'from_attributes'`. `scorer.py` calls `.dict()`.
* **Impact:** Console warnings during execution.
* **Related files:** `backend/schemas/schemas.py`, `backend/services/semantic/scorer.py`
* **Confidence:** Confirmed
* **Suggested investigation:** Remove `orm_mode = True` and use `from_attributes = True`, and replace `.dict()` with `.model_dump()`.

---

* **ID:** AUDIT-028
* **Severity:** LOW
* **Category:** Test Organization
* **Location:** `tests/test_recruiter.py` vs `backend/tests/test_recruiter.py`, `backend/tests/test_info_extractor.py` vs `backend/tests/services/test_info_extractor.py`, `backend/tests/test_auth.py` vs `backend/tests/routers/test_auth.py`
* **Issue:** Duplicate and fragmented test files across root `tests/` and `backend/tests/`.
* **Evidence:** `tests/test_recruiter.py` has 1 broken test, while `backend/tests/test_recruiter.py` has 3 tests. `backend/tests/test_info_extractor.py` only tests experience extraction, while `backend/tests/services/test_info_extractor.py` tests LinkedIn and education.
* **Impact:** Disorganized test suite and confusion regarding which tests to maintain.
* **Related files:** All test files mentioned above.
* **Confidence:** Confirmed
* **Suggested investigation:** Consolidate all tests into `backend/tests/` under matching domain directories.

---

* **ID:** AUDIT-029
* **Severity:** LOW
* **Category:** Repository Cleanliness / Git
* **Location:** Repository root
* **Issue:** Tracked-but-deleted files left in Git index, and committed build/cache artifacts.
* **Evidence:** `git status` shows deleted files tracked in git: `benchmark3.py`, `commit_message.txt`, `dummy.js`, `pr_description.md`, `pre_commit.js`, `submission_description.txt`. In addition, `.firebase/hosting.ZnJvbnRlbmQ.cache` and the entire `graphify-out/` folder (~1.75MB) are tracked in git.
* **Impact:** Dirty git working tree, repo clutter.
* **Related files:** `.gitignore`, `.firebase/`, `graphify-out/`
* **Confidence:** Confirmed
* **Suggested investigation:** Stage deletions with `git rm`, add `.firebase/` and `graphify-out/` to `.gitignore`, and remove them from git cache.

---

* **ID:** AUDIT-030
* **Severity:** LOW
* **Category:** Documentation Consistency
* **Location:** `README.md`
* **Issue:** Multiple factual discrepancies between README documentation and codebase reality.
* **Evidence:**
  - README line 61 claims "Tailwind v4 CSS", but `package.json` line 12 installs Tailwind `^3.4.17`.
  - README line 22-23 references a "Multi-Agent Analysis" stage that does not exist.
  - README line 10 links to live website `ai-resume-screener-69d23.web.app`, but configuration targets `nipun-platform`.
  - README lines 144 and 150 document `alembic upgrade head` and `python scratch/migrate_to_supabase.py`, but both folders are git-ignored.
* **Impact:** Misleading documentation for developers and evaluators.
* **Related files:** `README.md`, `package.json`, `firebase.json`
* **Confidence:** Confirmed
* **Suggested investigation:** Update README to accurately reflect Tailwind v3, true pipeline stages, and active Firebase domains.

---

# Informational Findings

* **ID:** AUDIT-031
* **Severity:** INFO
* **Category:** Workspace Cleanliness
* **Location:** `scratch/`
* **Issue:** `scratch/` directory contains 22 files (~5.5MB) including 16 debug PNG screenshots from earlier UI development iterations.
* **Evidence:** Files like `current_page_masterpiece.png`, `layout_shift_fixed.png`, `walkthrough_step3_clean.png`, `download_cdns.py` exist in the local workspace.
* **Impact:** Local disk usage; properly ignored by `.gitignore`.
* **Confidence:** Confirmed
* **Suggested investigation:** Clean up local development screenshots when no longer needed.

---

* **ID:** AUDIT-032
* **Severity:** INFO
* **Category:** Workspace Cleanliness
* **Location:** `.codegraph/codegraph.db`
* **Issue:** 2.46MB SQLite database generated by local code graph indexing tool.
* **Evidence:** Exists locally; properly ignored in `.gitignore`.
* **Confidence:** Confirmed
* **Suggested investigation:** Informational only.

---

* **ID:** AUDIT-033
* **Severity:** INFO
* **Category:** Routing / Hosting
* **Location:** `firebase.json:9-14`
* **Issue:** Firebase Hosting wildcard rewrite `** -> /index.html` on a multi-page static site.
* **Evidence:** Exact `.html` files (`recruiter.html`, `candidate.html`, `onboarding.html`) are served directly by Firebase Hosting. However, visiting extension-less URLs like `/recruiter` rewrites to `/index.html` where client-side JavaScript performs a redirect to `recruiter.html`.
* **Confidence:** Confirmed
* **Suggested investigation:** Add clean URL rewrites or configure `cleanUrls: true` in `firebase.json`.

---

* **ID:** AUDIT-034
* **Severity:** INFO
* **Category:** Dependency Modernization
* **Location:** `backend/services/document_service.py:2`, `requirements.txt:5`
* **Issue:** `PyPDF2` package is deprecated.
* **Evidence:** PyPDF2 outputs `DeprecationWarning: PyPDF2 is deprecated. Please move to the pypdf library instead.` on import.
* **Confidence:** Confirmed
* **Suggested investigation:** Migrate to modern `pypdf`.

---

# Authentication & Authorization Audit

### Authentication Architecture
- **JWT Issuance:** Custom tokens generated using `PyJWT` with `HS256` signed by `settings.JWT_SECRET`.
- **Token Verification:** `get_current_user` dependency (`backend/dependencies/auth_deps.py:17`) decodes the token, extracts the `"sub"` claim (email), and queries the database (`db.query(User).filter(User.email == email).first()`).
- **Google Sign-In:** `POST /api/auth/google` verifies Firebase ID tokens against Google's public x509 certificates via `pyjwt.decode(..., algorithms=["RS256"], audience=project_id)`. Upon successful verification, it registers the user if non-existent and issues a backend JWT.

### Protected Routes & Authorization Model
- **Role Enforcement:** Handled by FastAPI dependencies:
  - `require_recruiter`: Rejects non-recruiters with 403 Forbidden.
  - `require_candidate`: Rejects non-candidates with 403 Forbidden.
  - Role is checked against the database `current_user.role` object, preventing client-side role forgery.

### Findings & Missing Protections
1. **Missing Authentication on Legacy Endpoint (Partial):** `/api/process` delegates to recruiter processing, requiring `require_recruiter`. Candidate resumes submitted from the public landing page without a token fail with 401.
2. **Stale Token Role Claims:** When a user signs up or logs in before completing onboarding, their token contains `"role": "UNASSIGNED"`. After onboarding, the role is updated in PostgreSQL, but the client keeps the old token.
3. **No Brute-Force Rate Limiting on Auth Endpoints:** `POST /api/auth/login` and `POST /api/auth/signup` do not have `@limiter.limit` decorators applied, leaving them susceptible to credential stuffing.
4. **IDOR Evaluation:** Candidate routes (`/api/candidate/*`) properly filter all database queries by `Resume.candidate_id == current_user.id`. Recruiter routes (`/api/recruiter/*`) properly filter job descriptions and stats by `JobDescription.owner_id == current_user.id`. No direct IDOR vulnerabilities were found in candidate/recruiter query filters.

---

# Database Audit

### Architecture & Session Handling
- **Database Engine:** SQLAlchemy 2.0 connected via `create_db_engine(url, pool_pre_ping=True)`.
- **Session Lifecycle:** Managed via `get_db` generator dependency with `try...finally: db.close()`. All router endpoints properly yield and close sessions.
- **Transactions:** Explicit `db.commit()` and `db.rollback()` exception handlers are present across router endpoints.

### Findings
1. **Migrations Ignored by Version Control (AUDIT-003):** The `alembic/` directory is git-ignored, preventing schema history distribution.
2. **Missing Unique Constraint on `ScoringProfile.name` (AUDIT-018):** Startup seeding under multi-worker setups can create duplicate profiles.
3. **Missing Indexes on Foreign Keys:** While primary keys and `User.email` are indexed, foreign keys like `ScanResult.job_description_id`, `ScanResult.resume_id`, and `Resume.candidate_id` lack explicit indexes, which may degrade query performance as table volume grows.
4. **Startup Network Blocking (AUDIT-020):** `database.py` executes a blocking connection test at module load time.

---

# Information Extraction Audit

### Pipeline Stages
`Document Bytes` → `document_service.extract_text` → `info_extractor.py` / `skill_extractor.py` → `nlp_service.preprocess_text` → `skills.extractor` → `semantic.matcher` → `metadata_builder`

### Findings
1. **Degree Extraction False Positives (AUDIT-006):** Regex matching `"me"`, `"be"`, and `"ms"` erroneously awards Master's or Bachelor's degrees to almost all candidates.
2. **Candidate Name Extraction Bias (AUDIT-017):** Header lines containing job titles ("SOFTWARE ENGINEER") are extracted as candidate names.
3. **Unmatched Skills Dropped from Metadata (AUDIT-013):** `metadata_builder.py` sets `"extracted"` to `matched_skills`, erasing candidate skills that did not match the JD.
4. **Unsupported `.doc` Format (AUDIT-012):** `.doc` files are passed to `python-docx` and fail.
5. **Missing Table Text in DOCX (AUDIT-021):** `extract_text_from_docx` ignores text in tables.
6. **Deprecated PDF Parser (AUDIT-034):** `PyPDF2` emits deprecation warnings on every run.

---

# Pipeline & Business Logic Audit

### Pipeline Stages
1. `ResumeTextExtractionStage`
2. `SkillExtractionStage`
3. `SemanticMatchingStage`
4. `ScoringProfileResolutionStage`
5. `ScoringStage`
6. `ExplanationBuildingStage`
7. `RecommendationBuildingStage`
8. `PersistenceStage`

### Findings
1. **Pipeline Truncation (AUDIT-001):** `orchestrator.py` halts after Stage 4 and returns `None`, crashing all screening requests.
2. **Missing Dependency in Stage 7 (AUDIT-002):** `RecommendationBuildingStage` imports `builder.py` which requires `httpx`.
3. **Duplicate Scoring Math (AUDIT-016):** Formulas for experience, education, projects, and weights are duplicated identically between `stages.py:ScoringStage` and `scoring_service.py:rank_candidates`.
4. **Shadowed Monolith (AUDIT-014):** `backend/services/pipeline.py` (42KB) is shadowed by package `backend/services/pipeline/`.

---

# Frontend ↔ Backend Contract Audit

| Frontend Call | Backend Route | Method | Auth | Contract Status | Finding |
|---|---|---|---|---|---|
| `api.login` | `/api/auth/login` | POST | None | **Matched** | Valid contract |
| `api.signup` | `/api/auth/signup` | POST | None | **Matched** | Valid contract |
| `api.googleLogin` | `/api/auth/google` | POST | None | **Matched** | Hardcoded route in `api.js:179` |
| `api.getMe` | `/api/auth/me` | GET | Bearer | **Matched** | Valid contract |
| `api.getProfile` | `/api/profile` | GET | Bearer | **Matched** | Valid contract |
| `api.submitOnboarding` | `/api/onboarding` | POST | Bearer | **Matched** | Token role claim not refreshed after completion |
| `api.screenResumes` | `/api/process` | POST | Bearer (Recruiter) | **Partial Mismatch** | Comment calls it "candidate-facing ATS", but backend requires recruiter auth |
| `api.screenResumesRecruiter` | `/api/recruiter/process` | POST | Bearer (Recruiter) | **Matched** | Backend crashes at runtime due to AUDIT-001 |
| `api.screenResumeCandidate` | `/api/candidate/process` | POST | Bearer (Candidate) | **Matched** | Backend crashes at runtime due to AUDIT-001 |
| `api.getCandidateStats` | `/api/candidate/stats` | GET | Bearer (Candidate) | **Matched** | Valid contract |
| `api.getCandidateResumes` | `/api/candidate/resumes` | GET | Bearer (Candidate) | **Mismatched Shape** | Backend omits `analysis_metadata` expected by frontend timeline (AUDIT-011) |
| `api.getCandidateResumeDetails` | `/api/candidate/resumes/{id}` | GET | Bearer (Candidate) | **Matched** | Valid contract |
| `api.deleteCandidateResume` | `/api/candidate/resumes/{id}` | DELETE | Bearer (Candidate) | **Matched** | Soft deletes resume |
| `api.updateCandidateResumeLabel`| `/api/candidate/resumes/{id}/label` | PUT | Bearer (Candidate) | **Matched** | Valid contract |
| `api.updateRecommendationStatus`| `/api/candidate/resumes/{id}/recommendations/{rec_id}` | PUT | Bearer (Candidate) | **Matched** | Valid contract |
| `api.getScoringProfiles` | `/api/recruiter/profiles` | GET | Bearer (Recruiter) | **Matched** | Valid contract |
| `api.getJobs` | `/api/recruiter/jobs` | GET | Bearer (Recruiter) | **Matched** | Query param `include_archived` supported |
| `api.createJob` | `/api/recruiter/jobs` | POST | Bearer (Recruiter) | **Matched** | FormData correctly mapped to Form fields |
| `api.updateJob` | `/api/recruiter/jobs/{id}` | PUT | Bearer (Recruiter) | **Matched** | FormData correctly mapped to Form fields |
| `api.archiveJob` | `/api/recruiter/jobs/{id}` | DELETE | Bearer (Recruiter) | **Matched** | Soft deletes job |
| `api.deleteJob` | `/api/recruiter/jobs/{id}/delete` | DELETE | Bearer (Recruiter) | **Matched** | Hard deletes job |
| `api.getRecruiterStats` | `/api/recruiter/stats` | GET | Bearer (Recruiter) | **Matched** | Unit tests fail due to mock bug |

---

# Links / Routes / Direct References

1. **`frontend/assets/js/firebase-init.js:3` → `../../firebase-config.js?v=5`**: File is git-ignored and missing in fresh clones (AUDIT-004).
2. **`notebooks/evaluation.ipynb:146` → `from services.skill_expander import get_related_skills`**: Invalid module path; should be `backend.services.skill_expander`.
3. **`README.md:10` → `https://ai-resume-screener-69d23.web.app/`**: Discrepant from active `nipun-platform` Firebase configuration.
4. **`README.md:144` → `alembic upgrade head`**: Fails on fresh clones because `alembic/` is git-ignored (AUDIT-003).
5. **`README.md:150` → `python scratch/migrate_to_supabase.py`**: Fails on fresh clones because `scratch/` is git-ignored.
6. **`frontend/recruiter.html:275`, `candidate.html:357`, `onboarding.html:174` → `assets/js/landing.js`**: Unnecessary script reference on authenticated pages.

---

# Unwanted / Suspicious Files

| Path | Type | Reason | Confidence | Recommendation |
|---|---|---|---|---|
| `backend/services/pipeline.py` | Redundant / Dead Code | 42KB monolith shadowed by `pipeline/` package | Confirmed | Merge any unique code into `pipeline/` and delete |
| `backend/services/skill_expander.py` | Dead Code | Unused in backend; only referenced in notebook | Confirmed | Integrate into `semantic/` or delete |
| `benchmark3.py` | Deleted Tracked File | Tracked in git index but deleted locally | Confirmed | Run `git rm benchmark3.py` |
| `commit_message.txt` | Deleted Tracked File | Tracked in git index but deleted locally | Confirmed | Run `git rm commit_message.txt` |
| `dummy.js` | Deleted Tracked File | Tracked in git index but deleted locally | Confirmed | Run `git rm dummy.js` |
| `pr_description.md` | Deleted Tracked File | Tracked in git index but deleted locally | Confirmed | Run `git rm pr_description.md` |
| `pre_commit.js` | Deleted Tracked File | Tracked in git index but deleted locally | Confirmed | Run `git rm pre_commit.js` |
| `submission_description.txt` | Deleted Tracked File | Tracked in git index but deleted locally | Confirmed | Run `git rm submission_description.txt` |
| `.firebase/hosting.ZnJvbnRlbmQ.cache` | Committed Cache | Build/hosting cache committed to git | Confirmed | Remove from git and add to `.gitignore` |
| `graphify-out/` | Committed Artifacts | ~1.75MB of generated HTML/JSON visualization graphs | Confirmed | Remove from git and add to `.gitignore` |
| `scratch/` (22 files) | Dev Artifacts | Screenshots (~5.5MB) and scratch scripts | Confirmed | Keep git-ignored; clean up locally |
| `.codegraph/codegraph.db` | Local Database | 2.46MB code graph database | Confirmed | Keep git-ignored |
| `tests/test_recruiter.py` | Fragmented Test | 1 broken test duplicate of `backend/tests/test_recruiter.py` | Confirmed | Consolidate into `backend/tests/` |

---

# Missing / Unimplemented Functionality

1. **Pipeline Stages 5, 6, 7 Execution in `orchestrator.py`:** Truncated after Stage 4.
2. **Recruiter Candidate Retrieval Endpoints:** No API exists to query candidates evaluated for a job description.
3. **Password Reset / Recovery:** No password reset or email verification endpoints exist.
4. **Email Notifications:** `aiosmtplib` and email credentials exist in configuration, but no email dispatching service is implemented.
5. **Table Parsing in Word Resumes:** `document_service.py` omits table contents from DOCX files.
6. **Recruiter Policy Rules:** `backend/services/policy/recruiter_policy.py` is an empty `pass` class.

---

# Test Results

### Test Suite Execution Summary
- **Command 1:** `.\venv\Scripts\python -m pytest`
  - **Result:** Failed during collection (1 error in `conftest.py`, 1 test collected)
  - **Root Cause:** `RuntimeError: The starlette.testclient module requires the httpx package to be installed.`
- **Command 2:** `.\venv\Scripts\python -m pytest tests/test_recruiter.py`
  - **Result:** 1 collected, 1 FAILED
  - **Error:** `AssertionError: assert <MagicMock ...> == 0` (mocking `.all()` instead of `.first()`)
- **Command 3:** `.\venv\Scripts\python -m pytest backend/tests/test_recruiter.py --noconftest`
  - **Result:** 3 collected, 2 PASSED, 1 FAILED
  - **Passed:** `test_create_job_description_success`, `test_create_job_description_minimal`
  - **Failed:** `test_get_recruiter_stats_malformed_experience` (`TypeError: 'MagicMock' object is not subscriptable`)
- **Command 4:** `.\venv\Scripts\python -m pytest backend/tests/services/xai/test_evidence.py --noconftest`
  - **Result:** 5 PASSED
- **Command 5:** `.\venv\Scripts\python -m pytest backend/tests/test_info_extractor.py backend/tests/services/test_info_extractor.py backend/tests/services/xai/test_formatter.py --noconftest`
  - **Result:** 19 PASSED
- **Command 6:** `.\venv\Scripts\python -m pytest backend/tests/services/recommendations/test_estimator.py --noconftest`
  - **Result:** Failed import collection (`ModuleNotFoundError: No module named 'httpx'`)
- **Warnings:** `PyPDF2 is deprecated. Please move to the pypdf library instead.` (emitted across test runs).

---

# Documentation Consistency

1. **Tailwind Version:** `README.md` documents "compiled Tailwind v4 CSS", but `package.json` installs `"tailwindcss": "^3.4.17"` (v3).
2. **Missing Setup Directories:** `README.md` instructs running `alembic upgrade head` and `python scratch/migrate_to_supabase.py`, but both `alembic/` and `scratch/` are ignored in `.gitignore`.
3. **Pipeline Stages:** `README.md` describes a 6-stage pipeline and a "Multi-Agent Analysis" stage. The codebase implements an 8-stage pipeline (`stages.py`) without any multi-agent layer.
4. **Firebase Hosting URL:** `README.md` lists `https://ai-resume-screener-69d23.web.app/`, while current Firebase config specifies `nipun-platform`.
5. **Pipeline Path:** `README.md` points to `backend/services/pipeline.py`, whereas active code uses `backend/services/pipeline/`.

---

# End-to-End Flow Results

## Candidate Flow
- **Signup / Login:** Works as expected. User created in database, password hashed with bcrypt, JWT issued.
- **Onboarding:** User submits status, field of study, domain. Profile updated, `profile_completed` set to `True`. Role set in DB, but JWT token is not refreshed.
- **Resume Upload (`/api/candidate/process`):** **BROKEN**.
  - Document text extracted from PDF/DOCX.
  - Passes to `screen_resumes` → invokes `pipeline.run_analysis`.
  - `orchestrator.py` halts after Stage 4, returning `None`.
  - Crashes with `AttributeError: 'NoneType' object has no attribute 'status'`.
- **Dashboard & History (`/api/candidate/resumes`):** Works if data exists, but timeline comparison falls back to defaults because `analysis_metadata` is omitted from the response.
- **Recommendation Status Update:** Works as expected with `flag_modified` on JSON field.

## Recruiter Flow
- **Signup / Login:** Works as expected.
- **Onboarding:** Recruiter profile created with company details.
- **Job Library (`/api/recruiter/jobs`):** Full CRUD works as expected (create, read, update, archive, permanent delete).
- **Resume Screening (`/api/recruiter/process`):** **BROKEN**.
  - Invokes `screen_resumes` → crashes due to pipeline truncation (AUDIT-001).
- **Recruiter Dashboard (`/api/recruiter/stats`):** Aggregates computed from database records. Works at runtime when database has valid records, but unit tests fail due to mock issues.
- **Candidate Inspection:** **BROKEN / MISSING**. No endpoint exists to view candidate lists or evaluation cards after the screening response is lost.

---

# Dependency & Configuration Findings

1. **Missing from venv:** `httpx` is in `requirements.txt` but not installed in the environment.
2. **Unused in backend:** `pandas`, `numpy`, `jinja2`, `aiosmtplib`, `passlib[bcrypt]`.
3. **Unused in frontend:** `cors` npm package.
4. **Missing from `.env.example`:** `ALLOWED_ORIGINS`, `MAX_FILE_SIZE`, `RATE_LIMIT`, `LOG_LEVEL`, `GEMINI_API_KEY`, `OPENAI_API_KEY`.
5. **Project ID Mismatch:** `config.py` defaults to `ai-resume-screener-69d23`, but `.env` and `firebase-config.js` use `nipun-platform`.

---

# Recommended Fix Order

1. **CRITICAL — AUDIT-001 — Restore Pipeline Execution in `orchestrator.py`:** Add Stages 5, 6, 7 and `return context.event` to `AnalysisPipeline.run_analysis`.
2. **CRITICAL — AUDIT-002 — Install `httpx` & Make Imports Safe:** Install `httpx` in virtual environment and ensure recommendation imports handle missing keys gracefully.
3. **CRITICAL — AUDIT-003 — Track Database Migrations:** Remove `alembic` from `.gitignore` and commit `alembic/` to git.
4. **CRITICAL — AUDIT-004 — Fix Frontend Config Distribution:** Commit an example config or remove `frontend/firebase-config.js` from `.gitignore`.
5. **CRITICAL — AUDIT-005 — Rotate and Protect Credentials:** Rotate Supabase DB password, revoke Google app password, regenerate JWT secret, and scrub secrets.
6. **HIGH — AUDIT-007 — Configure CORS Allowed Origins:** Add default origins in `backend/config.py` and document in `.env.example`.
7. **HIGH — AUDIT-006 — Fix Education Extraction Regex:** Require periods/context for `M.E.` and `B.E.` to prevent matching "me" and "be".
8. **HIGH — AUDIT-008 — Implement Recruiter Candidate Endpoints:** Add `GET /api/recruiter/jobs/{id}/candidates` to allow viewing past screening results.
9. **HIGH — AUDIT-013 — Preserve Full Candidate Skills in Metadata:** Pass all extracted candidate skills to `metadata_builder.py`.
10. **HIGH — AUDIT-011 — Return Metadata in Candidate Resumes API:** Add `analysis_metadata` fields to `GET /api/candidate/resumes`.
11. **HIGH — AUDIT-012 — Correct `.doc` File Handling:** Disallow `.doc` or integrate a binary Word parser.
12. **HIGH — AUDIT-009 & AUDIT-010 — Fix Unit Tests:** Update database mocks in `test_recruiter.py` and remove mock calls on `db_session` in `test_auth.py`.
13. **MEDIUM — AUDIT-014 — Decommission Shadowed `pipeline.py`:** Delete obsolete monolith `backend/services/pipeline.py`.
14. **MEDIUM — AUDIT-016 — Eliminate Duplicate Scoring Logic:** Unify scoring formulas between `stages.py` and `scoring_service.py`.

---

# Files Requiring Manual Review

1. `backend/services/pipeline.py`: Must be compared line-by-line with `backend/services/pipeline/stages.py` and `orchestrator.py` before deletion.
2. `backend/services/skill_expander.py`: Review whether the concept expansions and alias tables should be merged into `backend/services/skills/` and `backend/services/semantic/`.
3. `backend/routers/auth.py` (`fetch_google_certs`): Review timeout and error handling when Google's metadata endpoint is unreachable.
4. `scratch/migrate_to_supabase.py`: Review if migration logic needs to be promoted to an Alembic data migration or retained as an administrative tool.

---

# Audit Limitations

1. **Missing `httpx` in Virtual Environment:** Prevented running tests requiring `fastapi.testclient.TestClient` (`test_auth.py`, `routers/test_auth.py`) and recommendation estimator tests.
2. **Live Third-Party API Calls:** Google Gemini API and OpenAI API keys were not configured; live LLM enhancement calls could not be verified end-to-end against live external endpoints.
3. **Read-Only Constraint:** Per instructions, no files were modified, dependencies were not installed, and tests requiring changes were not altered.
4. **Live Supabase Egress:** Direct port 5432 database connection was established and verified for schema drift and migrations, but live write operations were avoided to prevent state mutation.

---

# Final Assessment

- **Correctness:** **Deficient in Core Flows**. The application cannot complete resume screening end-to-end due to pipeline truncation in `orchestrator.py` (AUDIT-001) and missing `httpx` (AUDIT-002). Education extraction is fundamentally skewed by regex boundary bugs (AUDIT-006).
- **Security:** **High Risk**. Plaintext production credentials (Supabase DB, Google App Password, JWT Secret) are stored in `.env`. CORS is blocked by default (AUDIT-007).
- **Reliability:** **Moderate to Low**. Missing migrations in version control (AUDIT-003) and missing frontend config (AUDIT-004) ensure that fresh clones will fail to run. Top-level synchronous database connections (AUDIT-020) cause startup blocking.
- **Maintainability:** **Fair, with Architectural Drift**. Well-architected modular packages (`services/pipeline/`, `services/skills/`, `services/semantic/`, `services/xai/`) are compromised by obsolete duplicate files (`pipeline.py`, `skill_expander.py`) and duplicated scoring logic.
- **Frontend/Backend Integration:** **Good Structure, Contract Gaps**. Routes generally align, but candidate timeline comparison is missing backend data (AUDIT-011), and recruiter candidate history viewing is missing entirely (AUDIT-008).
- **Database Integrity:** **Good**. Schema models and Alembic migrations match the live Supabase PostgreSQL database cleanly, with proper foreign keys and cascade deletion.
- **Test Coverage:** **Low and Failing**. Several existing tests fail due to mock bugs (AUDIT-009, AUDIT-010), and the suite cannot run under default pytest without `--noconftest` due to missing `httpx`.
