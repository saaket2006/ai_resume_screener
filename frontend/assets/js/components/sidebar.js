/**
 * Sidebar component that manages link highlights and titles in recruiter workspace.
 */

const sidebarLinkIds = {
    "#/recruiter/dashboard": "link-rec-dashboard",
    "#/recruiter/screen": "link-rec-screen",
    "#/recruiter/profile": "link-rec-profile"
};

/**
 * Updates the active link in the sidebar based on the current hash route.
 * @param {string} hash - The active hash route
 */
export function updateSidebarActiveLink(hash) {
    const defaultHash = "#/recruiter/dashboard";
    const activeHash = hash || defaultHash;

    // Remove active class from all links
    Object.values(sidebarLinkIds).forEach(id => {
        const link = document.getElementById(id);
        if (link) {
            link.classList.remove('active');
        }
    });

    // Add active class to current hash link
    const targetId = sidebarLinkIds[activeHash] || sidebarLinkIds[defaultHash];
    const activeLink = document.getElementById(targetId);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}
