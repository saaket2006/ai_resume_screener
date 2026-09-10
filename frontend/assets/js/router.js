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
import {
    showForgotPasswordView,
    showResetPasswordView,
    resetAuthModalToTabs
} from './pages/login.js';

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
 * Parses a hash string into its route path and URLSearchParams query parameters.
 * Conceptually: '#/reset-password?token=abc123' -> { route: '#/reset-password', params: URLSearchParams }
 */
export function parseHash(hash = window.location.hash) {
    if (!hash) return { route: '', params: new URLSearchParams() };
    const [routePart, queryPart] = hash.split('?');
    return {
        route: routePart || '',
        params: new URLSearchParams(queryPart || '')
    };
}

/**
 * Central routing router entry point. Enforces role-based route access limits.
 */
export function handleRouting() {
    const user = state.getUser();
    const { route, params } = parseHash(window.location.hash);
    const pathname = window.location.pathname.toLowerCase();

    // 1. Password Reset: #/reset-password?token=<TOKEN>
    if (route === ROUTES.RESET_PASSWORD) {
        const authModal = document.getElementById('auth-modal');
        if (authModal) {
            authModal.classList.remove('hidden');
            const token = params.get('token') || '';
            showResetPasswordView(token);
        }
        return;
    }

    // 2. Forgot Password: #/forgot-password
    if (route === ROUTES.FORGOT_PASSWORD) {
        const authModal = document.getElementById('auth-modal');
        if (authModal) {
            authModal.classList.remove('hidden');
            showForgotPasswordView();
        }
        return;
    }

    // 3. Unauthenticated User Routes (Login / Sign Up)
    if (!user) {
        if (route === ROUTES.LOGIN || route === ROUTES.SIGNUP) {
            const authModal = document.getElementById('auth-modal');
            if (authModal) {
                authModal.classList.remove('hidden');
                resetAuthModalToTabs();
                const isLogin = route === ROUTES.LOGIN;
                const tabLogin = document.getElementById('tab-login');
                const tabSignup = document.getElementById('tab-signup');
                const loginPlane = document.getElementById('login-plane');
                const signupPlane = document.getElementById('signup-plane');
                if (tabLogin) tabLogin.classList.toggle('active', isLogin);
                if (tabSignup) tabSignup.classList.toggle('active', !isLogin);
                if (loginPlane) {
                    loginPlane.classList.toggle('hidden', !isLogin);
                    loginPlane.classList.toggle('active-plane', isLogin);
                }
                if (signupPlane) {
                    signupPlane.classList.toggle('hidden', isLogin);
                    signupPlane.classList.toggle('active-plane', !isLogin);
                }
            }
        }
        return;
    }

    // 4. Authenticated Workspace Routes
    if (pathname.includes('recruiter')) {
        const currentHash = route || ROUTES.DASHBOARD;
        if (currentHash.startsWith("#/candidate")) {
            window.location.hash = ROUTES.DASHBOARD;
            return;
        }
        handleRecruiterRouting(currentHash);
    } else if (pathname.includes('candidate')) {
        const currentHash = route || ROUTES.CANDIDATE_DASHBOARD;
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
