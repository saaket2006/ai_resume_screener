# Graph Report - .  (2026-08-01)

## Corpus Check
- 100 files · ~69,707 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 814 nodes · 1818 edges · 72 communities (52 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 258 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Resume Data Models & Pipeline
- NLP, Scoring & Semantic Matching
- Policy Engine & Recommendations
- Explainable AI (XAI) System
- GSAP Animation Library (Core)
- Frontend UI Components & Pages
- ScrollTrigger Library
- Frontend API Layer
- Auth, Database & Onboarding
- Core Backend Config & Routers
- Recruiter API Endpoints
- Frontend Auth & State Management
- Candidate API Endpoints
- Data Models & Pydantic Schemas
- GSAP Animation Library (Utils)
- Frontend Constants & Onboarding
- GSAP Animation Library (Timeline)
- Frontend Components & Candidate Pages
- Documentation & Project Concepts
- Auth Utilities & Login/Signup
- Frontend App & Modal Components
- Package.json Dependencies
- ScrollTrigger Library (Core)
- GSAP Animation Library (Easing)
- ScrollTrigger Library (Utils)
- GSAP Animation Library (Animation)
- ScrollTrigger Library (Observers)
- Frontend Animations & Landing
- Legacy Resume Processing Endpoints
- Document Processing Service
- GSAP Animation Library (Context)
- ScrollTrigger Library (Config)
- Skill Expansion Service
- ScrollTrigger Library (Minimal)
- ScrollTrigger Library (Minimal 2)
- Main App Entry Points
- Loading Overlay Component
- GSAP/ScrollTrigger Shared
- GSAP Animation Library (Minimal)
- Skill Validation Service
- MCP Server Config
- GSAP/ScrollTrigger Shared Minimal
- Dependency: aiosmtplib
- Dependency: gunicorn
- Dependency: spaCy Model
- Dependency: jinja2
- Dependency: numpy
- Dependency: pandas
- Dependency: passlib
- Dependency: psycopg2
- Dependency: pydantic-email
- Dependency: pyjwt
- Dependency: pypdf2
- Dependency: pytest
- Dependency: python-docx
- Dependency: python-dotenv
- Dependency: python-multipart
- Dependency: scikit-learn
- Dependency: slowapi

## God Nodes (most connected - your core abstractions)
1. `User` - 38 edges
2. `ResumeStatus` - 34 edges
3. `Resume` - 31 edges
4. `ScanResult` - 31 edges
5. `ScoringProfile` - 29 edges
6. `UserRole` - 27 edges
7. `XaiEngine` - 27 edges
8. `request()` - 27 edges
9. `SemanticMatcher` - 25 edges
10. `SemanticScorer` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Candidate Dashboard` --conceptually_related_to--> `Resume Screening`  [INFERRED]
  frontend/index.html → README.md
- `Recruiter Portal` --conceptually_related_to--> `Resume Screening`  [INFERRED]
  frontend/index.html → README.md
- `spacy` --implements--> `Skill Extraction`  [INFERRED]
  requirements.txt → README.md
- `spacy` --implements--> `Semantic Matching`  [INFERRED]
  requirements.txt → README.md
- `alembic` --implements--> `FastAPI`  [INFERRED]
  requirements.txt → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Core Backend Stack** — readme_fastapi, readme_postgresql, requirements_fastapi, requirements_sqlalchemy, requirements_alembic [INFERRED 0.75]
- **Core Frontend Stack** — readme_react, frontend_index_html_resume_screener_ui [INFERRED 0.75]
- **AI/ML Stack** — readme_semantic_matching, readme_skill_extraction, requirements_spacy [INFERRED 0.75]

## Communities (72 total, 20 thin omitted)

### Community 0 - "Resume Data Models & Pipeline"
Cohesion: 0.06
Nodes (70): ResumeStatus, Resume, ScanResult, ScoringProfile, BaseModel, UpdateRecommendationPayload, extract_education(), extract_email() (+62 more)

### Community 1 - "NLP, Scoring & Semantic Matching"
Cohesion: 0.06
Nodes (38): preprocess_text(), Cleans text by: - Lowercasing - Removing punctuation - Removing stopwords -…, rank_candidates(), Ranks resumes against a job description using TF-IDF and Cosine Similarity. To…, Session, Core business logic to screen and rank candidate resumes against a job…, screen_resumes(), get_weight() (+30 more)

### Community 2 - "Policy Engine & Recommendations"
Cohesion: 0.08
Nodes (30): Defines thresholds and priorities for AI Resume Improvement Engine…, RecommendationPolicy, Defines recruiter-specific configurations and security permissions., RecruiterPolicy, Defines policy configurations for ATS scoring and weights. Removes magic…, ScoringPolicy, Defines policy configurations and fallback weights for adaptive scoring…, ScoringProfilePolicy (+22 more)

### Community 3 - "Explainable AI (XAI) System"
Cohesion: 0.09
Nodes (37): build_score_components(), Any, Builds the structured ScoreComponent list using the candidate's scored…, _resolve_status(), Any, Helper to construct a dict representation of StructuredExplanations., Generates structured multi-level explanations (SUMMARY, DETAILED, TECHNICAL)…, effective_exp_title() (+29 more)

### Community 4 - "GSAP Animation Library (Core)"
Cohesion: 0.06
Nodes (12): ee(), Jd(), Kd(), Ld(), ma(), Md(), na(), Od() (+4 more)

### Community 5 - "Frontend UI Components & Pages"
Cohesion: 0.13
Nodes (22): getProfile(), getRecruiterCandidateCardHTML(), populateRecruiterProfileUI(), sidebarLinkIds, updateSidebarActiveLink(), updateStatisticCard(), initializeCandidateProfile(), initializeCandidateScreen() (+14 more)

### Community 6 - "ScrollTrigger Library"
Cohesion: 0.07
Nodes (4): dc(), Ha(), Ia(), ob()

### Community 7 - "Frontend API Layer"
Cohesion: 0.16
Nodes (25): archiveJob(), createJob(), deleteCandidateResume(), deleteJob(), getCandidateResumeDetails(), getCandidateResumes(), getCandidateStats(), getJobs() (+17 more)

### Community 8 - "Auth, Database & Onboarding"
Cohesion: 0.12
Nodes (23): Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_current_user(), Session, Validates the JWT token and returns the corresponding User. Raises 401…, CandidateProfile (+15 more)

### Community 9 - "Core Backend Config & Routers"
Cohesion: 0.16
Nodes (14): api_route, Settings, get_db(), FastAPI Dependency to yield a database session., Restricts route access to users registered with the RECRUITER role., Restricts route access to users registered with the CANDIDATE role., require_candidate(), require_recruiter() (+6 more)

### Community 10 - "Recruiter API Endpoints"
Cohesion: 0.10
Nodes (24): archive_job_description(), create_job_description(), delete_job_description(), get_recruiter_stats(), get_scoring_profiles(), list_job_descriptions(), process_resumes(), delete (+16 more)

### Community 11 - "Frontend Auth & State Management"
Cohesion: 0.17
Nodes (13): login(), checkAuthStatus(), initLoginPage(), initSignupPage(), clearState(), getToken(), getUser(), setOnboardingStatus() (+5 more)

### Community 12 - "Candidate API Endpoints"
Cohesion: 0.12
Nodes (22): candidate_status(), delete_candidate_resume(), get_candidate_resume_details(), get_candidate_resumes(), get_candidate_stats(), process_candidate_resume(), delete, get (+14 more)

### Community 13 - "Data Models & Pydantic Schemas"
Cohesion: 0.35
Nodes (17): CompanyType, UserRole, CandidateProfileCreate, CandidateProfileResponse, Config, OnboardingStatusResponse, BaseModel, RecruiterProfileCreate (+9 more)

### Community 14 - "GSAP Animation Library (Utils)"
Cohesion: 0.15
Nodes (20): _a(), ac(), Bo(), db(), ea(), eb(), ga(), gb() (+12 more)

### Community 15 - "Frontend Constants & Onboarding"
Cohesion: 0.20
Nodes (16): API_BASE, API_ENDPOINTS, CANDIDATE_STATUS_VALUES, COMPANY_TYPES, MESSAGES, ROLES, ROUTES, getStepsForRole() (+8 more)

### Community 16 - "GSAP Animation Library (Timeline)"
Cohesion: 0.15
Nodes (17): _assertThisInitialized(), Ec(), Fc(), gc(), ka(), qa(), t(), tb() (+9 more)

### Community 17 - "Frontend Components & Candidate Pages"
Cohesion: 0.22
Nodes (10): getEmptyStateHTML(), toggleButtonLoading(), initNavbar(), clearCandidateWorkspaceState(), initCandidatePage(), initializeCandidateDashboard(), renderCandidateAnalysisResults(), renderFileList() (+2 more)

### Community 18 - "Documentation & Project Concepts"
Cohesion: 0.31
Nodes (16): Candidate Dashboard, Recruiter Portal, Resume Screener UI, AI Resume Screener, FastAPI, PostgreSQL, React Frontend, Resume Screening (+8 more)

### Community 19 - "Auth Utilities & Login/Signup"
Cohesion: 0.19
Nodes (13): create_access_token(), get_password_hash(), Verifies a plain text password against the hashed version using bcrypt., Hashes a plain text password using bcrypt., Generates a secure JSON Web Token., verify_password(), login(), post (+5 more)

### Community 20 - "Frontend App & Modal Components"
Cohesion: 0.23
Nodes (11): clearCandidateState(), handleFiles(), renderFileList(), renderResults(), updateResumeCountDisplay(), uploadedFiles, getCandidateDetailRowHTML(), getCandidateRowHTML() (+3 more)

### Community 21 - "Package.json Dependencies"
Cohesion: 0.15
Nodes (12): cors, firebase, dependencies, cors, firebase, devDependencies, tailwindcss, @tailwindcss/cli (+4 more)

### Community 22 - "ScrollTrigger Library (Core)"
Cohesion: 0.22
Nodes (11): Fa(), Ga(), mb(), oc(), qc(), rc(), Ta(), ub() (+3 more)

### Community 23 - "GSAP Animation Library (Easing)"
Cohesion: 0.29
Nodes (10): be(), _d(), fa(), ia(), ie(), je(), ke(), le() (+2 more)

### Community 24 - "ScrollTrigger Library (Utils)"
Cohesion: 0.22
Nodes (10): bf(), cf(), df(), ef(), kf(), lf(), M(), mf() (+2 more)

### Community 25 - "GSAP Animation Library (Animation)"
Cohesion: 0.28
Nodes (9): Aa(), Animation(), ha(), ja(), Jc(), Lc(), Ra(), Sa() (+1 more)

### Community 26 - "ScrollTrigger Library (Observers)"
Cohesion: 0.22
Nodes (9): Ab(), J(), jc(), kb(), lc(), Ra(), rb(), Sa() (+1 more)

### Community 27 - "Frontend Animations & Landing"
Cohesion: 0.46
Nodes (6): initCounters(), initFeatureStack(), initHeroAnimation(), initNavbarEffects(), initStoryAnimation(), initWalkthrough()

### Community 28 - "Legacy Resume Processing Endpoints"
Cohesion: 0.29
Nodes (7): legacy_process_resumes(), limit, post, Request, Session, UploadFile, Legacy endpoint delegating to recruiter process_resumes. Requires Recruiter…

### Community 29 - "Document Processing Service"
Cohesion: 0.38
Nodes (6): extract_text(), extract_text_from_docx(), extract_text_from_pdf(), Extract text from a DOCX file., Route to appropriate extractor based on extension., Extract text from a PDF file.

### Community 30 - "GSAP Animation Library (Context)"
Cohesion: 0.29
Nodes (7): Ab(), Bb(), cb(), Context(), Ew(), fb(), zb()

### Community 31 - "ScrollTrigger Library (Config)"
Cohesion: 0.53
Nodes (6): Bb(), Ja(), Ka(), La(), Oa(), z()

### Community 32 - "Skill Expansion Service"
Cohesion: 0.40
Nodes (4): get_related_skills(), is_skill_in_text(), Checks if an explicit skill contains a broad conceptual keyword. For example,…, Checks if a skill or any of its known aliases exists in the given text. Handles…

### Community 33 - "ScrollTrigger Library (Minimal)"
Cohesion: 0.40
Nodes (5): A(), B(), F(), G(), K()

### Community 34 - "ScrollTrigger Library (Minimal 2)"
Cohesion: 0.40
Nodes (5): mc(), O(), P(), r(), wb()

### Community 35 - "Main App Entry Points"
Cohesion: 0.50
Nodes (4): get_profile(), get, Retrieves the full profile details of the authenticated user., read_root()

### Community 36 - "Loading Overlay Component"
Cohesion: 0.50
Nodes (3): loadingOverlay, STAGES, STATUS_MESSAGES

### Community 37 - "GSAP/ScrollTrigger Shared"
Cohesion: 0.50
Nodes (4): la(), Q(), Gb(), Hb()

### Community 38 - "GSAP Animation Library (Minimal)"
Cohesion: 0.50
Nodes (4): Ud(), vd(), we(), xe()

## Knowledge Gaps
- **41 isolated node(s):** `codegraph`, `Settings`, `uploadedFiles`, `sidebarLinkIds`, `COMPANY_TYPES` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `Auth, Database & Onboarding` to `Resume Data Models & Pipeline`, `Main App Entry Points`, `Core Backend Config & Routers`, `Recruiter API Endpoints`, `Candidate API Endpoints`, `Data Models & Pydantic Schemas`, `Auth Utilities & Login/Signup`, `Legacy Resume Processing Endpoints`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `XaiEngine` connect `Resume Data Models & Pipeline` to `Explainable AI (XAI) System`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `build_resume_recommendations()` connect `Policy Engine & Recommendations` to `Resume Data Models & Pipeline`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `User` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`User` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ResumeStatus` (e.g. with `CandidateProfile` and `JobDescription`) actually correct?**
  _`ResumeStatus` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Resume` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`Resume` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `ScanResult` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`ScanResult` has 24 INFERRED edges - model-reasoned connections that need verification._