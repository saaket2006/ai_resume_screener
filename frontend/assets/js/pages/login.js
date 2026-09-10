import * as api from '../api.js';
import * as state from '../state.js';
import { checkAuthStatus } from '../auth.js';
import { showError, hideError, validatePassword } from '../utils.js';
import { MESSAGES } from '../constants.js';
import { signInWithPopup } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";
import { auth, googleProvider } from '../firebase-init.js?v=5';

let initialized = false;

/**
 * Switches the auth card to standard Login / Sign Up view.
 */
export function resetAuthModalToTabs() {
    const tabsContainer = document.getElementById('auth-tabs-container');
    const divider = document.getElementById('auth-modal-divider');
    const googleBtn = document.getElementById('google-login-btn');
    const forgotPlane = document.getElementById('forgot-password-plane');
    const resetPlane = document.getElementById('reset-password-plane');
    const authErrorMsg = document.getElementById('auth-error');

    if (tabsContainer) tabsContainer.classList.remove('hidden');
    if (divider) divider.classList.remove('hidden');
    if (googleBtn) googleBtn.classList.remove('hidden');
    if (forgotPlane) forgotPlane.classList.add('hidden');
    if (resetPlane) resetPlane.classList.add('hidden');
    if (authErrorMsg) hideError(authErrorMsg);
}

/**
 * Shows the Forgot Password view inside the Auth Modal.
 */
export function showForgotPasswordView() {
    const tabsContainer = document.getElementById('auth-tabs-container');
    const divider = document.getElementById('auth-modal-divider');
    const googleBtn = document.getElementById('google-login-btn');
    const loginPlane = document.getElementById('login-plane');
    const signupPlane = document.getElementById('signup-plane');
    const forgotPlane = document.getElementById('forgot-password-plane');
    const resetPlane = document.getElementById('reset-password-plane');
    const authErrorMsg = document.getElementById('auth-error');
    const forgotFeedback = document.getElementById('forgot-password-feedback');
    const forgotEmailInput = document.getElementById('forgot-email');

    if (tabsContainer) tabsContainer.classList.add('hidden');
    if (divider) divider.classList.add('hidden');
    if (googleBtn) googleBtn.classList.add('hidden');
    if (loginPlane) loginPlane.classList.add('hidden');
    if (signupPlane) signupPlane.classList.add('hidden');
    if (resetPlane) resetPlane.classList.add('hidden');

    if (forgotPlane) {
        forgotPlane.classList.remove('hidden');
        forgotPlane.classList.add('active-plane');
    }
    if (authErrorMsg) hideError(authErrorMsg);
    if (forgotFeedback) {
        forgotFeedback.classList.add('hidden');
        forgotFeedback.textContent = '';
    }
    if (forgotEmailInput) {
        forgotEmailInput.value = '';
        setTimeout(() => forgotEmailInput.focus(), 100);
    }
}

/**
 * Shows the Reset Password view inside the Auth Modal.
 */
