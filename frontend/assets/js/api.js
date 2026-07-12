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
