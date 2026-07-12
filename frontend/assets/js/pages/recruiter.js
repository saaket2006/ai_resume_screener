import * as api from '../api.js';
import * as state from '../state.js';
import { getRecruiterCandidateCardHTML } from '../components/candidateCard.js';
import { updateStatisticCard } from '../components/statisticCard.js';
import { populateRecruiterProfileUI } from '../components/profileSection.js';
import { toggleButtonLoading } from '../components/loadingSpinner.js';
import { MESSAGES } from '../constants.js';

let recUploadedFiles = [];
let initialized = false;

/**
 * Binds event listeners for recruiter workspace (runs once on startup).
 */
export function initRecruiterPage() {
    if (initialized) return;

    const recDropZone = document.getElementById('rec-drop-zone');
    const recResumesInput = document.getElementById('rec-resumes');
    const recResumesHeader = document.getElementById('rec-resumes-header');
    const recProcessBtn = document.getElementById('rec-process-btn');
    const recResultsContainer = document.getElementById('rec-results-container');
    const recJobDescription = document.getElementById('rec-job-description');

    if (recDropZone && recResumesInput) {
        recDropZone.addEventListener('click', () => recResumesInput.click());

        recDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            recDropZone.classList.add('drag-over');
        });

        recDropZone.addEventListener('dragleave', () => {
            recDropZone.classList.remove('drag-over');
        });

        recDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            recDropZone.classList.remove('drag-over');
            handleRecFiles(e.dataTransfer.files);
        });

        recResumesInput.addEventListener('change', (e) => {
            handleRecFiles(e.target.files);
        });
    }

    function handleRecFiles(files) {
        for (let file of files) {
            if (file.name.match(/\.(pdf|doc|docx)$/i)) {
                recUploadedFiles.push(file);
                renderRecFileList();
            } else {
                alert(`File ${file.name} is not a valid format. Only PDF and DOCX are supported.`);
            }
        }
        updateRecResumeCountDisplay();
    }

    window.removeRecFile = (index) => {
        recUploadedFiles.splice(index, 1);
        renderRecFileList();
        updateRecResumeCountDisplay();
        
        if (recUploadedFiles.length === 0) {
            recDropZone.classList.remove('collapsed', 'active');
            recResumesHeader.classList.add('hidden');
        }
    };

    if (recProcessBtn) {
        recProcessBtn.addEventListener('click', async () => {
            const jd = recJobDescription.value.trim();
            if (!jd) {
                alert(MESSAGES.ENTER_JD);
                return;
            }
            if (recUploadedFiles.length === 0) {
                alert(MESSAGES.UPLOAD_RESUME);
                return;
            }

            recResultsContainer.classList.add('hidden');

            recDropZone.classList.add('collapsed');
            recDropZone.classList.remove('active');
            recResumesHeader.classList.remove('hidden');
            updateRecResumeCountDisplay();

            const formData = new FormData();
            formData.append('job_description', jd);
            recUploadedFiles.forEach(file => {
                formData.append('resumes', file);
            });

            toggleButtonLoading(recProcessBtn, true, "Processing...", "Run ATS Screening");

            try {
                const data = await api.screenResumesRecruiter(formData);
                renderRecruiterResults(data.results);
            } catch (err) {
                alert(err.message);
            } finally {
                toggleButtonLoading(recProcessBtn, false, "Processing...", "Run ATS Screening");
            }
        });
    }

    const recQuickViewModal = document.getElementById('rec-quick-view-modal');
    const closeQuickViewBtn = document.getElementById('close-quick-view-btn');

    if (closeQuickViewBtn && recQuickViewModal) {
        closeQuickViewBtn.addEventListener('click', () => {
            recQuickViewModal.classList.add('hidden');
        });
        
        recQuickViewModal.addEventListener('click', (e) => {
            if (e.target === recQuickViewModal) {
                recQuickViewModal.classList.add('hidden');
            }
        });
    }

    initialized = true;
}

/**
 * Clears Recruiter workspace input state.
 */
export function clearRecruiterWorkspaceState() {
    const recJobDescription = document.getElementById('rec-job-description');
    const recDropZone = document.getElementById('rec-drop-zone');
    const recResumesHeader = document.getElementById('rec-resumes-header');
    const recResultsContainer = document.getElementById('rec-results-container');
    const recResultsList = document.getElementById('rec-results-list');

    if (recJobDescription) recJobDescription.value = '';
    recUploadedFiles = [];
    renderRecFileList();
    if (recDropZone) recDropZone.classList.remove('collapsed', 'active');
    if (recResumesHeader) recResumesHeader.classList.add('hidden');
    if (recResultsContainer) recResultsContainer.classList.add('hidden');
    if (recResultsList) recResultsList.innerHTML = '';
}

function updateRecResumeCountDisplay() {
    const recResumesCount = document.getElementById('rec-resumes-count');
    if (recResumesCount) {
        recResumesCount.textContent = `Resumes (${recUploadedFiles.length})`;
    }
}

