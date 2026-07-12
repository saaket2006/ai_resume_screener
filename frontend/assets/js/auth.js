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
    if (!token) {
        authModal.classList.remove('hidden');
        appContainer.classList.add('hidden');
        onboardingModal.classList.add('hidden');
        recruiterContainer.classList.add('hidden');
        candidateContainer.classList.add('hidden');
        return;
    }

    try {
        const user = await api.getMe();
        state.setUser(user);
        state.setOnboardingStatus(user.profile_completed);

        if (user.profile_completed === false) {
            showOnboardingWizard();
            return;
        }

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
        authModal.classList.remove('hidden');
        appContainer.classList.add('hidden');
        onboardingModal.classList.add('hidden');
        recruiterContainer.classList.add('hidden');
        candidateContainer.classList.add('hidden');
    }
}
