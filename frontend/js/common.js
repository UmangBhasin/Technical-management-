function currentRole() {
  return sessionStorage.getItem("role");
}

function dashboardPath(role = currentRole()) {
  return role === "admin" ? "admin-dashboard.html" : "user-dashboard.html";
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
  dashboardLink.href = dashboardPath(role);
}

function renderAppNav() {
  const nav = document.getElementById("appNav");
  if (!nav) {
    return;
  }

  const role = currentRole();
  const isAdmin = role === "admin";
  const items = isAdmin
    ? [
        ["Dashboard", "admin-dashboard.html"],
        ["Maintenance", "maintenance.html"],
        ["Membership", "membership.html"],
        ["Transactions", "transactions.html"],
        ["Reports", "reports.html"],
        ["Charts", "reports.html#charts"],
      ]
    : [
        ["Dashboard", "user-dashboard.html"],
        ["Transactions", "transactions.html"],
        ["Reports", "reports.html"],
        ["Charts", "reports.html#charts"],
      ];

  const currentPath = window.location.pathname.split("/").pop() || "";
  const currentHash = window.location.hash || "";

  nav.innerHTML = items
    .map(([label, href]) => {
      const [targetPath, targetHash = ""] = href.split("#");
      const isActive = targetHash
        ? currentPath === targetPath && currentHash === `#${targetHash}`
        : currentPath === targetPath;
      return `<a href="${href}" class="${isActive ? "active" : ""}">${label}</a>`;
    })
    .join("");
}

function enforcePageFlow(options = {}) {
  const { allowedRoles = ["admin", "user"], pageType = "module" } = options;
  requireAuth(allowedRoles);

  const role = currentRole();
  const visitedDashboard = sessionStorage.getItem("dashboard_visited") === "yes";
  if (pageType === "dashboard") {
    sessionStorage.setItem("dashboard_visited", "yes");
    return;
  }

  if (!visitedDashboard) {
    window.location.href = dashboardPath(role);
  }
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

function validateMandatoryFields(fieldIds, messageElementId) {
  for (const fieldId of fieldIds) {
    const el = document.getElementById(fieldId);
    if (!el) {
      continue;
    }
    const value = (el.value || "").trim();
    if (!value) {
      showMessage(messageElementId, `${fieldId.replace(/_/g, " ")} is required`);
      return false;
    }
  }
  return true;
}

window.APP_COMMON = {
  requireAuth,
  setupDashboardLink,
  renderAppNav,
  enforcePageFlow,
  setupCommonHeader,
  showMessage,
  validateMandatoryFields,
  currentRole,
  currentName,
  dashboardPath,
};
