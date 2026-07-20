import {
    initHeroAnimation,
    initStoryAnimation,
    initFeatureStack,
    initWalkthrough,
    initCounters,
    initNavbarEffects
} from './animations.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize animations
    initHeroAnimation();
    initStoryAnimation();
    initFeatureStack();
    initWalkthrough();
    initCounters();
    initNavbarEffects();

    // 2. Simple Scroll Fade-In Observer for Sections
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('opacity-100', 'translate-y-0');
                entry.target.classList.remove('opacity-0', 'translate-y-8');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    // Mark sections to fade in (other than the hero/story which have custom scroll triggers)
    document.querySelectorAll('#pricing, #faq, #walkthrough h2, #walkthrough p').forEach(el => {
        el.classList.add('opacity-0', 'translate-y-8', 'transition-all', 'duration-700', 'ease-out');
        fadeObserver.observe(el);
    });

    // 3. FAQ Accordion Handler
    document.querySelectorAll('.faq-header').forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            const icon = header.querySelector('.faq-icon');
            const isHidden = content.classList.contains('hidden');
            
            // Close all others
            document.querySelectorAll('.faq-content').forEach(c => c.classList.add('hidden'));
            document.querySelectorAll('.faq-icon').forEach(i => i.textContent = '▼');

            if (isHidden) {
                content.classList.remove('hidden');
                icon.textContent = '▲';
            } else {
                content.classList.add('hidden');
                icon.textContent = '▼';
            }
        });
    });

    // 4. Auth Modal Triggers
    const authModal = document.getElementById('auth-modal');
    
    // Bind click to open auth modal to login view
    document.querySelectorAll('.nav-login-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            if (authModal) {
                authModal.classList.remove('hidden');
                const tabLogin = document.getElementById('tab-login');
                if (tabLogin) tabLogin.click();
            }
        });
    });

    // Bind click to open auth modal to signup view
    document.querySelectorAll('.nav-signup-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            if (authModal) {
                authModal.classList.remove('hidden');
                const tabSignup = document.getElementById('tab-signup');
                if (tabSignup) tabSignup.click();
            }
        });
    });

    // Close Auth Modal when clicking outside the dialog card (on the overlay itself)
    if (authModal) {
        authModal.addEventListener('click', (e) => {
            if (e.target === authModal) {
                authModal.classList.add('hidden');
            }
        });
    }

    // Close Auth Modal on Esc key press
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && authModal && !authModal.classList.contains('hidden')) {
            authModal.classList.add('hidden');
        }
    });

    // Landing Logo click soft reload handler
    const landingLogo = document.getElementById('landing-logo');
    if (landingLogo) {
        landingLogo.addEventListener('click', () => {
            // Reset simulated playground
            if (window.resetPlaygroundSimulation) {
                window.resetPlaygroundSimulation();
            }
            // Close auth modal
            if (authModal) {
                authModal.classList.add('hidden');
            }
            // Reset hash route and scroll to top smoothly
            window.location.hash = "";
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    window.resetPlaygroundSimulation = function() {
        const stateUpload = document.getElementById('play-state-upload');
        const stateLoading = document.getElementById('play-state-loading');
        const stateResult = document.getElementById('play-state-result');
        
        if (!stateUpload || !stateLoading || !stateResult) return;

        stateResult.classList.add('hidden');
        stateLoading.classList.add('hidden');
        stateUpload.classList.remove('hidden');
    };
});
