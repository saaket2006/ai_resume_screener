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
        } else {
            const landingContainer = document.getElementById('landing-container');
            if (landingContainer) {
                landingContainer.classList.remove('hidden');
            }
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
            } else {
                const onboardingModal = document.getElementById('onboarding-modal');
                if (onboardingModal) onboardingModal.classList.remove('hidden');
            }
            return;
        }
        
        if (user.role === ROLES.RECRUITER) {
            if (!pathname.endsWith('recruiter.html')) {
                window.location.href = 'recruiter.html';
            } else {
                const recruiterContainer = document.getElementById('recruiter-container');
                if (recruiterContainer) recruiterContainer.classList.remove('hidden');
            }
        } else if (user.role === ROLES.CANDIDATE) {
            if (!pathname.endsWith('candidate.html')) {
                window.location.href = 'candidate.html';
            } else {
                const candidateContainer = document.getElementById('candidate-container');
                if (candidateContainer) candidateContainer.classList.remove('hidden');
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
