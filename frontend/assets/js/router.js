import { ROUTES, ROLES } from './constants.js';
import * as state from './state.js';
import { updateSidebarActiveLink } from './components/sidebar.js';
import { 
    initializeRecruiterDashboard, 
    initializeRecruiterScreen, 
    initializeRecruiterProfile 
} from './pages/recruiter.js';
import {
    initializeCandidateDashboard,
    initializeCandidateScreen,
    initializeCandidateProfile
} from './pages/candidate.js';

/**
 * Handles recruiter workspace routing sub-views.
 */
export function handleRecruiterRouting(hash) {
    const recViewDashboard = document.getElementById('rec-view-dashboard');
    const recViewScreen = document.getElementById('rec-view-screen');
    const recViewProfile = document.getElementById('rec-view-profile');
    const recPageTitle = document.getElementById('rec-page-title');
    
    if (!recViewDashboard || !recViewScreen || !recViewProfile || !recPageTitle) {
        return;
    }

    recViewDashboard.classList.add('hidden');
    recViewScreen.classList.add('hidden');
    recViewProfile.classList.add('hidden');
    
    updateSidebarActiveLink(hash);
    
    if (hash === ROUTES.DASHBOARD) {
        recViewDashboard.classList.remove('hidden');
        recPageTitle.textContent = "Dashboard";
        initializeRecruiterDashboard();
    } else if (hash === ROUTES.SCREEN) {
        recViewScreen.classList.remove('hidden');
        recPageTitle.textContent = "Resume Screening";
        initializeRecruiterScreen();
    } else if (hash === ROUTES.PROFILE) {
        recViewProfile.classList.remove('hidden');
        recPageTitle.textContent = "My Profile";
        initializeRecruiterProfile();
    }
}

/**
 * Handles candidate workspace routing sub-views.
 */
export function handleCandidateRouting(hash) {
    const candViewDashboard = document.getElementById('cand-view-dashboard');
    const candViewScreen = document.getElementById('cand-view-screen');
    const candViewProfile = document.getElementById('cand-view-profile');
    const candPageTitle = document.getElementById('cand-page-title');

    if (!candViewDashboard || !candViewScreen || !candViewProfile || !candPageTitle) {
        return;
    }

    candViewDashboard.classList.add('hidden');
    candViewScreen.classList.add('hidden');
    candViewProfile.classList.add('hidden');

    updateSidebarActiveLink(hash);

    if (hash === ROUTES.CANDIDATE_DASHBOARD) {
        candViewDashboard.classList.remove('hidden');
        candPageTitle.textContent = "Dashboard";
        initializeCandidateDashboard();
    } else if (hash === ROUTES.CANDIDATE_SCREEN) {
        candViewScreen.classList.remove('hidden');
        candPageTitle.textContent = "Resume Analysis";
        initializeCandidateScreen();
    } else if (hash === ROUTES.CANDIDATE_PROFILE) {
        candViewProfile.classList.remove('hidden');
        candPageTitle.textContent = "My Profile";
        initializeCandidateProfile();
    }
}

/**
 * Central routing router entry point. Enforces role-based route access limits.
 */
export function handleRouting() {
    const user = state.getUser();
    const hash = window.location.hash;
    const pathname = window.location.pathname;

    if (!user) {
        if (hash === ROUTES.LOGIN || hash === ROUTES.SIGNUP) {
            const authModal = document.getElementById('auth-modal');
            if (authModal) {
                authModal.classList.remove('hidden');
                const tabId = hash === ROUTES.LOGIN ? 'tab-login' : 'tab-signup';
                const tabBtn = document.getElementById(tabId);
                if (tabBtn) tabBtn.click();
            }
        }
        return;
    }

    if (pathname.endsWith('recruiter.html')) {
        const currentHash = hash || ROUTES.DASHBOARD;
        if (currentHash.startsWith("#/candidate")) {
            window.location.hash = ROUTES.DASHBOARD;
            return;
        }
        handleRecruiterRouting(currentHash);
    } else if (pathname.endsWith('candidate.html')) {
        const currentHash = hash || ROUTES.CANDIDATE_DASHBOARD;
        if (currentHash.startsWith("#/recruiter")) {
            window.location.hash = ROUTES.CANDIDATE_DASHBOARD;
            return;
        }
        handleCandidateRouting(currentHash);
    }
}

/**
 * Registers hashchange routing event triggers.
 */
export function initRouter() {
    window.addEventListener('hashchange', () => {
        handleRouting();
    });
}
