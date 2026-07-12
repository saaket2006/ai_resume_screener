import * as api from '../api.js';
import * as state from '../state.js';
import { getEmptyStateHTML } from '../components/emptyState.js';
import { toggleButtonLoading } from '../components/loadingSpinner.js';
import { MESSAGES } from '../constants.js';

let candUploadedFile = null;
let initialized = false;

/**
 * Binds event listeners for candidate workspace views (runs once on startup).
 */
export function initCandidatePage() {
    if (initialized) return;

    const candDropZone = document.getElementById('cand-drop-zone');
    const candResumesInput = document.getElementById('cand-resumes');
    const candResumesHeader = document.getElementById('cand-resumes-header');
    const candProcessBtn = document.getElementById('cand-process-btn');
    const candResultsContainer = document.getElementById('cand-results-container');
    const candJobDescription = document.getElementById('cand-job-description');

    if (candDropZone && candResumesInput) {
        candDropZone.addEventListener('click', () => candResumesInput.click());

        candDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            candDropZone.classList.add('drag-over');
        });

        candDropZone.addEventListener('dragleave', () => {
            candDropZone.classList.remove('drag-over');
        });

        candDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            candDropZone.classList.remove('drag-over');
            handleCandidateFile(e.dataTransfer.files[0]);
        });

        candResumesInput.addEventListener('change', (e) => {
            handleCandidateFile(e.target.files[0]);
        });
    }

    function handleCandidateFile(file) {
        if (!file) return;
        if (file.name.match(/\.(pdf|doc|docx)$/i)) {
            candUploadedFile = file;
            renderFileList();
            updateResumeCountDisplay();
        } else {
            alert(`File ${file.name} is not a valid format. Only PDF and DOCX are supported.`);
        }
    }

    window.removeCandFile = () => {
        candUploadedFile = null;
        renderFileList();
        updateResumeCountDisplay();
        if (candDropZone) {
            candDropZone.classList.remove('collapsed', 'active');
        }
        if (candResumesHeader) {
            candResumesHeader.classList.add('hidden');
        }
    };

    if (candProcessBtn) {
        candProcessBtn.addEventListener('click', async () => {
            const jd = candJobDescription.value.trim();
            if (!jd) {
                alert(MESSAGES.ENTER_JD);
                return;
            }
            if (!candUploadedFile) {
                alert(MESSAGES.UPLOAD_RESUME);
                return;
            }

            candResultsContainer.classList.add('hidden');

            if (candDropZone) {
                candDropZone.classList.add('collapsed');
                candDropZone.classList.remove('active');
            }
            if (candResumesHeader) {
                candResumesHeader.classList.remove('hidden');
            }
            updateResumeCountDisplay();

            const formData = new FormData();
            formData.append('job_description', jd);
            formData.append('resume', candUploadedFile);

            toggleButtonLoading(candProcessBtn, true, "Analyzing...", "Analyze Resume");

            try {
                const results = await api.screenResumeCandidate(formData);
                renderCandidateAnalysisResults(results.results[0]);
            } catch (err) {
                alert(err.message);
            } finally {
                toggleButtonLoading(candProcessBtn, false, "Analyzing...", "Analyze Resume");
            }
        });
    }

    initialized = true;
}

function updateResumeCountDisplay() {
    const countSpan = document.getElementById('cand-resumes-count');
    if (countSpan) {
        countSpan.textContent = candUploadedFile ? "Resume (1)" : "Resume (0)";
    }
}

