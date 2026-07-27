/**
 * Profile Section component. Maps profile properties to DOM text fields.
 */

/**
 * Populates Recruiter dashboard and profile view element fields.
 * @param {Object} profile - User profile containing recruiter details
 */
export function populateRecruiterProfileUI(profile) {
    const recName = profile.email.split('@')[0];
    const compName = profile.recruiter_profile?.company_name || "N/A";
    const compType = profile.recruiter_profile?.company_type || "N/A";
    const hiringDomain = profile.recruiter_profile?.hiring_domain || "N/A";

    const mappings = {
        "dash-rec-name": recName,
        "dash-comp-name": compName,
        "dash-comp-type": compType,
        "dash-hiring-domain": hiringDomain,
        "rec-top-user-name": recName,
        "profile-rec-name": recName,
        "profile-rec-email": profile.email,
        "profile-comp-name": compName,
        "profile-comp-type": compType,
        "profile-hiring-domain": hiringDomain
    };

    Object.entries(mappings).forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el) {
            el.textContent = val;
        }
    });
}
