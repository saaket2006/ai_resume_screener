# Graph Report - ai_resume_screener  (2026-09-10)

## Corpus Check
- 123 files · ~132,780 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 919 nodes · 2143 edges · 67 communities (59 shown, 8 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 273 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dcf768ae`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- stages.py
- test_estimator.py
- build_score_components
- Skill
- extract_education
- google_login
- JobDescription
- gsap.min.js
- models/models.py
- routers/test_auth.py
- ScrollTrigger.min.js
- UserRole
- state.js
- api.js
- User
- navbar.js
- s
- recruiter.js
- Tween
- package.json
- candidate.js
- app.js
- _d
- onboarding.js
- yc
- ja
- jc
- animations.js
- test_user
- cb
- test_remediation.py
- Oa
- bf
- skill_expander.py
- K
- Landing Index HTML
- env.py
- loadingOverlay.js
- Q
- r
- legacy_process_resumes
- validate_skill_name
- zd
- firebase-config.example.js
- Graphify Agent Rule
- Graphify Workflow Guide
- AI Resume Screener Overview
- Resume Screener Report
- Python Dependencies
- get_onboarding_status

## God Nodes (most connected - your core abstractions)
1. `User` - 49 edges
2. `PipelineStage` - 33 edges
3. `UserRole` - 30 edges
4. `AnalysisContext` - 30 edges
5. `PersistenceStage` - 30 edges
6. `request()` - 27 edges
7. `ScoringProfileResolutionStage` - 26 edges
8. `ResumeTextExtractionStage` - 25 edges
9. `SkillExtractionStage` - 25 edges
10. `SemanticMatchingStage` - 25 edges

## Surprising Connections (you probably didn't know these)
- `run_optimized()` --calls--> `User`  [EXTRACTED]
  benchmark.py → backend/models/models.py
- `test_get_recruiter_stats_empty_scans()` --calls--> `User`  [EXTRACTED]
  tests/test_recruiter.py → backend/models/models.py
- `mock_pipeline_ctx()` --calls--> `AnalysisContext`  [EXTRACTED]
  benchmark.py → backend/services/pipeline/context.py
- `run_optimized()` --calls--> `PersistenceStage`  [EXTRACTED]
  benchmark.py → backend/services/pipeline/stages.py
- `CandidateProfile` --uses--> `UserRole`  [INFERRED]
  backend/models/models.py → backend/models/enums.py

## Import Cycles
- None detected.

## Communities (67 total, 8 thin omitted)

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
Cohesion: 0.08
Nodes (27): get_weight(), Returns the matching weight for the given match type., MatchReason, MatchResult, BaseModel, Universal domain object representing a semantic match between a required skill…, Evaluates relationship type, confidence, and matches between two Skill objects.…, resolve_relationship() (+19 more)

### Community 4 - "extract_education"
Cohesion: 0.08
Nodes (40): extract_education(), extract_email(), extract_experience(), extract_github(), extract_linkedin(), extract_name(), extract_phone(), extract_projects() (+32 more)

### Community 5 - "google_login"
Cohesion: 0.19
Nodes (17): create_access_token(), Generates a secure JSON Web Token., get_me(), google_login(), login(), get, limit, post (+9 more)

### Community 6 - "JobDescription"
Cohesion: 0.08
Nodes (31): JobDescription, archive_job_description(), create_job_description(), delete_job_description(), get_recruiter_stats(), get_scoring_profiles(), list_job_descriptions(), process_resumes() (+23 more)

### Community 7 - "gsap.min.js"
Cohesion: 0.06
Nodes (16): ee(), Jd(), Kd(), Ld(), ma(), Md(), na(), Od() (+8 more)

### Community 8 - "models/models.py"
Cohesion: 0.11
Nodes (23): api_route, Settings, check_db_connection(), get_db(), Tests connection to the configured database on demand (e.g. startup or health…, FastAPI Dependency to yield a database session., get_current_user(), Session (+15 more)

### Community 9 - "routers/test_auth.py"
Cohesion: 0.16
Nodes (10): get_password_hash(), Verifies a plain text password against the hashed version using bcrypt., Hashes a plain text password using bcrypt., verify_password(), fetch_google_certs(), test_fetch_google_certs_error(), test_fetch_google_certs_success(), test_fetch_google_certs_timeout() (+2 more)

### Community 10 - "ScrollTrigger.min.js"
Cohesion: 0.07
Nodes (4): dc(), Ha(), Ia(), ob()

### Community 11 - "UserRole"
Cohesion: 0.33
Nodes (18): CompanyType, UserRole, GoogleLoginRequest, BaseModel, CandidateProfileResponse, Config, OnboardingStatusResponse, OnboardingSubmission (+10 more)

### Community 12 - "state.js"
Cohesion: 0.12
Nodes (18): login(), checkAuthStatus(), app, auth, googleProvider, initializeLoginPage(), initLoginPage(), initializeSignupPage() (+10 more)

### Community 13 - "api.js"
Cohesion: 0.17
Nodes (23): archiveJob(), createJob(), deleteCandidateResume(), deleteJob(), getCandidateResumeDetails(), getCandidateResumes(), getCandidateStats(), getJobs() (+15 more)

### Community 14 - "User"
Cohesion: 0.13
Nodes (27): Restricts route access to users registered with the CANDIDATE role., require_candidate(), User, candidate_status(), delete_candidate_resume(), get_candidate_resume_details(), get_candidate_resumes(), get_candidate_stats() (+19 more)

### Community 15 - "navbar.js"
Cohesion: 0.40
Nodes (5): initNavbar(), ROUTES, clearCandidateWorkspaceState(), renderFileList(), clearState()

### Community 16 - "s"
Cohesion: 0.15
Nodes (20): _a(), ac(), Bo(), db(), ea(), eb(), ga(), gb() (+12 more)

### Community 17 - "recruiter.js"
Cohesion: 0.18
Nodes (12): toggleButtonLoading(), populateRecruiterProfileUI(), updateStatisticCard(), clearRecruiterWorkspaceState(), initializeRecruiterScreen(), initRecruiterPage(), loadJobDescriptionsDropdown(), loadScoringProfilesDropdown() (+4 more)

### Community 18 - "Tween"
Cohesion: 0.15
Nodes (18): _assertThisInitialized(), Ec(), Fc(), gc(), ka(), qa(), t(), tb() (+10 more)

### Community 19 - "package.json"
Cohesion: 0.12
Nodes (15): autoprefixer, cors, firebase, dependencies, cors, firebase, devDependencies, autoprefixer (+7 more)

### Community 20 - "candidate.js"
Cohesion: 0.17
Nodes (18): getProfile(), getEmptyStateHTML(), sidebarLinkIds, updateSidebarActiveLink(), initCandidatePage(), initializeCandidateDashboard(), initializeCandidateProfile(), initializeCandidateScreen() (+10 more)

### Community 21 - "app.js"
Cohesion: 0.26
Nodes (11): clearCandidateState(), handleFiles(), renderFileList(), renderResults(), updateResumeCountDisplay(), uploadedFiles, getCandidateDetailRowHTML(), getCandidateRowHTML() (+3 more)

### Community 22 - "_d"
Cohesion: 0.29
Nodes (10): be(), _d(), fa(), ia(), ie(), je(), ke(), le() (+2 more)

### Community 23 - "onboarding.js"
Cohesion: 0.21
Nodes (15): API_BASE, API_ENDPOINTS, CANDIDATE_STATUS_VALUES, COMPANY_TYPES, MESSAGES, ROLES, getStepsForRole(), hideObError() (+7 more)

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
Cohesion: 0.29
Nodes (7): client(), db_session(), Create a new database session for a test., Create a test client using the test database., Creates a test user in the database., test_user(), fixture

### Community 29 - "cb"
Cohesion: 0.29
Nodes (7): Ab(), Bb(), cb(), Context(), Ew(), fb(), zb()

### Community 30 - "test_remediation.py"
Cohesion: 0.07
Nodes (35): anyio, extract_text(), extract_text_from_docx(), extract_text_from_pdf(), Extract text from a DOCX file, including paragraphs and tables., Route to appropriate extractor based on extension., Extract text from a PDF file., build_analysis_metadata() (+27 more)

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

### Community 36 - "env.py"
Cohesion: 0.20
Nodes (11): Run migrations in 'offline' mode., Run migrations in 'online' mode., run_migrations_offline(), run_migrations_online(), CandidateProfile, RecruiterProfile, post, Session (+3 more)

### Community 37 - "loadingOverlay.js"
Cohesion: 0.50
Nodes (3): loadingOverlay, STAGES, STATUS_MESSAGES

### Community 38 - "Q"
Cohesion: 0.50
Nodes (4): la(), Q(), Gb(), Hb()

### Community 39 - "r"
Cohesion: 0.50
Nodes (4): mc(), O(), P(), r()

### Community 48 - "legacy_process_resumes"
Cohesion: 0.29
Nodes (7): legacy_process_resumes(), limit, post, Request, Session, UploadFile, Legacy endpoint delegating to recruiter process_resumes. Requires Recruiter…

### Community 66 - "get_onboarding_status"
Cohesion: 0.67
Nodes (3): get_onboarding_status(), get, Returns the user's onboarding completion status and role.

## Knowledge Gaps
- **28 isolated node(s):** `Settings`, `uploadedFiles`, `sidebarLinkIds`, `COMPANY_TYPES`, `CANDIDATE_STATUS_VALUES` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `s()` connect `s` to `bf`, `gsap.min.js`, `Tween`, `app.js`, `cb`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `stages.py`, `get_onboarding_status`, `env.py`, `google_login`, `JobDescription`, `models/models.py`, `routers/test_auth.py`, `UserRole`, `legacy_process_resumes`, `test_user`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `XaiEngine` connect `stages.py` to `build_score_components`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `User` (e.g. with `CompanyType` and `ResumeStatus`) actually correct?**
  _`User` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `PipelineStage` (e.g. with `AnalysisPipeline` and `ResumeStatus`) actually correct?**
  _`PipelineStage` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `UserRole` (e.g. with `CandidateProfile` and `JobDescription`) actually correct?**
  _`UserRole` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `AnalysisContext` (e.g. with `AnalysisPipeline` and `ExplanationBuildingStage`) actually correct?**
  _`AnalysisContext` has 11 INFERRED edges - model-reasoned connections that need verification._