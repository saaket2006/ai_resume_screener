import { API_BASE, API_ENDPOINTS } from './constants.js';
import * as state from './state.js';

/**
 * Shared HTTP request helper with timeout, auth token injection, and global error handling.
 */
async function request(endpoint, options = {}) {
    const token = state.getToken();
    const headers = { ...options.headers };

    // Auto-inject auth header
    if (token && !headers["Authorization"]) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    // Default Content-Type to application/json except for FormData
    if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
    }

    const timeout = options.timeout || 15000; // 15 seconds default timeout
    const controller = new AbortController();
    const timerId = setTimeout(() => controller.abort(), timeout);

    const config = {
        ...options,
        headers,
        signal: controller.signal
    };

    const url = endpoint.startsWith("http") ? endpoint : `${API_BASE}${endpoint}`;

    try {
        const response = await fetch(url, config);
        clearTimeout(timerId);

        // Global session expiration handler (401 Unauthorized)
        if (response.status === 401) {
            state.clearState();
            window.location.hash = "#/login";
            throw new Error("Session expired. Please log in again.");
        }

        const contentType = response.headers.get("content-type");
        let data;
        if (contentType && contentType.includes("application/json")) {
            data = await response.json();
        } else {
            data = await response.text();
        }

        if (!response.ok) {
            const message = (data && data.detail) || data || "Request failed";
            throw new Error(message);
        }

        return data;
    } catch (error) {
        clearTimeout(timerId);
        if (error.name === "AbortError") {
            throw new Error("Request timed out");
        }
        throw error;
    }
}

/**
 * POST /api/auth/login
 */
export async function login(email, password) {
    return request(API_ENDPOINTS.LOGIN, {
        method: "POST",
        body: JSON.stringify({ email, password })
    });
}

/**
 * POST /api/auth/signup
 */
export async function signup(email, password) {
    return request(API_ENDPOINTS.SIGNUP, {
        method: "POST",
        body: JSON.stringify({ email, password })
    });
}

/**
 * GET /api/auth/me
 */
export async function getMe() {
    return request(API_ENDPOINTS.ME, {
        method: "GET"
    });
}

/**
 * GET /api/profile
 */
export async function getProfile() {
    return request(API_ENDPOINTS.PROFILE, {
        method: "GET"
    });
}

/**
 * GET /api/recruiter/stats
 */
export async function getRecruiterStats() {
    return request(API_ENDPOINTS.STATS, {
        method: "GET"
    });
}

/**
 * POST /api/onboarding/recruiter
 */
export async function submitRecruiterOnboarding(payload) {
    return request(API_ENDPOINTS.ONBOARDING_RECRUITER, {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

/**
 * POST /api/onboarding/candidate
 */
export async function submitCandidateOnboarding(payload) {
    return request(API_ENDPOINTS.ONBOARDING_CANDIDATE, {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

/**
 * POST /api/process (legacy candidate-facing ATS)
 */
export async function screenResumes(formData) {
    return request(API_ENDPOINTS.PROCESS, {
        method: "POST",
        body: formData
    });
}

/**
 * POST /api/recruiter/process
 */
export async function screenResumesRecruiter(formData) {
    return request(API_ENDPOINTS.PROCESS_RECRUITER, {
        method: "POST",
        body: formData
    });
}

/**
 * GET /api/candidate/stats
 */
export async function getCandidateStats() {
    return request(API_ENDPOINTS.CANDIDATE_STATS, {
        method: "GET"
    });
}

/**
 * POST /api/candidate/process
 */
export async function screenResumeCandidate(formData) {
    return request(API_ENDPOINTS.CANDIDATE_PROCESS, {
        method: "POST",
        body: formData
    });
}

/**
 * GET /api/candidate/resumes
 */
export async function getCandidateResumes() {
    return request(API_ENDPOINTS.CANDIDATE_RESUMES, {
        method: "GET"
    });
}

/**
 * GET /api/candidate/resumes/{resume_id}
 */
export async function getCandidateResumeDetails(resumeId) {
    return request(`${API_ENDPOINTS.CANDIDATE_RESUMES}/${resumeId}`, {
        method: "GET"
    });
}

/**
 * DELETE /api/candidate/resumes/{resume_id}
 */
export async function deleteCandidateResume(resumeId) {
    return request(`${API_ENDPOINTS.CANDIDATE_RESUMES}/${resumeId}`, {
        method: "DELETE"
    });
}

/**
 * PUT /api/candidate/resumes/{resume_id}/label
 */
export async function updateCandidateResumeLabel(resumeId, label) {
    return request(`${API_ENDPOINTS.CANDIDATE_RESUMES}/${resumeId}/label`, {
        method: "PUT",
        body: JSON.stringify({ label })
    });
}

/**
 * GET /api/recruiter/profiles
 */
export async function getScoringProfiles() {
    return request(API_ENDPOINTS.PROFILES, {
        method: "GET"
    });
}

/**
 * GET /api/recruiter/jobs
 */
export async function getJobs(includeArchived = false) {
    return request(`${API_ENDPOINTS.JOBS}?include_archived=${includeArchived}`, {
        method: "GET"
    });
}

/**
 * POST /api/recruiter/jobs
 */
export async function createJob(formData) {
    return request(API_ENDPOINTS.JOBS, {
        method: "POST",
        body: formData
    });
}

/**
 * PUT /api/recruiter/jobs/{jd_id}
 */
export async function updateJob(jdId, formData) {
    return request(`${API_ENDPOINTS.JOBS}/${jdId}`, {
        method: "PUT",
        body: formData
    });
}

/**
 * DELETE /api/recruiter/jobs/{jd_id}
 */
export async function archiveJob(jdId) {
    return request(`${API_ENDPOINTS.JOBS}/${jdId}`, {
        method: "DELETE"
    });
}

/**
 * DELETE /api/recruiter/jobs/{jd_id}/delete
 */
export async function deleteJob(jdId) {
    return request(`${API_ENDPOINTS.JOBS}/${jdId}/delete`, {
        method: "DELETE"
    });
}