function renderRecFileList() {
    const recFileList = document.getElementById('rec-file-list');
    if (!recFileList) return;
    recFileList.innerHTML = '';
    recUploadedFiles.forEach((file, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${file.name}</span>
            <span style="color: #ef4444; cursor:pointer;" onclick="removeRecFile(${index})">✕</span>
        `;
        recFileList.appendChild(li);
    });
}

/**
 * Initializer for Recruiter Dashboard view.
 */
export async function initializeRecruiterDashboard() {
    try {
        const profile = await api.getProfile();
        state.setProfile(profile);
        populateRecruiterProfileUI(profile);
        
        const stats = await api.getRecruiterStats();
        updateStatisticCard("stat-total-screened", stats.total_candidates_screened);
        updateStatisticCard("stat-avg-score", `${stats.average_ats_score.toFixed(1)}%`);
    } catch (err) {
        console.error("Error loading recruiter dashboard:", err);
    }
}

/**
 * Initializer for Recruiter Resume Screening view.
 */
export function initializeRecruiterScreen() {
    // Screening workspace just waits for user interaction; clear old inputs if needed or preserve
}

/**
 * Initializer for Recruiter Profile view.
 */
export async function initializeRecruiterProfile() {
    try {
        const profile = await api.getProfile();
        state.setProfile(profile);
        populateRecruiterProfileUI(profile);
    } catch (err) {
        console.error("Error loading recruiter profile:", err);
    }
}

function renderRecruiterResults(results) {
    const recResultsList = document.getElementById('rec-results-list');
    const recResultsContainer = document.getElementById('rec-results-container');
    if (!recResultsList) return;
    recResultsList.innerHTML = '';

    results.forEach(cand => {
        const card = document.createElement('div');
        card.className = 'candidate-card';
        card.innerHTML = getRecruiterCandidateCardHTML(cand);
        recResultsList.appendChild(card);
    });

    recResultsContainer.classList.remove('hidden');
    recResultsContainer.scrollIntoView({ behavior: 'smooth' });
}

// Modal quick view details mapping, bound to window
window.showCandidateQuickView = (cand) => {
    const recQuickViewModal = document.getElementById('rec-quick-view-modal');
    const qvCandName = document.getElementById('qv-cand-name');
    const qvCandScoreBadge = document.getElementById('qv-cand-score-badge');
    const qvCandEmail = document.getElementById('qv-cand-email');
    const qvCandPhone = document.getElementById('qv-cand-phone');
    const qvCandLinkedin = document.getElementById('qv-cand-linkedin');
    const qvCandGithub = document.getElementById('qv-cand-github');
    const qvCandEducation = document.getElementById('qv-cand-education');
    const qvCandExperience = document.getElementById('qv-cand-experience');
    const qvCandProjects = document.getElementById('qv-cand-projects');
    const qvCandExtractedSkills = document.getElementById('qv-cand-extracted-skills');
    const qvCandMatchedSkills = document.getElementById('qv-cand-matched-skills');
    const qvCandMissingSkills = document.getElementById('qv-cand-missing-skills');

    if (!recQuickViewModal) return;
    
    qvCandName.textContent = cand.name;
    
    let scoreClass = 'low-score';
    if (cand.similarity_score >= 70) {
        scoreClass = 'high-score';
    } else if (cand.similarity_score >= 40) {
        scoreClass = 'med-score';
    }
    
    qvCandScoreBadge.className = `score-badge ${scoreClass}`;
    qvCandScoreBadge.textContent = `${cand.similarity_score}% Match`;
    
    qvCandEmail.textContent = cand.email !== 'Not Provided' ? cand.email : 'N/A';
    qvCandPhone.textContent = cand.phone !== 'Not Provided' ? cand.phone : 'N/A';
    
    if (cand.linkedin !== 'Not Provided') {
        const url = cand.linkedin.startsWith('http') ? cand.linkedin : 'https://' + cand.linkedin;
        qvCandLinkedin.innerHTML = `<a href="${url}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.linkedin}</a>`;
    } else {
        qvCandLinkedin.textContent = 'N/A';
    }
    
    if (cand.github !== 'Not Provided') {
        const url = cand.github.startsWith('http') ? cand.github : 'https://' + cand.github;
        qvCandGithub.innerHTML = `<a href="${url}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.github}</a>`;
    } else {
        qvCandGithub.textContent = 'N/A';
    }
    
    qvCandEducation.textContent = cand.education || 'N/A';
    qvCandExperience.textContent = cand.experience ? `${cand.experience} Years` : '0 Years';
    qvCandProjects.textContent = cand.projects ? `${cand.projects} out of 5 projects match focus` : '0 projects matching';
    
    const allExtracted = cand.matched_skills.concat(cand.missing_skills);
    qvCandExtractedSkills.innerHTML = allExtracted.map(s => `<span class="skill-tag">${s}</span>`).join('') || '<span style="color:#666">None</span>';
    qvCandMatchedSkills.innerHTML = cand.matched_skills.map(s => `<span class="skill-tag matched">${s}</span>`).join('') || '<span style="color:#666">None</span>';
    qvCandMissingSkills.innerHTML = cand.missing_skills.map(s => `<span class="skill-tag missing">${s}</span>`).join('') || '<span style="color:#666">None</span>';
    
    recQuickViewModal.classList.remove('hidden');
};
