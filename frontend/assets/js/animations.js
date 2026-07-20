/* GSAP Scroll Animations & Timelines Module */

export function initHeroAnimation() {
    // 1. Title fade, blur, and slide up letter by letter
    const headline = document.querySelector('.hero-headline');
    if (headline) {
        // Trim and normalize whitespace
        const text = headline.textContent.trim().replace(/\s+/g, ' ');
        // Split by words, wrap each word in its own inline span so that
        // the browser can still word-wrap between words naturally.
        const words = text.split(' ');
        headline.innerHTML = words.map(word => {
            const letters = word.split('').map(char =>
                `<span class="hero-letter" style="display:inline-block; opacity:0; filter:blur(10px); transform:translateY(20px);">${char}</span>`
            ).join('');
            return `<span style="display:inline-block; white-space:nowrap;">${letters}</span>`;
        }).join(' ');

        gsap.to('.hero-letter', {
            opacity: 1,
            filter: 'blur(0px)',
            y: 0,
            duration: 0.8,
            stagger: 0.03,
            ease: 'power3.out',
            onComplete: () => {
                // Return to normal flow so responsiveness isn't affected
                headline.querySelectorAll('span').forEach(s => {
                    s.style.display = '';
                    s.style.filter = '';
                    s.style.transform = '';
                    s.style.whiteSpace = '';
                });
            }
        });
    }

    // 2. Terminal typewriter
    const terminalText = document.querySelector('.terminal-typewriter');
    if (terminalText) {
        const text = terminalText.textContent;
        terminalText.textContent = '';
        let i = 0;
        function type() {
            if (i < text.length) {
                terminalText.textContent += text.charAt(i);
                i++;
                setTimeout(type, 45);
            }
        }
        type();
    }

    // 3. Parallax mouse move for hero mockup
    const heroMockup = document.querySelector('.hero-mockup-wrapper');
    if (heroMockup) {
        document.addEventListener('mousemove', (e) => {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 45;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 45;
            gsap.to(heroMockup, {
                rotationY: xAxis,
                rotationX: -yAxis,
                ease: 'power2.out',
                duration: 0.5
            });
        });
        
        document.addEventListener('mouseleave', () => {
            gsap.to(heroMockup, {
                rotationY: 0,
                rotationX: 0,
                ease: 'power2.out',
                duration: 0.8
            });
        });
    }

    // 4. Floating badges animation
    gsap.to('.floating-badge-1', { y: -12, duration: 2.2, repeat: -1, yoyo: true, ease: 'sine.inOut' });
    gsap.to('.floating-badge-2', { y: 12, duration: 2.6, repeat: -1, yoyo: true, ease: 'sine.inOut', delay: 0.3 });
    gsap.to('.floating-badge-3', { y: -8, duration: 2.0, repeat: -1, yoyo: true, ease: 'sine.inOut', delay: 0.6 });
}

export function initStoryAnimation() {
    const storyElements = gsap.utils.toArray('.story-element');
    if (storyElements.length === 0) return;

    storyElements.forEach((el) => {
        gsap.fromTo(el, 
            { opacity: 0.1, y: 30, scale: 0.95 },
            { 
                opacity: 1, 
                y: 0, 
                scale: 1,
                scrollTrigger: {
                    trigger: el,
                    start: 'top 80%',
                    end: 'top 50%',
                    scrub: true,
                    toggleActions: 'play reverse play reverse'
                }
            }
        );
    });
}

export function initFeatureStack() {
    const cards = gsap.utils.toArray('.feature-card-wrapper');
    if (cards.length === 0) return;

    cards.forEach((card, index) => {
        if (index === cards.length - 1) return;

        gsap.to(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 120px',
                end: 'bottom 100px',
                scrub: true,
                pin: false
            },
            scale: 0.92,
            opacity: 0.6,
            filter: 'blur(3px)',
            ease: 'none'
        });
    });
}

export function initWalkthrough() {
    const walkthroughSection = document.getElementById('walkthrough');
    if (!walkthroughSection) return;

    const blocks = document.querySelectorAll('.walkthrough-text-block');
    if (blocks.length === 0) return;

    let activeIndex = 0;
    const totalSteps = blocks.length;
    let isTransitioning = false;

    function activateStep(index) {
        if (index < 0 || index >= totalSteps) return;
        activeIndex = index;

        blocks.forEach((block, idx) => {
            const visualId = block.getAttribute('data-visual-target');
            const visualEl = document.getElementById(visualId);

            if (idx === index) {
                block.classList.add('border-emerald-500');
                block.classList.remove('border-slate-800');
                if (visualEl) {
                    gsap.to(visualEl, { opacity: 1, scale: 1, duration: 0.4 });
                }
            } else {
                block.classList.remove('border-emerald-500');
                block.classList.add('border-slate-800');
                if (visualEl) {
                    gsap.to(visualEl, { opacity: 0, scale: 0.95, duration: 0.3 });
                }
            }
        });
    }

    // Set initial state
    activateStep(0);

    // Bind click trigger
    blocks.forEach((block, idx) => {
        block.addEventListener('click', () => {
            activateStep(idx);
        });
    });

    // Intercept mouse wheel events to cycle walkthrough steps before scrolling the viewport
    walkthroughSection.addEventListener('wheel', (e) => {
        if (window.innerWidth < 1024) return; // only hijack scroll on desktop sizes

        // If scrolling down and we have next steps
        if (e.deltaY > 0 && activeIndex < totalSteps - 1) {
            e.preventDefault();
            if (!isTransitioning) {
                isTransitioning = true;
                activateStep(activeIndex + 1);
                setTimeout(() => { isTransitioning = false; }, 600);
            }
        }
        // If scrolling up and we have previous steps
        else if (e.deltaY < 0 && activeIndex > 0) {
            e.preventDefault();
            if (!isTransitioning) {
                isTransitioning = true;
                activateStep(activeIndex - 1);
                setTimeout(() => { isTransitioning = false; }, 600);
            }
        }
    }, { passive: false });
}

export function initCounters() {
    const counters = document.querySelectorAll('.stat-counter');
    if (counters.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const value = parseInt(target.getAttribute('data-value'));
                const duration = 2000;
                let start = 0;
                const timer = setInterval(() => {
                    start += Math.ceil(value / 40);
                    if (start >= value) {
                        target.textContent = value.toLocaleString();
                        clearInterval(timer);
                    } else {
                        target.textContent = start.toLocaleString();
                    }
                }, 30);
                observer.unobserve(target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

export function initNavbarEffects() {
    const navbar = document.getElementById('navbar-landing');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('backdrop-blur-md', 'bg-[#070a13]/85', 'border-b', 'py-3');
            navbar.classList.remove('py-5', 'bg-transparent');
        } else {
            navbar.classList.remove('backdrop-blur-md', 'bg-[#070a13]/85', 'border-b', 'py-3');
            navbar.classList.add('py-5', 'bg-transparent');
        }
    });
}
