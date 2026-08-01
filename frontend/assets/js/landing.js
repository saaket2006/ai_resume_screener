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

});
