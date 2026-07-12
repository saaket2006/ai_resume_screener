/**
 * Standardized empty state HTML renderer.
 */

/**
 * Returns empty state block HTML string.
 * @param {string} message - Description message
 * @returns {string} The HTML string
 */
export function getEmptyStateHTML(message = "No items found.") {
    return `
        <div class="empty-state-block" style="text-align: center; padding: 2rem; color: var(--text-secondary);">
            <span style="font-size: 2.5rem; display: block; margin-bottom: 0.5rem;">📁</span>
            <p>${message}</p>
        </div>
    `;
}
