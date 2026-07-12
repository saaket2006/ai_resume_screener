/**
 * Standardized loading state handler for buttons.
 */

/**
 * Toggles a button loading state by showing/hiding its loader and updating text.
 * @param {HTMLButtonElement} buttonEl - The button element
 * @param {boolean} isLoading - Whether the loading spinner should show
 * @param {string} loadingText - Text to display during loading
 * @param {string} defaultText - Standard button text
 */
export function toggleButtonLoading(buttonEl, isLoading, loadingText, defaultText) {
    if (!buttonEl) return;
    const btnText = buttonEl.querySelector('span');
    const loader = buttonEl.querySelector('.loader');

    buttonEl.disabled = isLoading;

    if (btnText) {
        btnText.textContent = isLoading ? loadingText : defaultText;
    }

    if (loader) {
        if (isLoading) {
            loader.classList.remove('hidden');
        } else {
            loader.classList.add('hidden');
        }
    }
}
