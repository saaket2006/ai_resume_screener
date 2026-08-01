# Graph Report - .  (2026-08-01)

## Corpus Check
- 99 files · ~69,562 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 778 nodes · 1768 edges · 53 communities (51 shown, 2 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 220 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Resume Analysis Pipeline
- Semantic Matching & Scoring
- Recommendation Engine
- XAI Explanation Engine
- GSAP Animation Library
- Auth & Recruiter API
- ScrollTrigger Library
- Database & Core Models
- Frontend App & Components
- Frontend Auth & Onboarding
- Frontend API Client
- Frontend UI Components
- Candidate Router
- GSAP Core Internals
- Enums & Auth Schemas
- GSAP Timeline & Tween
- Backend Entry & Config
- Package Config & Deps
- Auth Utils & Config
- Recruiter UI Components
- Router & State Management
- ScrollTrigger Internals
- GSAP Easing Internals
- ScrollTrigger More Internals
- GSAP Animation Internals
- ScrollTrigger More Internals 2
- Landing Page Animations
- Legacy Resume Processing
- Document Service
- GSAP Context Internals
- ScrollTrigger More Internals 3
- Skill Expander
- ScrollTrigger Minimal
- Loading Overlay
- GSAP/ScrollTrigger Bridge
- ScrollTrigger More Internals 4
- Auth Me Endpoint
- Onboarding Status Endpoint
- Skill Validator
- GSAP/ScrollTrigger Minimal

## God Nodes (most connected - your core abstractions)
1. `User` - 37 edges
2. `ResumeStatus` - 34 edges
3. `Resume` - 31 edges
4. `ScanResult` - 31 edges
5. `ScoringProfile` - 29 edges
6. `XaiEngine` - 27 edges
7. `UserRole` - 26 edges
8. `request()` - 26 edges
9. `SemanticMatcher` - 25 edges
10. `SemanticScorer` - 25 edges

## Surprising Connections (you probably didn't know these)
- `CandidateProfile` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py
- `JobDescription` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py
- `RecruiterProfile` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py
- `Resume` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py
- `ScanResult` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py

## Import Cycles
- None detected.

## Communities (53 total, 2 thin omitted)

### Community 0 - "Resume Analysis Pipeline"
Cohesion: 0.07
Nodes (68): ResumeStatus, Resume, ScanResult, ScoringProfile, extract_education(), extract_email(), extract_experience(), extract_github() (+60 more)

### Community 1 - "Semantic Matching & Scoring"
Cohesion: 0.06
Nodes (38): preprocess_text(), Cleans text by: - Lowercasing - Removing punctuation - Removing stopwords -…, rank_candidates(), Ranks resumes against a job description using TF-IDF and Cosine Similarity. To…, Session, Core business logic to screen and rank candidate resumes against a job…, screen_resumes(), get_weight() (+30 more)

### Community 2 - "Recommendation Engine"
Cohesion: 0.08
Nodes (30): Defines thresholds and priorities for AI Resume Improvement Engine…, RecommendationPolicy, Defines recruiter-specific configurations and security permissions., RecruiterPolicy, Defines policy configurations for ATS scoring and weights. Removes magic…, ScoringPolicy, Defines policy configurations and fallback weights for adaptive scoring…, ScoringProfilePolicy (+22 more)

### Community 3 - "XAI Explanation Engine"
Cohesion: 0.09
Nodes (37): build_score_components(), Any, Builds the structured ScoreComponent list using the candidate's scored…, _resolve_status(), Any, Helper to construct a dict representation of StructuredExplanations., Generates structured multi-level explanations (SUMMARY, DETAILED, TECHNICAL)…, effective_exp_title() (+29 more)

### Community 4 - "GSAP Animation Library"
Cohesion: 0.06
Nodes (16): ee(), Jd(), Kd(), Ld(), ma(), Md(), na(), Od() (+8 more)

### Community 5 - "Auth & Recruiter API"
Cohesion: 0.11
Nodes (29): Restricts route access to users registered with the RECRUITER role., Restricts route access to users registered with the CANDIDATE role., require_candidate(), require_recruiter(), User, archive_job_description(), create_job_description(), delete_job_description() (+21 more)

### Community 6 - "ScrollTrigger Library"
Cohesion: 0.07
Nodes (4): dc(), Ha(), Ia(), ob()

### Community 7 - "Database & Core Models"
Cohesion: 0.16
Nodes (18): Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), get_db(), FastAPI Dependency to yield a database session., CandidateProfile, JobDescription (+10 more)

