import {
    initHeroAnimation,
    initStoryAnimation,
    initFeatureStack,
    initWalkthrough,
    initCounters,
    initNavbarEffects
} from './animations.js';

document.addEventListener('DOMContentLoaded', () => {
    const pathname = window.location.pathname;
    if (pathname.endsWith('index.html') || pathname === '/') {
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
                    entry.target.classList.add('visible');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        const fadeElements = document.querySelectorAll('.fade-in-section');
        fadeElements.forEach(el => fadeObserver.observe(el));

        // 3. Interactive Walkthrough/Mockup logic
        const analyzeBtn = document.getElementById('mock-analyze-btn');
        const progressBar = document.getElementById('mock-progress');
        const badgeScore = document.getElementById('mock-badge-score');
        const analysisGrid = document.querySelector('.analysis-grid');

        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => {
                analyzeBtn.textContent = 'Analyzing...';
                progressBar.style.width = '0%';

                // Simulate progressive loading
                let progress = 0;
                const interval = setInterval(() => {
                    progress += 10;
                    progressBar.style.width = `${progress}%`;
                    if (progress >= 100) {
                        clearInterval(interval);
                        analyzeBtn.textContent = 'Analysis Complete';
                        analyzeBtn.classList.add('opacity-50');
                        analyzeBtn.disabled = true;

                        // Show mock analysis grid
                        if (analysisGrid) {
                            analysisGrid.classList.remove('hidden');
                        }

                        // Animate score increment
                        let score = 0;
                        const scoreInterval = setInterval(() => {
                            score += 1;
                            badgeScore.textContent = `${score}%`;
                            if (score >= 94) {
                                clearInterval(scoreInterval);
                            }
                        }, 20);
                    }
                }, 150);
            });
        }

        // 4. Hero Card Mouse Move Tilt Effect
        const heroCard = document.querySelector('.hero-mockup');
        if (heroCard) {
            document.addEventListener('mousemove', (e) => {
                // Check if device supports hover (not a touch screen)
                if (window.matchMedia("(hover: none)").matches) return;

                const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
                const yAxis = (window.innerHeight / 2 - e.pageY) / 50;
                heroCard.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
            });

            // Reset position on mouse leave body
            document.addEventListener('mouseleave', () => {
                heroCard.style.transform = `rotateY(0deg) rotateX(0deg)`;
            });
        }

        // 5. FAQ Accordion Logic
        const faqItems = document.querySelectorAll('.faq-item');
        faqItems.forEach(item => {
            const button = item.querySelector('button');
            const answer = item.querySelector('.faq-answer');
            const icon = item.querySelector('.faq-icon');

            button.addEventListener('click', () => {
                const isOpen = item.classList.contains('active');

                // Close all other FAQs
                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                    const otherAnswer = otherItem.querySelector('.faq-answer');
                    const otherIcon = otherItem.querySelector('.faq-icon');
                    otherAnswer.style.maxHeight = '0px';
                    otherAnswer.style.opacity = '0';
                    otherIcon.style.transform = 'rotate(0deg)';
                });

                // Toggle current FAQ
                if (!isOpen) {
                    item.classList.add('active');
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    answer.style.opacity = '1';
                    icon.style.transform = 'rotate(45deg)';
                }
            });
        });
    }
});
