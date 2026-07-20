import * as state from '../state.js';
import { clearRecruiterWorkspaceState } from '../pages/recruiter.js';
import { clearCandidateWorkspaceState } from '../pages/candidate.js';
import { ROUTES } from '../constants.js';

/**
 * Initializes the profile nav drop-down controls and logs.
 * @param {Function} clearCandidateStateCallback - Callback to clear candidate view variables
 */
export function initNavbar(clearCandidateStateCallback) {
    const userProfileDropdown = document.getElementById('user-profile-dropdown');
    const userTrigger = document.getElementById('user-trigger');
    const signOutBtn = document.getElementById('sign-out-btn');
    const recSignOutBtn = document.getElementById('rec-sign-out-btn');
    const candSignOutBtn = document.getElementById('cand-sign-out-btn');

    const authModal = document.getElementById('auth-modal');
    const appContainer = document.getElementById('app-container');
    const onboardingModal = document.getElementById('onboarding-modal');
    const recruiterContainer = document.getElementById('recruiter-container');
    const candidateContainer = document.getElementById('candidate-container');

    // Profile Dropdown Trigger Handlers
    if (userTrigger && userProfileDropdown) {
        userTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            userProfileDropdown.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!userProfileDropdown.contains(e.target)) {
                userProfileDropdown.classList.remove('active');
            }
        });
    }

    // Candidate Legacy View Sign Out Handler
    if (signOutBtn) {
        signOutBtn.addEventListener('click', () => {
            state.clearState();
            authModal.classList.remove('hidden');
            appContainer.classList.add('hidden');
            onboardingModal.classList.add('hidden');
            
            if (clearCandidateStateCallback) {
                clearCandidateStateCallback();
            }
            
            const tabLogin = document.getElementById('tab-login');
            if (tabLogin) tabLogin.click();
        });
    }

    // Recruiter workspace sign out link
    if (recSignOutBtn) {
        recSignOutBtn.addEventListener('click', () => {
            state.clearState();
            recruiterContainer.classList.add('hidden');
            authModal.classList.remove('hidden');
            onboardingModal.classList.add('hidden');
            appContainer.classList.add('hidden');
            
            clearRecruiterWorkspaceState();
            
            window.location.hash = ROUTES.LOGIN;
        });
    }

    // Candidate workspace sign out link
    if (candSignOutBtn) {
        candSignOutBtn.addEventListener('click', () => {
            state.clearState();
            candidateContainer.classList.add('hidden');
            authModal.classList.remove('hidden');
            onboardingModal.classList.add('hidden');
            appContainer.classList.add('hidden');
            
            clearCandidateWorkspaceState();
            
            window.location.hash = ROUTES.LOGIN;
        });
    }

    // Sidebar Logo: navigate back to landing page
    const landingContainer = document.getElementById('landing-container');

    const recSidebarLogo = document.getElementById('recruiter-sidebar-logo');
    if (recSidebarLogo) {
        recSidebarLogo.addEventListener('click', () => {
            state.clearState();
            recruiterContainer.classList.add('hidden');
            authModal.classList.add('hidden');
            onboardingModal.classList.add('hidden');
            appContainer.classList.add('hidden');
            if (landingContainer) landingContainer.classList.remove('hidden');
            clearRecruiterWorkspaceState();
            window.location.hash = '';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    const candSidebarLogo = document.getElementById('candidate-sidebar-logo');
    if (candSidebarLogo) {
        candSidebarLogo.addEventListener('click', () => {
            state.clearState();
            candidateContainer.classList.add('hidden');
            authModal.classList.add('hidden');
            onboardingModal.classList.add('hidden');
            appContainer.classList.add('hidden');
            if (landingContainer) landingContainer.classList.remove('hidden');
            clearCandidateWorkspaceState();
            window.location.hash = '';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}