### Community 8 - "Frontend App & Components"
Cohesion: 0.16
Nodes (17): login(), clearCandidateState(), handleFiles(), renderFileList(), renderResults(), updateResumeCountDisplay(), uploadedFiles, getCandidateDetailRowHTML() (+9 more)

### Community 9 - "Frontend Auth & Onboarding"
Cohesion: 0.16
Nodes (17): checkAuthStatus(), ROLES, getStepsForRole(), hideObError(), initializeOnboardingPage, initOnboarding(), showObError(), showOnboardingWizard() (+9 more)

### Community 10 - "Frontend API Client"
Cohesion: 0.17
Nodes (22): archiveJob(), createJob(), deleteCandidateResume(), deleteJob(), getCandidateResumeDetails(), getCandidateResumes(), getCandidateStats(), getJobs() (+14 more)

### Community 11 - "Frontend UI Components"
Cohesion: 0.14
Nodes (16): getEmptyStateHTML(), toggleButtonLoading(), initNavbar(), API_BASE, API_ENDPOINTS, CANDIDATE_STATUS_VALUES, COMPANY_TYPES, MESSAGES (+8 more)

### Community 12 - "Candidate Router"
Cohesion: 0.12
Nodes (20): candidate_status(), delete_candidate_resume(), get_candidate_resume_details(), get_candidate_resumes(), get_candidate_stats(), process_candidate_resume(), delete, get (+12 more)

### Community 13 - "GSAP Core Internals"
Cohesion: 0.15
Nodes (20): _a(), ac(), Bo(), db(), ea(), eb(), ga(), gb() (+12 more)

### Community 14 - "Enums & Auth Schemas"
Cohesion: 0.37
Nodes (16): CompanyType, UserRole, CandidateProfileResponse, Config, OnboardingStatusResponse, OnboardingSubmission, BaseModel, RecruiterProfileResponse (+8 more)

### Community 15 - "GSAP Timeline & Tween"
Cohesion: 0.15
Nodes (18): _assertThisInitialized(), Ec(), Fc(), gc(), ka(), qa(), t(), tb() (+10 more)

### Community 16 - "Backend Entry & Config"
Cohesion: 0.14
Nodes (13): api_route, get_current_user(), Session, Validates the JWT token and returns the corresponding User. Raises 401…, setup_logging(), get_profile(), health(), get (+5 more)

### Community 17 - "Package Config & Deps"
Cohesion: 0.12
Nodes (16): autoprefixer, cors, firebase, dependencies, cors, firebase, devDependencies, autoprefixer (+8 more)

### Community 18 - "Auth Utils & Config"
Cohesion: 0.16
Nodes (14): Settings, create_access_token(), get_password_hash(), Verifies a plain text password against the hashed version using bcrypt., Hashes a plain text password using bcrypt., Generates a secure JSON Web Token., verify_password(), login() (+6 more)

### Community 19 - "Recruiter UI Components"
Cohesion: 0.20
Nodes (11): getRecruiterCandidateCardHTML(), populateRecruiterProfileUI(), updateStatisticCard(), initializeRecruiterScreen(), initRecruiterPage(), loadJobDescriptionsDropdown(), loadScoringProfilesDropdown(), recUploadedFiles (+3 more)

### Community 20 - "Router & State Management"
Cohesion: 0.30
Nodes (13): getProfile(), sidebarLinkIds, updateSidebarActiveLink(), initializeCandidateDashboard(), initializeCandidateProfile(), initializeCandidateScreen(), initializeRecruiterDashboard(), initializeRecruiterProfile() (+5 more)

### Community 21 - "ScrollTrigger Internals"
Cohesion: 0.22
Nodes (11): Fa(), Ga(), mb(), oc(), qc(), rc(), Ta(), ub() (+3 more)

