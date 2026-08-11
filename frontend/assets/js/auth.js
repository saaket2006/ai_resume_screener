import * as api from './api.js';
import * as state from './state.js';
import { ROLES } from './constants.js';

/**
 * Checks authentication status and routes appropriately based on user profile completion and role.
 */
export async function checkAuthStatus() {
    const token = state.getToken();
    const pathname = window.location.pathname;

    if (!token) {
        if (!pathname.endsWith('index.html') && pathname !== '/') {
            window.location.href = 'index.html';
        }
        return;
    }

    try {
        const user = await api.getMe();
        state.setUser(user);
        state.setOnboardingStatus(user.profile_completed);

        if (user.profile_completed === false) {
            if (!pathname.endsWith('onboarding.html')) {
                window.location.href = 'onboarding.html';
            }
            return;
        }
        
        if (user.role === ROLES.RECRUITER) {
            if (!pathname.endsWith('recruiter.html')) {
                window.location.href = 'recruiter.html';
            }
        } else if (user.role === ROLES.CANDIDATE) {
            if (!pathname.endsWith('candidate.html')) {
                window.location.href = 'candidate.html';
            }
        }
    } catch (error) {
        console.error("Auth status verification failed:", error);
        state.clearState();
        if (!pathname.endsWith('index.html') && pathname !== '/') {
            window.location.href = 'index.html';
        }
    }
}
