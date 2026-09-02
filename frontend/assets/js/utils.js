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
 * Safely escapes HTML special characters to prevent XSS.
 */
export function escapeHTML(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Sanitizes a URL, ensuring it has an http or https protocol.
 * Returns '#' if invalid.
 */
export function sanitizeUrl(urlStr) {
    if (!urlStr) return '#';
    try {
        const parsedUrl = new URL(urlStr.startsWith('http') ? urlStr : 'https://' + urlStr);
        if (parsedUrl.protocol === 'http:' || parsedUrl.protocol === 'https:') {
            return parsedUrl.href;
        }
    } catch (e) {
        // invalid URL
    }
    return '#';
