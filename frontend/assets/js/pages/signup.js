import * as api from '../api.js';
import * as state from '../state.js';
import { checkAuthStatus } from '../auth.js';
import { showError, validatePassword } from '../utils.js';

let initialized = false;

/**
 * Binds event listeners for the Sign Up page (runs once on startup).
 */
export function initSignupPage() {
    if (initialized) return;

    const signupForm = document.getElementById('signup-form');
    const signupEmailInput = document.getElementById('signup-email');
    const signupPasswordInput = document.getElementById('signup-password');
    const emailSignupBtn = document.getElementById('email-signup-btn');
    const authErrorMsg = document.getElementById('auth-error');

    const passwordConstraints = {
        length: document.getElementById('constraint-length'),
        number: document.getElementById('constraint-number'),
        special: document.getElementById('constraint-special')
    };

    // Password Validation Real-time
    signupPasswordInput.addEventListener('input', () => {
        validatePassword(signupPasswordInput.value, passwordConstraints);
    });

    // Signup Submit
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = signupEmailInput.value.trim();
        const password = signupPasswordInput.value;

        if (!validatePassword(password, passwordConstraints)) {
            showError(authErrorMsg, "Please meet all password requirements.");
            return;
        }

        const btnText = emailSignupBtn.querySelector('span');
        btnText.textContent = "Creating Account...";
        emailSignupBtn.disabled = true;
        authErrorMsg.classList.add('hidden');

        try {
            await api.signup(email, password);

            // Auto-login on successful registration
            const data = await api.login(email, password);
            state.setToken(data.access_token);
            signupForm.reset();
            Object.values(passwordConstraints).forEach(c => { if (c) c.className = ''; });
            await checkAuthStatus();
        } catch (error) {
            showError(authErrorMsg, "Sign Up failed: " + error.message);
            emailSignupBtn.disabled = false;
        } finally {
            btnText.textContent = "Sign Up";
        }
    });

    initialized = true;
}

/**
 * Initializes/resets the Sign Up page view state.
 */
export function initializeSignupPage() {
    const signupForm = document.getElementById('signup-form');
    if (signupForm) signupForm.reset();

    const passwordConstraints = {
        length: document.getElementById('constraint-length'),
        number: document.getElementById('constraint-number'),
        special: document.getElementById('constraint-special')
    };

    Object.values(passwordConstraints).forEach(c => {
        if (c) c.className = '';
    });
}
