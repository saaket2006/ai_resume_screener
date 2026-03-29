import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js";
import {
    getAuth,
    signInWithEmailAndPassword,
    signInWithPopup,
    GoogleAuthProvider,
    onAuthStateChanged,
    signOut,
    setPersistence,
    browserSessionPersistence,
    inMemoryPersistence
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";

import { firebaseConfig } from "./firebase-config.js";

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Use inMemoryPersistence to ensure logout on any page refresh or tab close
setPersistence(auth, inMemoryPersistence)
    .catch((error) => {
        console.error("Auth persistence error:", error);
    });

const googleProvider = new GoogleAuthProvider();

document.addEventListener('DOMContentLoaded', () => {
    // Auth Elements
    const authModal = document.getElementById('auth-modal');
    const appContainer = document.getElementById('app-container');
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailLoginBtn = document.getElementById('email-login-btn');
    const googleLoginBtn = document.getElementById('google-login-btn');
    const signOutBtn = document.getElementById('sign-out-btn');
    const authErrorMsg = document.getElementById('auth-error');

    // Authentication Listeners
    onAuthStateChanged(auth, (user) => {
        if (user) {
            authModal.classList.add('hidden');
            appContainer.classList.remove('hidden');
        } else {
            authModal.classList.remove('hidden');
            appContainer.classList.add('hidden');
        }
    });

    const showError = (message) => {
        authErrorMsg.textContent = message;
        authErrorMsg.classList.remove('hidden');
    };

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        const btnText = emailLoginBtn.querySelector('span');

        btnText.textContent = "Signing in...";
        emailLoginBtn.disabled = true;
        authErrorMsg.classList.add('hidden');

        try {
            await signInWithEmailAndPassword(auth, email, password);
            loginForm.reset();
        } catch (error) {
            showError("Authentication failed: " + error.message);
        } finally {
            btnText.textContent = "Sign In";
            emailLoginBtn.disabled = false;
        }
    });

    googleLoginBtn.addEventListener('click', async () => {
        authErrorMsg.classList.add('hidden');
        try {
            await signInWithPopup(auth, googleProvider);
        } catch (error) {
            showError("Google Sign-In failed: " + error.message);
        }
    });

    signOutBtn.addEventListener('click', async () => {
        try {
            await signOut(auth);
        } catch (error) {
            console.error("Error signing out: ", error);
        }
    });

    // Original app elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('resumes');
    const fileList = document.getElementById('file-list');
    const processBtn = document.getElementById('process-btn');
    const btnText = processBtn.querySelector('span');
    const loader = processBtn.querySelector('.loader');
    const resultsContainer = document.getElementById('results-container');
    const resultsBody = document.getElementById('results-body');
    const jdInput = document.getElementById('job-description');

    let uploadedFiles = [];

    // Drag & Drop handlers
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    function handleFiles(files) {
        for (let file of files) {
            if (file.name.match(/\.(pdf|doc|docx)$/i)) {
                uploadedFiles.push(file);
                renderFileList();
            } else {
                alert(`File ${file.name} is not a valid format. Only PDF and DOCX are supported.`);
            }
        }
    }

    function renderFileList() {
        fileList.innerHTML = '';
        uploadedFiles.forEach((file, index) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${file.name}</span>
                <span style="color: #ef4444; cursor:pointer;" onclick="removeFile(${index})">✕</span>
            `;
            fileList.appendChild(li);
        });
    }

    window.removeFile = (index) => {
        uploadedFiles.splice(index, 1);
        renderFileList();
    };

    processBtn.addEventListener('click', async () => {
        const jd = jdInput.value.trim();
        if (!jd) {
            alert("Please enter a job description.");
            return;
        }
        if (uploadedFiles.length === 0) {
            alert("Please upload at least one resume.");
            return;
        }

        btnText.textContent = "Processing...";
        loader.classList.remove('hidden');
        processBtn.disabled = true;
        resultsContainer.classList.add('hidden');

        const formData = new FormData();
        formData.append('job_description', jd);
        uploadedFiles.forEach(file => {
            formData.append('resumes', file);
        });

        try {
            const response = await fetch("https://ai-resume-screener-production-2bb2.up.railway.app/api/process", {
                method: "POST",
                body: formData
            });

            const text = await response.text();

            console.log("RAW RESPONSE:", text);

            if (!response.ok) {
                alert("Server Error:\n" + text);
                throw new Error("Request failed");
            }

            const data = JSON.parse(text);
            renderResults(data.results);

        } catch (error) {
            alert(error.message);
        } finally {
            btnText.textContent = "Rank Candidates";
            loader.classList.add('hidden');
            processBtn.disabled = false;
        }
    });

    function renderResults(results) {
        resultsBody.innerHTML = '';

        results.forEach(cand => {
            // --- Main Row ---
            const tr = document.createElement('tr');
            tr.classList.add('candidate-row');

            const rankClass = cand.rank <= 3 ? `rank-${cand.rank}` : '';

            let scoreClass = 'low-score';
            let fillClass = 'score-fill-low';
            if (cand.similarity_score >= 15) {
                scoreClass = 'high-score';
                fillClass = 'score-fill-high';
            } else if (cand.similarity_score >= 5) {
                scoreClass = 'med-score';
                fillClass = 'score-fill-med';
            }

            tr.innerHTML = `
                <td><span class="rank-badge ${rankClass}">#${cand.rank}</span></td>
                <td>
                    <strong>${cand.name}</strong><br>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">📧 ${cand.email !== 'Not Provided' ? cand.email : '<span style="opacity:0.6">Not Provided</span>'}</small>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">📞 ${cand.phone !== 'Not Provided' ? cand.phone : '<span style="opacity:0.6">Not Provided</span>'}</small>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">🔗 ${cand.linkedin !== 'Not Provided' ? `<a href="${cand.linkedin.startsWith('http') ? cand.linkedin : 'https://' + cand.linkedin}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.linkedin}</a>` : '<span style="opacity:0.6">LinkedIn Not Provided</span>'}</small>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">💻 ${cand.github !== 'Not Provided' ? `<a href="${cand.github.startsWith('http') ? cand.github : 'https://' + cand.github}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.github}</a>` : '<span style="opacity:0.6">GitHub Not Provided</span>'}</small>
                    <div class="candidate-stats">
                        <span class="stat-badge">🎓 ${cand.education || 'None'}</span>
                        <span class="stat-badge">💼 ${cand.experience || 0} Yrs</span>
                        <span class="stat-badge">🚀 Proj: ${cand.projects || 0}/5</span>
                    </div>
                </td>
                <td style="min-width: 150px;">
                    <span class="score-badge ${scoreClass}">${cand.similarity_score}%</span>
                    <div class="score-container">
                        <div class="score-bar-fill ${fillClass}" style="width: 0%" data-target="${Math.min(cand.similarity_score, 100)}%"></div>
                    </div>
                </td>
                <td class="expand-hint-cell"><span class="expand-chevron">▶</span></td>
            `;
            resultsBody.appendChild(tr);

            // --- Expandable Detail Row ---
            const detailTr = document.createElement('tr');
            detailTr.classList.add('detail-row');

            const matchedHtml = cand.matched_skills.map(s => `<span class="skill-tag matched">${s}</span>`).join('');
            const missingHtml = cand.missing_skills.map(s => `<span class="skill-tag missing">${s}</span>`).join('');

            // Build score breakdown bars
            const breakdownItems = [
                { label: 'Skill Match', value: cand.skill_score || 0, weight: '50%' },
                { label: 'Experience', value: cand.experience_score || 0, weight: '25%' },
                { label: 'Education', value: cand.education_score || 0, weight: '15%' },
                { label: 'Projects', value: cand.projects_score || 0, weight: '10%' },
            ];

            let breakdownHtml = breakdownItems.map(item => {
                const val = Math.round(item.value);
                let barClass = 'score-fill-low';
                if (val >= 60) barClass = 'score-fill-high';
                else if (val >= 30) barClass = 'score-fill-med';
                return `
                    <div class="breakdown-item">
                        <div class="breakdown-label">
                            <span>${item.label}</span>
                            <span class="breakdown-weight">(${item.weight})</span>
                            <span class="breakdown-value">${val}%</span>
                        </div>
                        <div class="score-container breakdown-bar">
                            <div class="score-bar-fill ${barClass}" style="width: 0%" data-target="${val}%"></div>
                        </div>
                    </div>`;
            }).join('');

            // Final score summary line
            breakdownHtml += `
                <div class="breakdown-final">
                    <span>Final Score</span>
                    <span class="final-score-value">${cand.similarity_score}%</span>
                </div>`;

            detailTr.innerHTML = `
                <td colspan="4" class="detail-cell">
                    <div class="detail-panel">
                        <div class="detail-section">
                            <h4>📊 Score Breakdown</h4>
                            <div class="breakdown-grid">${breakdownHtml}</div>
                        </div>
                        <div class="detail-section">
                            <h4>✅ Matched Skills</h4>
                            <div class="skills-list">${matchedHtml || '<span style="color:#666">None</span>'}</div>
                        </div>
                        <div class="detail-section">
                            <h4>❌ Missing Skills</h4>
                            <div class="skills-list">${missingHtml || '<span style="color:#666">None</span>'}</div>
                        </div>
                    </div>
                </td>
            `;
            resultsBody.appendChild(detailTr);

            // Toggle detail row on main row click
            tr.addEventListener('click', (e) => {
                // Don't toggle if clicking a link
                if (e.target.tagName === 'A') return;
                const isOpen = detailTr.classList.toggle('open');
                tr.querySelector('.expand-chevron').textContent = isOpen ? '▼' : '▶';

                // Animate breakdown bars when opening
                if (isOpen) {
                    setTimeout(() => {
                        detailTr.querySelectorAll('.score-bar-fill').forEach(bar => {
                            bar.style.width = bar.getAttribute('data-target');
                        });
                    }, 50);
                } else {
                    detailTr.querySelectorAll('.score-bar-fill').forEach(bar => {
                        bar.style.width = '0%';
                    });
                }
            });
        });

        resultsContainer.classList.remove('hidden');
        resultsContainer.scrollIntoView({ behavior: 'smooth' });

        // Trigger main score bar animations
        setTimeout(() => {
            const bars = resultsBody.querySelectorAll('.candidate-row .score-bar-fill');
            bars.forEach(bar => {
                bar.style.width = bar.getAttribute('data-target');
            });
        }, 100);
    }
});