function renderFileList() {
    const list = document.getElementById('cand-file-list');
    if (!list) return;
    list.innerHTML = '';
    if (candUploadedFile) {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${candUploadedFile.name}</span>
            <span style="color: #ef4444; cursor:pointer;" onclick="removeCandFile()">✕</span>
        `;
        list.appendChild(li);
    }
}

export function clearCandidateWorkspaceState() {
    const candJobDescription = document.getElementById('cand-job-description');
    const candDropZone = document.getElementById('cand-drop-zone');
    const candResumesHeader = document.getElementById('cand-resumes-header');
    const candResultsContainer = document.getElementById('cand-results-container');
    
    if (candJobDescription) candJobDescription.value = '';
    candUploadedFile = null;
    renderFileList();
    if (candDropZone) candDropZone.classList.remove('collapsed', 'active');
    if (candResumesHeader) candResumesHeader.classList.add('hidden');
    if (candResultsContainer) candResultsContainer.classList.add('hidden');
}

/**
 * Page view initializer for Candidate Dashboard.
 */
export async function initializeCandidateDashboard() {
    const dashCandName = document.getElementById('dash-cand-name');
    const dashCandStatus = document.getElementById('dash-cand-status');
    const dashCandField = document.getElementById('dash-cand-field');
    const dashCandDomain = document.getElementById('dash-cand-domain');
    const candTopUserName = document.getElementById('cand-top-user-name');
    const statsContainer = document.getElementById('cand-stats-container');

    if (!statsContainer) return;

    try {
        // Fetch candidate details
        const profile = await api.getProfile();
        state.setProfile(profile);

        const candName = profile.email.split('@')[0];
        const statusVal = profile.candidate_profile?.current_status || "N/A";
        const fieldVal = profile.candidate_profile?.field_of_study || "N/A";
        const domainVal = profile.candidate_profile?.current_domain || "N/A";

        if (dashCandName) dashCandName.textContent = candName;
        if (dashCandStatus) dashCandStatus.textContent = statusVal;
        if (dashCandField) dashCandField.textContent = fieldVal;
        if (dashCandDomain) dashCandDomain.textContent = domainVal;
        if (candTopUserName) candTopUserName.textContent = candName;

        // Fetch candidate stats
        const stats = await api.getCandidateStats();
        
        if (stats.latest_ats_score !== null && stats.latest_ats_score !== undefined) {
            statsContainer.innerHTML = `
                <div class="rec-grid">
                    <div class="stat-card">
                        <div class="stat-header">
                            <span class="stat-title">Latest ATS Score</span>
                            <span class="stat-icon">📈</span>
                        </div>
                        <div class="stat-value" id="cand-stat-latest-score">${stats.latest_ats_score}%</div>
                        <p class="stat-description">Most recent semantic relevance match</p>
                    </div>
                </div>
            `;
        } else {
            statsContainer.innerHTML = getEmptyStateHTML("You have not analyzed any resumes yet. Go to Resume Analysis to evaluate your resume!");
        }
    } catch (err) {
        console.error("Error loading candidate dashboard stats:", err);
    }
}

/**
 * Page view initializer for Candidate Resume Analysis view.
 */
export function initializeCandidateScreen() {
    // Screening workspace awaits input
}

/**
 * Page view initializer for Candidate Profile view.
 */
export async function initializeCandidateProfile() {
    const profileCandName = document.getElementById('profile-cand-name');
    const profileCandEmail = document.getElementById('profile-cand-email');
    const profileCandStatus = document.getElementById('profile-cand-status');
    const profileCandField = document.getElementById('profile-cand-field');
    const profileCandDomain = document.getElementById('profile-cand-domain');

    try {
        const profile = await api.getProfile();
        state.setProfile(profile);

        const candName = profile.email.split('@')[0];
        if (profileCandName) profileCandName.textContent = candName;
        if (profileCandEmail) profileCandEmail.textContent = profile.email;
        if (profileCandStatus) profileCandStatus.textContent = profile.candidate_profile?.current_status || "N/A";
        if (profileCandField) profileCandField.textContent = profile.candidate_profile?.field_of_study || "N/A";
        if (profileCandDomain) profileCandDomain.textContent = profile.candidate_profile?.current_domain || "N/A";
    } catch (err) {
        console.error("Error loading candidate profile details:", err);
    }
}

function renderCandidateAnalysisResults(cand) {
    const resultsDetails = document.getElementById('cand-results-details');
    const resultsContainer = document.getElementById('cand-results-container');
    if (!resultsDetails || !resultsContainer) return;

    let scoreClass = 'low-score';
    if (cand.similarity_score >= 70) {
        scoreClass = 'high-score';
    } else if (cand.similarity_score >= 40) {
        scoreClass = 'med-score';
    }

    const matchedTags = cand.matched_skills.map(s => `<span class="skill-tag matched">${s}</span>`).join('') || '<span style="color:#666">None</span>';
    const missingTags = cand.missing_skills.map(s => `<span class="skill-tag missing">${s}</span>`).join('') || '<span style="color:#666">None</span>';
    const extractedTags = cand.matched_skills.concat(cand.missing_skills).map(s => `<span class="skill-tag">${s}</span>`).join('') || '<span style="color:#666">None</span>';

    resultsDetails.innerHTML = `
        <div class="qv-profile-summary" style="display: flex; align-items: center; gap: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 1.5rem;">
            <div class="qv-avatar" style="font-size: 3rem; background: rgba(255,255,255,0.02); width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">📄</div>
            <div class="qv-meta">
                <h2 style="font-size: 1.6rem; font-weight: 800; color: #fff; margin: 0 0 0.25rem 0;">${cand.name}</h2>
                <p class="score-badge ${scoreClass}" style="font-size: 1.25rem; font-weight: bold; margin: 0;">${cand.similarity_score}% Match</p>
            </div>
        </div>

        <div style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 1.5rem;">
            <div>
                <h4 style="font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid rgba(255,255,255,0.03); padding-bottom: 0.5rem; margin-bottom: 0.5rem;">Resume Information</h4>
                <div class="profile-info-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div class="info-field">
                        <span class="info-label" style="font-size: 0.75rem; color: #94a3b8;">Education</span>
                        <span class="info-value" style="color: #fff; font-weight: 500;">${cand.education || 'N/A'}</span>
                    </div>
                    <div class="info-field">
                        <span class="info-label" style="font-size: 0.75rem; color: #94a3b8;">Experience</span>
                        <span class="info-value" style="color: #fff; font-weight: 500;">${cand.experience ? `${cand.experience} Years` : '0 Years'}</span>
                    </div>
                    <div class="info-field">
                        <span class="info-label" style="font-size: 0.75rem; color: #94a3b8;">Projects Match</span>
                        <span class="info-value" style="color: #fff; font-weight: 500;">${cand.projects ? `${cand.projects} out of 5 projects` : '0 projects'}</span>
                    </div>
                </div>
            </div>

            <div>
                <h4 style="font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid rgba(255,255,255,0.03); padding-bottom: 0.5rem; margin-bottom: 0.5rem;">Skills Overview</h4>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div>
                        <h5 style="margin: 0 0 0.5rem 0; font-size: 0.8rem; color: #cbd5e1; font-weight: 600;">Extracted Skills</h5>
                        <div class="skills-tags-container" style="display: flex; flex-wrap: wrap; gap: 0.5rem;">${extractedTags}</div>
                    </div>
                    <div>
                        <h5 style="margin: 0 0 0.5rem 0; font-size: 0.8rem; color: #cbd5e1; font-weight: 600;">✅ Matched Skills</h5>
                        <div class="skills-tags-container" style="display: flex; flex-wrap: wrap; gap: 0.5rem;">${matchedTags}</div>
                    </div>
                    <div>
                        <h5 style="margin: 0 0 0.5rem 0; font-size: 0.8rem; color: #cbd5e1; font-weight: 600;">❌ Missing Skills</h5>
                        <div class="skills-tags-container" style="display: flex; flex-wrap: wrap; gap: 0.5rem;">${missingTags}</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    resultsContainer.classList.remove('hidden');
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}
