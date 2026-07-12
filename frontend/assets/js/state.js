let state = {
    currentUser: null,
    currentProfile: null,
    authToken: localStorage.getItem("access_token") || null,
    currentRoute: window.location.hash || "",
    onboardingStatus: null
};

export function setUser(user) {
    state.currentUser = user;
}

export function getUser() {
    return state.currentUser;
}

export function setProfile(profile) {
    state.currentProfile = profile;
}

export function getProfile() {
    return state.currentProfile;
}

export function setToken(token) {
    state.authToken = token;
    if (token) {
        localStorage.setItem("access_token", token);
    } else {
        localStorage.removeItem("access_token");
    }
}

export function getToken() {
    return state.authToken;
}

export function clearState() {
    state.currentUser = null;
    state.currentProfile = null;
    state.authToken = null;
    state.currentRoute = "";
    state.onboardingStatus = null;
    localStorage.removeItem("access_token");
}

export function setRoute(route) {
    state.currentRoute = route;
}

export function getRoute() {
    return state.currentRoute;
}

export function setOnboardingStatus(status) {
    state.onboardingStatus = status;
}

export function getOnboardingStatus() {
    return state.onboardingStatus;
}
