document.addEventListener('DOMContentLoaded', () => {
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
            const response = await fetch('http://127.0.0.1:8000/api/process', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Error processing resumes.");
            }

            const data = await response.json();
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
            const tr = document.createElement('tr');

            const rankClass = cand.rank <= 3 ? `rank-${cand.rank}` : '';

            let scoreClass = 'low-score';
            if (cand.similarity_score >= 15) scoreClass = 'high-score';
            else if (cand.similarity_score >= 5) scoreClass = 'med-score';

            const matchedHtml = cand.matched_skills.map(s => `<span class="skill-tag matched">${s}</span>`).join('');
            const missingHtml = cand.missing_skills.map(s => `<span class="skill-tag missing">${s}</span>`).join('');

            tr.innerHTML = `
                <td><span class="rank-badge ${rankClass}">#${cand.rank}</span></td>
                <td>
                    <strong>${cand.name}</strong><br>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">📧 ${cand.email !== 'Not Provided' ? cand.email : '<span style="opacity:0.6">Not Provided</span>'}</small>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">📞 ${cand.phone !== 'Not Provided' ? cand.phone : '<span style="opacity:0.6">Not Provided</span>'}</small>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">🔗 ${cand.linkedin !== 'Not Provided' ? `<a href="${cand.linkedin.startsWith('http') ? cand.linkedin : 'https://' + cand.linkedin}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.linkedin}</a>` : '<span style="opacity:0.6">LinkedIn Not Provided</span>'}</small>
                    <small style="color:var(--text-secondary); display:block; margin-top:2px;">💻 ${cand.github !== 'Not Provided' ? `<a href="${cand.github.startsWith('http') ? cand.github : 'https://' + cand.github}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.github}</a>` : '<span style="opacity:0.6">GitHub Not Provided</span>'}</small>
                    <small style="opacity: 0.6; font-size: 0.75rem; display:block; margin-top:4px;">File: ${cand.filename}</small>
                </td>
                <td><span class="score-badge ${scoreClass}">${cand.similarity_score}%</span></td>
                <td>${matchedHtml || '<span style="color:#666">-</span>'}</td>
                <td>${missingHtml || '<span style="color:#666">-</span>'}</td>
            `;
            resultsBody.appendChild(tr);
        });

        resultsContainer.classList.remove('hidden');
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
});
