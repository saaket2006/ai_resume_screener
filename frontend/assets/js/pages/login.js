import * as api from '../api.js';
import * as state from '../state.js';
import { checkAuthStatus } from '../auth.js';
import { showError } from '../utils.js';

let initialized = false;

/**
 * Binds event listeners for the Login page (runs once on startup).
 */
export function initLoginPage() {
    if (initialized) return;

    const tabLogin = document.getElementById('tab-login');
    const tabSignup = document.getElementById('tab-signup');
    const loginPlane = document.getElementById('login-plane');
    const signupPlane = document.getElementById('signup-plane');
    const authErrorMsg = document.getElementById('auth-error');

    const loginForm = document.getElementById('login-form');
    const loginEmailInput = document.getElementById('login-email');
    const loginPasswordInput = document.getElementById('login-password');
    const emailLoginBtn = document.getElementById('email-login-btn');

    // Tab Switching Logic
    tabLogin.addEventListener('click', () => {
        tabLogin.classList.add('active');
        tabSignup.classList.remove('active');
        loginPlane.classList.remove('hidden');
        loginPlane.classList.add('active-plane');
        signupPlane.classList.add('hidden');
        signupPlane.classList.remove('active-plane');
        authErrorMsg.classList.add('hidden');
    });

    tabSignup.addEventListener('click', () => {
        tabSignup.classList.add('active');
        tabLogin.classList.remove('active');
        signupPlane.classList.remove('hidden');
        signupPlane.classList.add('active-plane');
        loginPlane.classList.add('hidden');
        loginPlane.classList.remove('active-plane');
        authErrorMsg.classList.add('hidden');
    });

    // Toggle Password Visibility
    const toggleBtns = document.querySelectorAll('.toggle-password-btn');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const inputElement = document.getElementById(targetId);
            const iconElement = btn.querySelector('span');

            const type = inputElement.getAttribute('type') === 'password' ? 'text' : 'password';
            inputElement.setAttribute('type', type);
            iconElement.textContent = type === 'password' ? '\uD83D\uDC41\uFE0F' : '\uD83D\uDE48';
        });
    });

    // Clear Password Text
    const clearBtns = document.querySelectorAll('.clear-password-btn');
    clearBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const inputElement = document.getElementById(targetId);
            inputElement.value = '';
            inputElement.focus();

            if (targetId === 'signup-password') {
                const event = new Event('input', { bubbles: true });
                inputElement.dispatchEvent(event);
            }
        });
    });

    // Login Submit
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = loginEmailInput.value.trim();
        const password = loginPasswordInput.value;
        const btnText = emailLoginBtn.querySelector('span');

        btnText.textContent = "Signing in...";
        emailLoginBtn.disabled = true;
        authErrorMsg.classList.add('hidden');

        try {
            const data = await api.login(email, password);
            state.setToken(data.access_token);
            loginForm.reset();
            await checkAuthStatus();
        } catch (error) {
            showError(authErrorMsg, "Login failed: " + error.message);
            emailLoginBtn.disabled = false;
        } finally {
            btnText.textContent = "Sign In";
        }
    });

    initialized = true;
}

/**
 * Initializes/resets the Login page view state.
 */
export function initializeLoginPage() {
    const authErrorMsg = document.getElementById('auth-error');
    if (authErrorMsg) authErrorMsg.classList.add('hidden');

    const tabLogin = document.getElementById('tab-login');
    if (tabLogin) tabLogin.click(); // Default to login tab
}
