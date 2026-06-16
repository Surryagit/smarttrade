// Global logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/';
}

// Redirect to login if no token
function requireAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) window.location.href = '/';
    return token;
}