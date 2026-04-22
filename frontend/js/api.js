const apiBaseUrl = window.APP_CONFIG.API_BASE_URL;

function getToken() {
  return sessionStorage.getItem("access_token");
}

function setSession({ access_token, role, full_name }) {
  sessionStorage.setItem("access_token", access_token);
  sessionStorage.setItem("role", role);
  sessionStorage.setItem("full_name", full_name);
}

function clearSession() {
  sessionStorage.clear();
}

async function request(path, options = {}) {
  const headers = options.headers || {};
  const token = getToken();

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    headers,
  });

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    throw new Error(data?.detail || "Request failed");
  }

  return data;
}

window.API = {
  request,
  setSession,
  clearSession,
  getToken,
};
