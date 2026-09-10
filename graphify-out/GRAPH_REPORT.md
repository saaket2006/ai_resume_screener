# Graph Report - .  (2026-09-10)

## Corpus Check
- 130 files · ~132,665 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 913 nodes · 2140 edges · 66 communities (58 shown, 8 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 273 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52
- Community 53
- Community 62
- Community 63
- Community 64

## God Nodes (most connected - your core abstractions)

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (66 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 1.00
Nodes (52): ResumeStatus, Resume, ScanResult, ScoringProfile, AnalysisContext, Any, Lightweight, shared context carrying tracing IDs, configurations, and stage…, ExplanationBuiltEvent (+44 more)

### Community 1 - "Community 1"
Cohesion: 1.00
Nodes (47): Defines thresholds and priorities for AI Resume Improvement Engine…, RecommendationPolicy, Defines recruiter-specific configurations and security permissions., RecruiterPolicy, Defines policy configurations for ATS scoring and weights. Removes magic…, ScoringPolicy, Defines policy configurations and fallback weights for adaptive scoring…, ScoringProfilePolicy (+39 more)

### Community 2 - "Community 2"
Cohesion: 1.00
Nodes (43): build_score_components(), Any, Builds the structured ScoreComponent list using the candidate's scored…, _resolve_status(), Any, Helper to construct a dict representation of StructuredExplanations., Generates structured multi-level explanations (SUMMARY, DETAILED, TECHNICAL)…, effective_exp_title() (+35 more)

### Community 3 - "Community 3"
Cohesion: 1.00
Nodes (27): get_weight(), Returns the matching weight for the given match type., MatchReason, MatchResult, BaseModel, Universal domain object representing a semantic match between a required skill…, Evaluates relationship type, confidence, and matches between two Skill objects.…, resolve_relationship() (+19 more)

### Community 4 - "Community 4"
Cohesion: 1.00
Nodes (40): extract_education(), extract_email(), extract_experience(), extract_github(), extract_linkedin(), extract_name(), extract_phone(), extract_projects() (+32 more)

### Community 5 - "Community 5"
Cohesion: 1.00
Nodes (35): anyio, extract_text(), extract_text_from_docx(), extract_text_from_pdf(), Extract text from a DOCX file, including paragraphs and tables., Route to appropriate extractor based on extension., Extract text from a PDF file., build_analysis_metadata() (+27 more)

### Community 6 - "Community 6"
Cohesion: 1.00
Nodes (39): legacy_process_resumes(), limit, post, Request, Session, UploadFile, Legacy endpoint delegating to recruiter process_resumes. Requires Recruiter…, User (+31 more)

### Community 7 - "Community 7"
Cohesion: 1.00
Nodes (14): Ec(), ee(), Fc(), Jd(), Kd(), Ld(), ma(), Md() (+6 more)

### Community 8 - "Community 8"
Cohesion: 1.00
Nodes (24): Run migrations in 'offline' mode., run_migrations_offline(), run_migrations_online(), api_route, Settings, check_db_connection(), get_db(), Tests connection to the configured database on demand (e.g. startup or health… (+16 more)

### Community 9 - "Community 9"
Cohesion: 1.00
Nodes (27): create_access_token(), get_password_hash(), Verifies a plain text password against the hashed version using bcrypt., Hashes a plain text password using bcrypt., Generates a secure JSON Web Token., verify_password(), fetch_google_certs(), get_me() (+19 more)

### Community 10 - "Community 10"
Cohesion: 1.00
Nodes (4): dc(), Ha(), Ia(), ob()

### Community 11 - "Community 11"
Cohesion: 1.00
Nodes (25): CompanyType, UserRole, CandidateProfile, RecruiterProfile, GoogleLoginRequest, BaseModel, post, Session (+17 more)

### Community 12 - "Community 12"
Cohesion: 1.00
Nodes (18): checkAuthStatus(), initNavbar(), app, auth, googleProvider, initializeLoginPage(), initLoginPage(), initializeSignupPage() (+10 more)

### Community 13 - "Community 13"
Cohesion: 1.00
Nodes (24): archiveJob(), createJob(), deleteCandidateResume(), deleteJob(), getCandidateResumeDetails(), getCandidateResumes(), getCandidateStats(), getJobs() (+16 more)

### Community 14 - "Community 14"
Cohesion: 1.00
Nodes (24): candidate_status(), delete_candidate_resume(), get_candidate_resume_details(), get_candidate_resumes(), get_candidate_stats(), process_candidate_resume(), BaseModel, delete (+16 more)

### Community 15 - "Community 15"
Cohesion: 1.00
Nodes (13): getEmptyStateHTML(), API_BASE, API_ENDPOINTS, CANDIDATE_STATUS_VALUES, COMPANY_TYPES, MESSAGES, ROUTES, clearCandidateWorkspaceState() (+5 more)

### Community 16 - "Community 16"
Cohesion: 1.00
Nodes (19): _a(), ac(), Bo(), db(), ea(), eb(), fa(), ga() (+11 more)

### Community 17 - "Community 17"
Cohesion: 1.00
Nodes (12): toggleButtonLoading(), populateRecruiterProfileUI(), updateStatisticCard(), clearRecruiterWorkspaceState(), initializeRecruiterScreen(), initRecruiterPage(), loadJobDescriptionsDropdown(), loadScoringProfilesDropdown() (+4 more)

### Community 18 - "Community 18"
Cohesion: 1.00
Nodes (16): _assertThisInitialized(), gc(), ka(), qa(), t(), tb(), Timeline(), Tween() (+8 more)

### Community 19 - "Community 19"
Cohesion: 1.00
Nodes (14): autoprefixer, cors, firebase, dependencies, cors, firebase, devDependencies, autoprefixer (+6 more)

### Community 20 - "Community 20"
Cohesion: 1.00
Nodes (13): getProfile(), sidebarLinkIds, updateSidebarActiveLink(), initializeCandidateDashboard(), initializeCandidateProfile(), initializeCandidateScreen(), initializeRecruiterDashboard(), initializeRecruiterProfile() (+5 more)

### Community 21 - "Community 21"
Cohesion: 1.00
Nodes (11): clearCandidateState(), handleFiles(), renderFileList(), renderResults(), updateResumeCountDisplay(), uploadedFiles, getCandidateDetailRowHTML(), getCandidateRowHTML() (+3 more)

### Community 22 - "Community 22"
Cohesion: 1.00
Nodes (13): be(), _d(), ia(), ie(), je(), ke(), le(), oe() (+5 more)

### Community 23 - "Community 23"
Cohesion: 1.00
Nodes (10): ROLES, getStepsForRole(), hideObError(), initializeOnboardingPage, initOnboarding(), showObError(), showOnboardingWizard(), submitOnboarding() (+2 more)

### Community 24 - "Community 24"
Cohesion: 1.00
Nodes (11): Fa(), Ga(), mb(), oc(), qc(), rc(), Ta(), ub() (+3 more)

### Community 25 - "Community 25"
Cohesion: 1.00
Nodes (9): Aa(), Animation(), ha(), ja(), Jc(), Lc(), Ra(), Sa() (+1 more)

### Community 26 - "Community 26"
Cohesion: 1.00
Nodes (9): Ab(), J(), jc(), kb(), lc(), Ra(), rb(), Sa() (+1 more)

### Community 27 - "Community 27"
Cohesion: 1.00
Nodes (6): initCounters(), initFeatureStack(), initHeroAnimation(), initNavbarEffects(), initStoryAnimation(), initWalkthrough()

### Community 28 - "Community 28"
Cohesion: 1.00
Nodes (7): client(), db_session(), Create a new database session for a test., Create a test client using the test database., Creates a test user in the database., test_user(), fixture

### Community 29 - "Community 29"
Cohesion: 1.00
Nodes (7): Ab(), Bb(), cb(), Context(), Ew(), fb(), zb()

### Community 30 - "Community 30"
Cohesion: 1.00
Nodes (6): gb(), hb(), lb(), oa(), ob(), Wa()

### Community 31 - "Community 31"
Cohesion: 1.00
Nodes (6): Bb(), Ja(), Ka(), La(), Oa(), z()

### Community 32 - "Community 32"
Cohesion: 1.00
Nodes (6): bf(), cf(), df(), kf(), mf(), N()

### Community 33 - "Community 33"
Cohesion: 1.00
Nodes (4): get_related_skills(), is_skill_in_text(), Checks if an explicit skill contains a broad conceptual keyword. For example,…, Checks if a skill or any of its known aliases exists in the given text. Handles…

### Community 34 - "Community 34"
Cohesion: 1.00
Nodes (5): A(), B(), F(), G(), K()

### Community 35 - "Community 35"
Cohesion: 1.00
Nodes (5): Nipun Main Branding Image, Candidate Portal HTML, Landing Index HTML, Onboarding Portal HTML, Recruiter Dashboard HTML

### Community 36 - "Community 36"
Cohesion: 1.00
Nodes (4): get_profile(), get, Retrieves the full profile details of the authenticated user., read_root()

### Community 37 - "Community 37"
Cohesion: 1.00
Nodes (3): loadingOverlay, STAGES, STATUS_MESSAGES

### Community 38 - "Community 38"
Cohesion: 1.00
Nodes (4): la(), Q(), Gb(), Hb()

### Community 39 - "Community 39"
Cohesion: 1.00
Nodes (4): mc(), O(), P(), r()

### Community 48 - "Community 48"
Cohesion: 1.00
Nodes (3): get_current_user(), Session, Validates the JWT token and returns the corresponding User. Raises 401…

## Knowledge Gaps
- **27 isolated node(s):** `Settings`, `uploadedFiles`, `sidebarLinkIds`, `COMPANY_TYPES`, `CANDIDATE_STATUS_VALUES` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.