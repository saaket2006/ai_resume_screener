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
            document.querySelectorAll('.faq-icon').forEach(i => i.textContent = '\u25BC');

            if (isHidden) {
                content.classList.remove('hidden');
                icon.textContent = '\u25B2';
            } else {
                content.classList.add('hidden');
                icon.textContent = '\u25BC';
            }
        });
    });

    // 4. Auth Modal Triggers
    const authModal = document.getElementById('auth-modal');
    
    // Bind click to open auth modal for get started/sign in buttons
    document.querySelectorAll('.nav-login-btn, .nav-signup-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const isLogin = btn.classList.contains('nav-login-btn');
            window.location.hash = isLogin ? '#/login' : '#/signup';
            // Fallback in case hash doesn't trigger change
            if (authModal) {
                authModal.classList.remove('hidden');
                const tabId = isLogin ? 'tab-login' : 'tab-signup';
                const tabBtn = document.getElementById(tabId);
                if (tabBtn) tabBtn.click();
            }
        });
    });

    // 5. Interactive Demo Simulation
    window.runSimulatedPlayground = function() {
        const stateUpload = document.getElementById('play-state-upload');
        const stateLoading = document.getElementById('play-state-loading');
        const stateResult = document.getElementById('play-state-result');
        const loadingBar = document.getElementById('play-loading-bar');
        const loadingText = document.getElementById('play-loading-text');

        if (!stateUpload || !stateLoading || !stateResult) return;

        stateUpload.classList.add('hidden');
        stateLoading.classList.remove('hidden');

        // Progress animation step-by-step
        let progress = 0;
        loadingBar.style.width = '0%';
        loadingText.textContent = "Parsing PDF layout...";

        const interval = setInterval(() => {
            progress += 10;
            loadingBar.style.width = `${progress}%`;

            if (progress === 30) {
                loadingText.textContent = "Extracting skill entities...";
            } else if (progress === 60) {
                loadingText.textContent = "Running semantic JD match...";
            } else if (progress === 90) {
                loadingText.textContent = "Generating explainable scoring report...";
            } else if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    stateLoading.classList.add('hidden');
                    stateResult.classList.remove('hidden');
                }, 500);
            }
        }, 250);
    };

    window.resetPlaygroundSimulation = function() {
        const stateUpload = document.getElementById('play-state-upload');
        const stateLoading = document.getElementById('play-state-loading');
        const stateResult = document.getElementById('play-state-result');
        
        if (!stateUpload || !stateLoading || !stateResult) return;

        stateResult.classList.add('hidden');
        stateLoading.classList.add('hidden');
        stateUpload.classList.remove('hidden');
    };

    // Bind triggers to demo UI
    const playBtn = document.getElementById('playground-btn-upload');
    if (playBtn) {
        playBtn.addEventListener('click', window.runSimulatedPlayground);
    }
    const resetBtn = document.getElementById('playground-btn-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', window.resetPlaygroundSimulation);
    }
});
