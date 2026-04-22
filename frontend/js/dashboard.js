(async function initDashboard() {
  window.APP_COMMON.requireAuth(["admin", "user"]);
  window.APP_COMMON.setupCommonHeader();

  const role = window.APP_COMMON.currentRole();
  if (role === "admin" && !window.location.pathname.endsWith("admin-dashboard.html")) {
    window.location.href = "admin-dashboard.html";
    return;
  }
  if (role === "user" && !window.location.pathname.endsWith("user-dashboard.html")) {
    window.location.href = "user-dashboard.html";
    return;
  }

  try {
    const stats = await window.API.request("/reports/dashboard", { method: "GET" });
    const container = document.getElementById("statsContainer");
    const cards = [
      ["Total Users", stats.total_users],
      ["Total Memberships", stats.total_memberships],
      ["Active Memberships", stats.active_memberships],
      ["Total Transactions", stats.total_transactions],
      ["Total Revenue", `INR ${Number(stats.total_revenue).toFixed(2)}`],
    ];

    if (role === "admin") {
      cards.push(["Maintenance Cost", `INR ${Number(stats.total_maintenance_cost).toFixed(2)}`]);
    }

    container.innerHTML = cards
      .map(
        ([title, value]) =>
          `<article class="stat-card"><h3>${title}</h3><p>${value}</p></article>`,
      )
      .join("");
  } catch (error) {
    document.getElementById("statsContainer").innerHTML = `<p>${error.message}</p>`;
  }
})();
