/**
 * Initializes generic modals like Contact modal.
 */
export function initModals() {
    const contactModal = document.getElementById('contact-modal');
    const contactTriggerBtn = document.getElementById('contact-trigger-btn');
    const closeContactBtn = document.getElementById('close-contact-btn');

    // Show/Hide Contact Modal
    if (contactTriggerBtn && contactModal && closeContactBtn) {
        contactTriggerBtn.addEventListener('click', () => {
            contactModal.classList.remove('hidden');
        });

        closeContactBtn.addEventListener('click', () => {
            contactModal.classList.add('hidden');
        });

        contactModal.addEventListener('click', (e) => {
            if (e.target === contactModal) {
                contactModal.classList.add('hidden');
            }
        });
    }

    // Hide Name modal / Change name elements as custom name editing is replaced in Phase 1
    const changeNameBtn = document.getElementById('change-name-btn');
    if (changeNameBtn) {
        changeNameBtn.style.display = "none";
    }
}
