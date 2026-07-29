/**
 * Unified candidate layout rendering component.
 * Outputs exact same HTML markup structure, attributes, and classes to keep UI identical.
 */

/**
 * Returns candidate row HTML string for the legacy table.
 */
export function getCandidateRowHTML(cand) {
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

    const email = cand.email !== 'Not Provided' ? cand.email : '<span style="opacity:0.6">Not Provided</span>';
    const phone = cand.phone !== 'Not Provided' ? cand.phone : '<span style="opacity:0.6">Not Provided</span>';
    
    const linkedin = cand.linkedin !== 'Not Provided' 
        ? `<a href="${cand.linkedin.startsWith('http') ? cand.linkedin : 'https://' + cand.linkedin}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.linkedin}</a>` 
        : '<span style="opacity:0.6">LinkedIn Not Provided</span>';

    const github = cand.github !== 'Not Provided' 
        ? `<a href="${cand.github.startsWith('http') ? cand.github : 'https://' + cand.github}" target="_blank" style="color: #6366f1; text-decoration: none;">${cand.github}</a>` 
        : '<span style="opacity:0.6">GitHub Not Provided</span>';

    return `
        <td><span class="rank-badge ${rankClass}">#${cand.rank}</span></td>
        <td>
            <strong>${cand.name}</strong><br>
            <small style="color:var(--text-secondary); display:block; margin-top:2px;">&#x1F4E7; ${email}</small>
            <small style="color:var(--text-secondary); display:block; margin-top:2px;">&#x1F4DE; ${phone}</small>
            <small style="color:var(--text-secondary); display:block; margin-top:2px;">&#x1F517; ${linkedin}</small>
            <small style="color:var(--text-secondary); display:block; margin-top:2px;">&#x1F4BB; ${github}</small>
            <div class="candidate-stats">
                <span class="stat-badge">&#x1F393; ${cand.education || 'None'}</span>
                <span class="stat-badge">&#x1F4BC; ${cand.experience || 0} Yrs</span>
                <span class="stat-badge">&#x1F680; Proj: ${cand.projects || 0}/5</span>
            </div>
        </td>
        <td style="min-width: 150px;">
            <span class="score-badge ${scoreClass}">${cand.similarity_score}%</span>
            <div class="score-container">
                <div class="score-bar-fill ${fillClass}" style="width: 0%" data-target="${Math.min(cand.similarity_score, 100)}%"></div>
            </div>
        </td>
        <td class="expand-hint-cell"><span class="expand-chevron">&#x25B6;</span></td>
    `;
}

/**
 * Returns candidate detail row HTML string for the legacy table.
 */
export function getCandidateDetailRowHTML(cand) {
    const matchedHtml = cand.matched_skills.map(s => `<span class="skill-tag matched">${s}</span>`).join('');
    const missingHtml = cand.missing_skills.map(s => `<span class="skill-tag missing">${s}</span>`).join('');

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

    breakdownHtml += `
        <div class="breakdown-final">
            <span>Final Score</span>
            <span class="final-score-value">${cand.similarity_score}%</span>
        </div>`;

    return `
        <td colspan="4" class="detail-cell">
            <div class="detail-panel">
                <div class="detail-section">
                    <h4>&#x1F4CA; Score Breakdown</h4>
                    <div class="breakdown-grid">${breakdownHtml}</div>
                </div>
                <div class="detail-section">
                    <h4>&#x2705; Matched Skills</h4>
                    <div class="skills-list">${matchedHtml || '<span style="color:#666">None</span>'}</div>
                </div>
                <div class="detail-section">
                    <h4>&#x274C; Missing Skills</h4>
                    <div class="skills-list">${missingHtml || '<span style="color:#666">None</span>'}</div>
                </div>
            </div>
        </td>
    `;
}

/**
 * Returns candidate card HTML string for the Recruiter Workspace.
 */
export function getRecruiterCandidateCardHTML(cand) {
    const isTopRank = cand.rank <= 3 ? 'top-rank' : '';
    
    let scoreClass = 'low-score';
    if (cand.similarity_score >= 70) {
        scoreClass = 'high-score';
    } else if (cand.similarity_score >= 40) {
        scoreClass = 'med-score';
    }

    const matchedTags = cand.matched_skills.slice(0, 5).map(s => `<span class="skill-tag matched">${s}</span>`).join('');
    const missingTags = cand.missing_skills.slice(0, 5).map(s => `<span class="skill-tag missing">${s}</span>`).join('');

    const candString = JSON.stringify(cand).replace(/'/g, "&apos;");

    return `
        <div class="cand-left">
            <div class="cand-rank ${isTopRank}">#${cand.rank}</div>
            <div class="cand-info">
                <h4 class="cand-name">${cand.name}</h4>
                <div class="cand-skills-summary">
                    <div class="skills-row">
                        <span class="skills-row-label matched">Matched:</span>
                        ${matchedTags || '<span style="color:#666; font-size:0.8rem;">None</span>'}
                    </div>
                    <div class="skills-row" style="margin-top: 0.25rem;">
                        <span class="skills-row-label missing">Missing:</span>
                        ${missingTags || '<span style="color:#666; font-size:0.8rem;">None</span>'}
                    </div>
                </div>
            </div>
        </div>
        <div class="cand-right">
            <div class="score-block">
                <span class="score-badge ${scoreClass}">${cand.similarity_score}%</span>
            </div>
            <button class="quick-view-btn" onclick='showCandidateQuickView(${candString})'>Quick View</button>
        </div>
    `;
}
