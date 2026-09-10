# Graph Report - ai_resume_screener  (2026-09-10)

## Corpus Check
- 126 files · ~135,698 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 967 nodes · 2274 edges · 68 communities (60 shown, 8 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 290 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e1ab5f59`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- stages.py
- test_estimator.py
- build_score_components
- Skill
- test_remediation.py
- JobDescription
- User
- gsap.min.js
- models/models.py
- seed_default_profiles
- ScrollTrigger.min.js
- auth.py
- login.js
- api.js
- process_candidate_resume
- candidate.js
- s
- recruiter.js
- Tween
- package.json
- router.js
- app.js
- _d
- state.js
- yc
- ja
- jc
- animations.js
- test_user
- cb
- get_profile
- Oa
- bf
- skill_expander.py
- K
- Landing Index HTML
- get_onboarding_status
- loadingOverlay.js
- Q
- r
- process_resumes
- validate_skill_name
- zd
- firebase-config.example.js
- Graphify Agent Rule
- Graphify Workflow Guide
- AI Resume Screener Overview
- Resume Screener Report
- Python Dependencies
- submit_onboarding

## God Nodes (most connected - your core abstractions)
1. `User` - 51 edges
2. `UserRole` - 36 edges
3. `PipelineStage` - 33 edges
4. `AnalysisContext` - 30 edges
5. `PersistenceStage` - 30 edges
6. `request()` - 29 edges
7. `CompanyType` - 28 edges
8. `ScoringProfileResolutionStage` - 26 edges
9. `ResumeStatus` - 25 edges
10. `ResumeTextExtractionStage` - 25 edges

## Surprising Connections (you probably didn't know these)
- `run_optimized()` --calls--> `User`  [EXTRACTED]
  benchmark.py → backend/models/models.py
- `mock_pipeline_ctx()` --calls--> `AnalysisContext`  [EXTRACTED]
  benchmark.py → backend/services/pipeline/context.py
- `run_optimized()` --calls--> `PersistenceStage`  [EXTRACTED]
  benchmark.py → backend/services/pipeline/stages.py
- `CandidateProfile` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py
- `JobDescription` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py

## Import Cycles
- None detected.

## Communities (68 total, 8 thin omitted)

### Community 0 - "stages.py"
Cohesion: 0.10
Nodes (52): ResumeStatus, Resume, ScanResult, ScoringProfile, AnalysisContext, Any, Lightweight, shared context carrying tracing IDs, configurations, and stage…, ExplanationBuiltEvent (+44 more)

### Community 1 - "test_estimator.py"
Cohesion: 0.06
Nodes (47): Defines thresholds and priorities for AI Resume Improvement Engine…, RecommendationPolicy, Defines recruiter-specific configurations and security permissions., RecruiterPolicy, Defines policy configurations for ATS scoring and weights. Removes magic…, ScoringPolicy, Defines policy configurations and fallback weights for adaptive scoring…, ScoringProfilePolicy (+39 more)

### Community 2 - "build_score_components"
Cohesion: 0.07
Nodes (46): build_score_components(), Any, Builds the structured ScoreComponent list using the candidate's scored…, _resolve_status(), Any, Helper to construct a dict representation of StructuredExplanations., Generates structured multi-level explanations (SUMMARY, DETAILED, TECHNICAL)…, effective_exp_title() (+38 more)

### Community 3 - "Skill"
Cohesion: 0.05
Nodes (44): preprocess_text(), Cleans text by: - Lowercasing - Removing punctuation - Removing stopwords -…, _get_tfidf_model(), rank_candidates(), Caches the TF-IDF vectorizer and JD matrix for a given set of JD skills.…, Ranks resumes against a job description using TF-IDF and Cosine Similarity. To…, Session, Core business logic to screen and rank candidate resumes against a job… (+36 more)

### Community 4 - "test_remediation.py"
Cohesion: 0.05
Nodes (58): anyio, extract_text(), extract_text_from_docx(), extract_text_from_pdf(), Extract text from a DOCX file, including paragraphs and tables., Route to appropriate extractor based on extension., Extract text from a PDF file., extract_education() (+50 more)

### Community 5 - "JobDescription"
Cohesion: 0.22
Nodes (11): JobDescription, BaseModel, UpdateRecommendationPayload, create_job_description(), post, Adds a new job description to the recruiter's library., test_create_job_description_minimal(), test_create_job_description_success() (+3 more)

### Community 6 - "User"
Cohesion: 0.16
Nodes (20): Restricts route access to users registered with the RECRUITER role., require_recruiter(), User, archive_job_description(), delete_job_description(), get_recruiter_stats(), get_scoring_profiles(), list_job_descriptions() (+12 more)

### Community 7 - "gsap.min.js"
Cohesion: 0.06
Nodes (16): ee(), Jd(), Kd(), Ld(), ma(), Md(), na(), Od() (+8 more)

### Community 8 - "models/models.py"
Cohesion: 0.14
Nodes (18): Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), api_route, Settings, get_db(), FastAPI Dependency to yield a database session. (+10 more)

### Community 9 - "seed_default_profiles"
Cohesion: 0.22
Nodes (8): check_db_connection(), Tests connection to the configured database on demand (e.g. startup or health…, Startup event handler: verify database connectivity and seed default profiles., startup_event(), Session, Checks if scoring profiles exist in the database; if not, seeds missing default…, seed_default_profiles(), on_event

### Community 10 - "ScrollTrigger.min.js"
Cohesion: 0.07
Nodes (4): dc(), Ha(), Ia(), ob()

### Community 11 - "auth.py"
Cohesion: 0.05
Nodes (81): create_access_token(), get_password_hash(), Verifies a plain text password against the hashed version using bcrypt., Hashes a plain text password using bcrypt., Generates a secure JSON Web Token., verify_password(), CompanyType, UserRole (+73 more)

### Community 12 - "login.js"
Cohesion: 0.22
Nodes (10): MESSAGES, app, auth, googleProvider, initializeLoginPage(), initializeSignupPage(), initSignupPage(), sanitizeUrl() (+2 more)

### Community 13 - "api.js"
Cohesion: 0.15
Nodes (27): archiveJob(), createJob(), deleteCandidateResume(), deleteJob(), forgotPassword(), getCandidateResumeDetails(), getCandidateResumes(), getCandidateStats() (+19 more)

### Community 14 - "process_candidate_resume"
Cohesion: 0.12
Nodes (22): candidate_status(), delete_candidate_resume(), get_candidate_resume_details(), get_candidate_resumes(), get_candidate_stats(), process_candidate_resume(), delete, get (+14 more)

### Community 15 - "candidate.js"
Cohesion: 0.14
Nodes (15): getEmptyStateHTML(), toggleButtonLoading(), initNavbar(), API_BASE, API_ENDPOINTS, CANDIDATE_STATUS_VALUES, COMPANY_TYPES, ROUTES (+7 more)

### Community 16 - "s"
Cohesion: 0.15
Nodes (20): _a(), ac(), Bo(), db(), ea(), eb(), ga(), gb() (+12 more)

### Community 17 - "recruiter.js"
Cohesion: 0.20
Nodes (11): populateRecruiterProfileUI(), updateStatisticCard(), clearRecruiterWorkspaceState(), initializeRecruiterScreen(), initRecruiterPage(), loadJobDescriptionsDropdown(), loadScoringProfilesDropdown(), recUploadedFiles (+3 more)

### Community 18 - "Tween"
Cohesion: 0.15
Nodes (18): _assertThisInitialized(), Ec(), Fc(), gc(), ka(), qa(), t(), tb() (+10 more)

### Community 19 - "package.json"
Cohesion: 0.12
Nodes (15): autoprefixer, cors, firebase, dependencies, cors, firebase, devDependencies, autoprefixer (+7 more)

### Community 20 - "router.js"
Cohesion: 0.22
Nodes (18): getProfile(), sidebarLinkIds, updateSidebarActiveLink(), initializeCandidateDashboard(), initializeCandidateProfile(), initializeCandidateScreen(), resetAuthModalToTabs(), showForgotPasswordView() (+10 more)

### Community 21 - "app.js"
Cohesion: 0.26
Nodes (11): clearCandidateState(), handleFiles(), renderFileList(), renderResults(), updateResumeCountDisplay(), uploadedFiles, getCandidateDetailRowHTML(), getCandidateRowHTML() (+3 more)

### Community 22 - "_d"
Cohesion: 0.29
Nodes (10): be(), _d(), fa(), ia(), ie(), je(), ke(), le() (+2 more)

### Community 23 - "state.js"
Cohesion: 0.15
Nodes (17): checkAuthStatus(), ROLES, getStepsForRole(), hideObError(), initializeOnboardingPage, initOnboarding(), showObError(), showOnboardingWizard() (+9 more)

### Community 24 - "yc"
Cohesion: 0.22
Nodes (11): Fa(), Ga(), mb(), oc(), qc(), rc(), Ta(), ub() (+3 more)

### Community 25 - "ja"
Cohesion: 0.28
Nodes (9): Aa(), Animation(), ha(), ja(), Jc(), Lc(), Ra(), Sa() (+1 more)

### Community 26 - "jc"
Cohesion: 0.22
Nodes (9): Ab(), J(), jc(), kb(), lc(), Ra(), rb(), Sa() (+1 more)

### Community 27 - "animations.js"
Cohesion: 0.46
Nodes (6): initCounters(), initFeatureStack(), initHeroAnimation(), initNavbarEffects(), initStoryAnimation(), initWalkthrough()

### Community 28 - "test_user"
Cohesion: 0.25
Nodes (8): anyio_backend(), client(), db_session(), fixture, Create a new database session for a test., Create a test client using the test database., Creates a test user in the database., test_user()

### Community 29 - "cb"
Cohesion: 0.29
Nodes (7): Ab(), Bb(), cb(), Context(), Ew(), fb(), zb()

### Community 30 - "get_profile"
Cohesion: 0.50
Nodes (4): get_profile(), get, Retrieves the full profile details of the authenticated user., read_root()

### Community 31 - "Oa"
Cohesion: 0.53
Nodes (6): Bb(), Ja(), Ka(), La(), Oa(), z()

### Community 32 - "bf"
Cohesion: 0.22
Nodes (10): bf(), cf(), df(), ef(), kf(), lf(), M(), mf() (+2 more)

### Community 33 - "skill_expander.py"
Cohesion: 0.40
Nodes (4): get_related_skills(), is_skill_in_text(), Checks if an explicit skill contains a broad conceptual keyword. For example,…, Checks if a skill or any of its known aliases exists in the given text. Handles…

### Community 34 - "K"
Cohesion: 0.40
Nodes (5): A(), B(), F(), G(), K()

### Community 35 - "Landing Index HTML"
Cohesion: 0.40
Nodes (5): Nipun Main Branding Image, Candidate Portal HTML, Landing Index HTML, Onboarding Portal HTML, Recruiter Dashboard HTML

### Community 36 - "get_onboarding_status"
Cohesion: 0.67
Nodes (3): get_onboarding_status(), get, Returns the user's onboarding completion status and role.

### Community 37 - "loadingOverlay.js"
Cohesion: 0.50
Nodes (3): loadingOverlay, STAGES, STATUS_MESSAGES

### Community 38 - "Q"
Cohesion: 0.50
Nodes (4): la(), Q(), Gb(), Hb()

### Community 39 - "r"
Cohesion: 0.50
Nodes (4): mc(), O(), P(), r()

### Community 48 - "process_resumes"
Cohesion: 0.17
Nodes (12): legacy_process_resumes(), limit, post, Request, Session, UploadFile, Legacy endpoint delegating to recruiter process_resumes. Requires Recruiter…, process_resumes() (+4 more)

### Community 66 - "submit_onboarding"
Cohesion: 0.50
Nodes (4): post, Session, Creates a user profile based on the role and marks onboarding as completed., submit_onboarding()

## Knowledge Gaps
- **28 isolated node(s):** `Settings`, `uploadedFiles`, `sidebarLinkIds`, `COMPANY_TYPES`, `CANDIDATE_STATUS_VALUES` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `s()` connect `s` to `bf`, `gsap.min.js`, `Tween`, `app.js`, `cb`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `stages.py`, `submit_onboarding`, `get_onboarding_status`, `JobDescription`, `models/models.py`, `auth.py`, `process_candidate_resume`, `process_resumes`, `test_user`, `get_profile`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `XaiEngine` connect `stages.py` to `build_score_components`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `User` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`User` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `UserRole` (e.g. with `CandidateProfile` and `JobDescription`) actually correct?**
  _`UserRole` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `PipelineStage` (e.g. with `AnalysisPipeline` and `ResumeStatus`) actually correct?**
  _`PipelineStage` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `AnalysisContext` (e.g. with `AnalysisPipeline` and `ExplanationBuildingStage`) actually correct?**
  _`AnalysisContext` has 11 INFERRED edges - model-reasoned connections that need verification._