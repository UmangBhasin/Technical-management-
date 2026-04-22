const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (password.length < 8) {
      window.APP_COMMON?.showMessage("formMessage", "Password must be at least 8 characters");
      return;
    }

    const payload = new URLSearchParams();
    payload.append("username", email);
    payload.append("password", password);

    try {
      const data = await window.API.request("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: payload,
      });

      window.API.setSession(data);
      window.location.href = data.role === "admin" ? "admin-dashboard.html" : "user-dashboard.html";
    } catch (error) {
      const message = error.message || "Login failed";
      const msgEl = document.getElementById("formMessage");
      msgEl.textContent = message;
    }
  });
}

if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const fullName = document.getElementById("fullName").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
      document.getElementById("formMessage").textContent = "Passwords do not match";
      return;
    }

    if (password.length < 8) {
      document.getElementById("formMessage").textContent = "Password must be at least 8 characters";
      return;
    }

    try {
      await window.API.request("/auth/register", {
        method: "POST",
        body: JSON.stringify({
          full_name: fullName,
          email,
          password,
        }),
      });

      document.getElementById("formMessage").style.color = "#0f766e";
      document.getElementById("formMessage").textContent = "Registration successful. Redirecting to login...";
      setTimeout(() => {
        window.location.href = "login.html";
      }, 900);
    } catch (error) {
      document.getElementById("formMessage").textContent = error.message || "Registration failed";
    }
  });
}
