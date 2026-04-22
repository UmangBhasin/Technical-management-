function currentRole() {
  return sessionStorage.getItem("role");
}

function currentName() {
  return sessionStorage.getItem("full_name") || "User";
}

function requireAuth(allowedRoles = ["admin", "user"]) {
  const token = sessionStorage.getItem("access_token");
  const role = currentRole();
  if (!token || !allowedRoles.includes(role)) {
    window.location.href = "login.html";
  }
}

function setupDashboardLink() {
  const role = currentRole();
  const dashboardLink = document.getElementById("dashboardLink");
  if (!dashboardLink) {
    return;
  }
  dashboardLink.href = role === "admin" ? "admin-dashboard.html" : "user-dashboard.html";
}

function setupCommonHeader() {
  const welcomeText = document.getElementById("welcomeText");
  if (welcomeText) {
    welcomeText.textContent = `Welcome, ${currentName()}`;
  }

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      window.API.clearSession();
      window.location.href = "login.html";
    });
  }
}

function showMessage(elementId, message, isError = true) {
  const el = document.getElementById(elementId);
  if (!el) {
    return;
  }
  el.textContent = message;
  el.style.color = isError ? "#d62839" : "#0f766e";
}

window.APP_COMMON = {
  requireAuth,
  setupDashboardLink,
  setupCommonHeader,
  showMessage,
  currentRole,
};