export function showResetPasswordView(token = "") {
    const tabsContainer = document.getElementById('auth-tabs-container');
    const divider = document.getElementById('auth-modal-divider');
    const googleBtn = document.getElementById('google-login-btn');
    const loginPlane = document.getElementById('login-plane');
    const signupPlane = document.getElementById('signup-plane');
    const forgotPlane = document.getElementById('forgot-password-plane');
    const resetPlane = document.getElementById('reset-password-plane');
    const authErrorMsg = document.getElementById('auth-error');
    const resetFeedback = document.getElementById('reset-password-feedback');
    const resetTokenInput = document.getElementById('reset-token-input');
    const resetSubmitBtn = document.getElementById('reset-submit-btn');

    if (tabsContainer) tabsContainer.classList.add('hidden');
    if (divider) divider.classList.add('hidden');
    if (googleBtn) googleBtn.classList.add('hidden');
    if (loginPlane) loginPlane.classList.add('hidden');
    if (signupPlane) signupPlane.classList.add('hidden');
    if (forgotPlane) forgotPlane.classList.add('hidden');

    if (resetPlane) {
        resetPlane.classList.remove('hidden');
        resetPlane.classList.add('active-plane');
    }
    if (authErrorMsg) hideError(authErrorMsg);
    if (resetFeedback) {
        resetFeedback.classList.add('hidden');
        resetFeedback.textContent = '';
    }
    if (resetTokenInput) {
        resetTokenInput.value = token || "";
    }

    if (!token) {
        if (authErrorMsg) showError(authErrorMsg, "Invalid or missing reset token. Please request a new password reset link.");
        if (resetSubmitBtn) resetSubmitBtn.disabled = true;
    } else if (resetSubmitBtn) {
        resetSubmitBtn.disabled = false;
    }
}

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
        resetAuthModalToTabs();
        tabLogin.classList.add('active');
        tabSignup.classList.remove('active');
        loginPlane.classList.remove('hidden');
        loginPlane.classList.add('active-plane');
        signupPlane.classList.add('hidden');
        signupPlane.classList.remove('active-plane');
        authErrorMsg.classList.add('hidden');
        window.location.hash = '#/login';
    });

    tabSignup.addEventListener('click', () => {
        resetAuthModalToTabs();
        tabSignup.classList.add('active');
        tabLogin.classList.remove('active');
        signupPlane.classList.remove('hidden');
        signupPlane.classList.add('active-plane');
        loginPlane.classList.add('hidden');
        loginPlane.classList.remove('active-plane');
        authErrorMsg.classList.add('hidden');
        window.location.hash = '#/signup';
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

            if (targetId === 'signup-password' || targetId === 'reset-new-password') {
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

    // Forgot Password Form Handling
    const forgotForm = document.getElementById('forgot-password-form');
    const forgotEmailInput = document.getElementById('forgot-email');
    const forgotSubmitBtn = document.getElementById('forgot-submit-btn');
    const forgotFeedback = document.getElementById('forgot-password-feedback');

    if (forgotForm) {
        forgotForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = forgotEmailInput.value.trim();
            const btnText = forgotSubmitBtn.querySelector('span');

            btnText.textContent = "Sending link...";
            forgotSubmitBtn.disabled = true;
            if (authErrorMsg) hideError(authErrorMsg);
            if (forgotFeedback) forgotFeedback.classList.add('hidden');

            try {
                const data = await api.forgotPassword(email);
                if (forgotFeedback) {
                    forgotFeedback.textContent = data.message || MESSAGES.PASSWORD_RESET_SENT;
                    forgotFeedback.classList.remove('hidden');
                }
                forgotForm.reset();
            } catch (error) {
                showError(authErrorMsg, "Unable to request password reset: " + error.message);
            } finally {
                btnText.textContent = "Send Reset Link";
                forgotSubmitBtn.disabled = false;
            }
        });
    }

    // Reset Password Form Handling
    const resetForm = document.getElementById('reset-password-form');
    const resetNewPasswordInput = document.getElementById('reset-new-password');
    const resetConfirmPasswordInput = document.getElementById('reset-confirm-password');
    const resetTokenInput = document.getElementById('reset-token-input');
    const resetSubmitBtn = document.getElementById('reset-submit-btn');
    const resetFeedback = document.getElementById('reset-password-feedback');

    const resetConstraints = {
        length: document.getElementById('reset-constraint-length'),
        number: document.getElementById('reset-constraint-number'),
        special: document.getElementById('reset-constraint-special')
    };

    if (resetNewPasswordInput) {
        resetNewPasswordInput.addEventListener('input', () => {
            validatePassword(resetNewPasswordInput.value, resetConstraints);
        });
    }

    if (resetForm) {
        resetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const token = resetTokenInput ? resetTokenInput.value.trim() : "";
            const newPassword = resetNewPasswordInput.value;
            const confirmPassword = resetConfirmPasswordInput.value;

            if (!token) {
                showError(authErrorMsg, "Invalid or missing reset token.");
                return;
            }

            if (!validatePassword(newPassword, resetConstraints)) {
                showError(authErrorMsg, MESSAGES.PASSWORD_REQ);
                return;
            }

            if (newPassword !== confirmPassword) {
                showError(authErrorMsg, MESSAGES.PASSWORD_MISMATCH);
                return;
            }

            const btnText = resetSubmitBtn.querySelector('span');
            btnText.textContent = "Updating password...";
            resetSubmitBtn.disabled = true;
            if (authErrorMsg) hideError(authErrorMsg);

            try {
                const data = await api.resetPassword(token, newPassword);
                if (resetFeedback) {
                    resetFeedback.textContent = data.message || MESSAGES.PASSWORD_RESET_SUCCESS;
                    resetFeedback.classList.remove('hidden');
                }
                resetForm.reset();
                Object.values(resetConstraints).forEach(c => { if (c) c.className = ''; });

                // Redirect to login after a brief pause so user can read confirmation
                setTimeout(() => {
                    window.location.hash = '#/login';
                }, 2500);
            } catch (error) {
                showError(authErrorMsg, "Reset failed: " + error.message);
                resetSubmitBtn.disabled = false;
            } finally {
                btnText.textContent = "Update Password";
            }
        });
    }

    // Google Sign-In Event Binding
    const googleLoginBtn = document.getElementById('google-login-btn');
    if (googleLoginBtn) {
        googleLoginBtn.addEventListener('click', async () => {
            const btnText = googleLoginBtn.querySelector('span');
            const originalText = btnText ? btnText.textContent : "Continue with Google";
            if (btnText) btnText.textContent = "Connecting to Google...";
            googleLoginBtn.disabled = true;
            authErrorMsg.classList.add('hidden');

            try {
                // Firebase popup sign-in
                const result = await signInWithPopup(auth, googleProvider);
                // Retrieve Firebase ID Token
                const idToken = await result.user.getIdToken();
                // Call backend custom google login route
                const data = await api.googleLogin(idToken);
                state.setToken(data.access_token);
                // Trigger route authentication routing checks
                await checkAuthStatus();
            } catch (error) {
                console.error("Google authentication failed: ", error);
                showError(authErrorMsg, "Google authentication failed: " + error.message);
                googleLoginBtn.disabled = false;
                if (btnText) btnText.textContent = originalText;
            }
        });
    }

    initialized = true;
}

/**
 * Initializes/resets the Login page view state without overwriting window.location.hash.
 */
export function initializeLoginPage() {
    const authErrorMsg = document.getElementById('auth-error');
    if (authErrorMsg) authErrorMsg.classList.add('hidden');

    resetAuthModalToTabs();
    const tabLogin = document.getElementById('tab-login');
    const tabSignup = document.getElementById('tab-signup');
    const loginPlane = document.getElementById('login-plane');
    const signupPlane = document.getElementById('signup-plane');

    if (tabLogin) tabLogin.classList.add('active');
    if (tabSignup) tabSignup.classList.remove('active');
    if (loginPlane) {
        loginPlane.classList.remove('hidden');
        loginPlane.classList.add('active-plane');
    }
    if (signupPlane) {
        signupPlane.classList.add('hidden');
        signupPlane.classList.remove('active-plane');
    }
}

