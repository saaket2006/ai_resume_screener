import { ROUTES } from './constants.js';
import { updateSidebarActiveLink } from './components/sidebar.js';
import { 
    initializeRecruiterDashboard, 
    initializeRecruiterScreen, 
    initializeRecruiterProfile 
} from './pages/recruiter.js';

/**
 * Handles hash-based routing for recruiter workspace views.
 * Shows/hides sections and invokes page-specific initializers.
 */
export function handleRecruiterRouting() {
    const hash = window.location.hash || ROUTES.DASHBOARD;
    
    const recViewDashboard = document.getElementById('rec-view-dashboard');
    const recViewScreen = document.getElementById('rec-view-screen');
    const recViewProfile = document.getElementById('rec-view-profile');
    const recPageTitle = document.getElementById('rec-page-title');
    
    if (!recViewDashboard || !recViewScreen || !recViewProfile || !recPageTitle) {
        return;
    }

    // Hide all recruiter sub-views
    recViewDashboard.classList.add('hidden');
    recViewScreen.classList.add('hidden');
    recViewProfile.classList.add('hidden');
    
    // Highlight the active link in the sidebar
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
 * Initializes the routing events.
 */
export function initRouter() {
    window.addEventListener('hashchange', () => {
        const recruiterContainer = document.getElementById('recruiter-container');
        if (recruiterContainer && !recruiterContainer.classList.contains('hidden')) {
            handleRecruiterRouting();
        }
    });
}