### Community 22 - "GSAP Easing Internals"
Cohesion: 0.29
Nodes (10): be(), _d(), fa(), ia(), ie(), je(), ke(), le() (+2 more)

### Community 23 - "ScrollTrigger More Internals"
Cohesion: 0.22
Nodes (10): bf(), cf(), df(), ef(), kf(), lf(), M(), mf() (+2 more)

### Community 24 - "GSAP Animation Internals"
Cohesion: 0.28
Nodes (9): Aa(), Animation(), ha(), ja(), Jc(), Lc(), Ra(), Sa() (+1 more)

### Community 25 - "ScrollTrigger More Internals 2"
Cohesion: 0.22
Nodes (9): Ab(), J(), jc(), kb(), lc(), Ra(), rb(), Sa() (+1 more)

### Community 26 - "Landing Page Animations"
Cohesion: 0.46
Nodes (6): initCounters(), initFeatureStack(), initHeroAnimation(), initNavbarEffects(), initStoryAnimation(), initWalkthrough()

### Community 27 - "Legacy Resume Processing"
Cohesion: 0.29
Nodes (7): legacy_process_resumes(), limit, post, Request, Session, UploadFile, Legacy endpoint delegating to recruiter process_resumes. Requires Recruiter…

### Community 28 - "Document Service"
Cohesion: 0.38
Nodes (6): extract_text(), extract_text_from_docx(), extract_text_from_pdf(), Extract text from a DOCX file., Route to appropriate extractor based on extension., Extract text from a PDF file.

### Community 29 - "GSAP Context Internals"
Cohesion: 0.29
Nodes (7): Ab(), Bb(), cb(), Context(), Ew(), fb(), zb()

### Community 30 - "ScrollTrigger More Internals 3"
Cohesion: 0.53
Nodes (6): Bb(), Ja(), Ka(), La(), Oa(), z()

### Community 31 - "Skill Expander"
Cohesion: 0.40
Nodes (4): get_related_skills(), is_skill_in_text(), Checks if an explicit skill contains a broad conceptual keyword. For example,…, Checks if a skill or any of its known aliases exists in the given text. Handles…

### Community 32 - "ScrollTrigger Minimal"
Cohesion: 0.40
Nodes (5): A(), B(), F(), G(), K()

### Community 33 - "Loading Overlay"
Cohesion: 0.50
Nodes (3): loadingOverlay, STAGES, STATUS_MESSAGES

### Community 34 - "GSAP/ScrollTrigger Bridge"
Cohesion: 0.50
Nodes (4): la(), Q(), Gb(), Hb()

### Community 35 - "ScrollTrigger More Internals 4"
Cohesion: 0.50
Nodes (4): mc(), O(), P(), r()

### Community 44 - "Auth Me Endpoint"
Cohesion: 0.67
Nodes (3): get_me(), get, Retrieves the authenticated user's profile details.

### Community 45 - "Onboarding Status Endpoint"
Cohesion: 0.67
Nodes (3): get_onboarding_status(), get, Returns the user's onboarding completion status and role.

## Knowledge Gaps
- **18 isolated node(s):** `Settings`, `uploadedFiles`, `sidebarLinkIds`, `COMPANY_TYPES`, `CANDIDATE_STATUS_VALUES` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `Auth & Recruiter API` to `Resume Analysis Pipeline`, `Database & Core Models`, `Auth Me Endpoint`, `Candidate Router`, `Enums & Auth Schemas`, `Onboarding Status Endpoint`, `Backend Entry & Config`, `Auth Utils & Config`, `Legacy Resume Processing`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `XaiEngine` connect `Resume Analysis Pipeline` to `XAI Explanation Engine`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `build_resume_recommendations()` connect `Recommendation Engine` to `Resume Analysis Pipeline`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `User` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`User` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ResumeStatus` (e.g. with `CandidateProfile` and `JobDescription`) actually correct?**
  _`ResumeStatus` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Resume` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`Resume` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `ScanResult` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`ScanResult` has 24 INFERRED edges - model-reasoned connections that need verification._