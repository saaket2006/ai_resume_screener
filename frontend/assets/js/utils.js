/**
 * Validates a password against the required constraints.
 * Updates the visual state of constraint indicators.
 * @param {string} pass - The password to validate
 * @param {Object} constraintElems - { length, number, special } DOM elements
 * @returns {boolean} Whether all constraints pass
 */
export function validatePassword(pass, constraintElems) {
    const hasLength = pass.length >= 8;
    const hasNumber = /\d/.test(pass);
    const hasSpecial = /[@$!%*?&]/.test(pass);

    if (constraintElems.length) constraintElems.length.className = hasLength ? 'valid' : '';
    if (constraintElems.number) constraintElems.number.className = hasNumber ? 'valid' : '';
    if (constraintElems.special) constraintElems.special.className = hasSpecial ? 'valid' : '';

    return hasLength && hasNumber && hasSpecial;
}

/**
 * Shows an error message on an element.
 */
export function showError(elem, message) {
    elem.textContent = message;
    elem.classList.remove('hidden');
}

/**
 * Hides an error message element.
 */
export function hideError(elem) {
    elem.textContent = "";
    elem.classList.add('hidden');
}

/**
 * Escapes HTML characters in a string to prevent XSS.
 * @param {string} str - The string to escape
 * @returns {string} The escaped string
 */
export function escapeHTML(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
