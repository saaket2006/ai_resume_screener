/**
 * Statistic Card component for updating dashboard counters.
 */

/**
 * Updates a statistic card value inside the DOM.
 * @param {string} elementId - ID of the element to update
 * @param {string|number} value - The new value to set
 */
export function updateStatisticCard(elementId, value) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = value;
    }
}
