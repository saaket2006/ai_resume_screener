/**
 * Sidebar component that manages link highlights and titles in recruiter/candidate workspaces.
 */

const sidebarLinkIds = {
    "#/recruiter/dashboard": "link-rec-dashboard",
    "#/recruiter/screen": "link-rec-screen",
    "#/recruiter/profile": "link-rec-profile",
    "#/candidate/dashboard": "link-cand-dashboard",
    "#/candidate/screen": "link-cand-screen",
    "#/candidate/profile": "link-cand-profile"
};

/**
 * Updates the active link in the sidebar based on the current hash route.
 * @param {string} hash - The active hash route
 */
export function updateSidebarActiveLink(hash) {
    const activeHash = hash || "";

    // Remove active class from all links
    Object.values(sidebarLinkIds).forEach(id => {
        const link = document.getElementById(id);
        if (link) {
            link.classList.remove('active');
        }
    });

    // Add active class to current hash link
    const targetId = sidebarLinkIds[activeHash];
    const activeLink = document.getElementById(targetId);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}
