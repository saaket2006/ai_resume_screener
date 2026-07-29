import * as api from './api.js';
import * as state from './state.js';
import { ROLES } from './constants.js';
import { showOnboardingWizard } from './pages/onboarding.js';
import { handleRouting } from './router.js';

/**
 * Checks authentication status and routes appropriately based on user profile completion and role.
 */
export async function checkAuthStatus() {
    const authModal = document.getElementById('auth-modal');
    const appContainer = document.getElementById('app-container');
    const onboardingModal = document.getElementById('onboarding-modal');
    const recruiterContainer = document.getElementById('recruiter-container');
    const candidateContainer = document.getElementById('candidate-container');
    const userDisplayNameElem = document.getElementById('user-display-name');

    const token = state.getToken();
    const landingContainer = document.getElementById('landing-container');

    if (!token) {
        if (landingContainer) landingContainer.classList.remove('hidden');
        authModal.classList.add('hidden');
        appContainer.classList.add('hidden');
        onboardingModal.classList.add('hidden');
        recruiterContainer.classList.add('hidden');
        candidateContainer.classList.add('hidden');
        // Handle unauthenticated hash routes (#/login, #/signup)
        handleRouting();
        return;
    }

    try {
        const user = await api.getMe();
        state.setUser(user);
        state.setOnboardingStatus(user.profile_completed);

        if (user.profile_completed === false) {
            if (landingContainer) landingContainer.classList.add('hidden');
            showOnboardingWizard();
            return;
        }

        if (landingContainer) landingContainer.classList.add('hidden');
        authModal.classList.add('hidden');
        onboardingModal.classList.add('hidden');
        
        if (user.role === ROLES.RECRUITER) {
            appContainer.classList.add('hidden');
            candidateContainer.classList.add('hidden');
            recruiterContainer.classList.remove('hidden');
            handleRouting();
        } else if (user.role === ROLES.CANDIDATE) {
            appContainer.classList.add('hidden');
            recruiterContainer.classList.add('hidden');
            candidateContainer.classList.remove('hidden');
            handleRouting();
        } else {
            // UNASSIGNED or other (redirect to legacy or fallback)
            recruiterContainer.classList.add('hidden');
            candidateContainer.classList.add('hidden');
            appContainer.classList.remove('hidden');
            userDisplayNameElem.textContent = user.email.split('@')[0];
        }
    } catch (error) {
        console.error("Auth status verification failed:", error);
        state.clearState();
        if (landingContainer) landingContainer.classList.remove('hidden');
        authModal.classList.add('hidden');
        appContainer.classList.add('hidden');
        onboardingModal.classList.add('hidden');
        recruiterContainer.classList.add('hidden');
        candidateContainer.classList.add('hidden');
    }
}
