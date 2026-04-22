window.APP_COMMON.requireAuth(["admin"]);
window.APP_COMMON.setupDashboardLink();

(async function loadReports() {
  try {
    const data = await window.API.request("/reports/monthly-revenue", { method: "GET" });
    const table = document.getElementById("monthlyRevenueTable");

    if (!data.length) {
      table.innerHTML = '<tr><td colspan="2">No revenue data available</td></tr>';
      return;
    }

    table.innerHTML = data
      .map((item) => `<tr><td>${item.month}</td><td>INR ${Number(item.revenue).toFixed(2)}</td></tr>`)
      .join("");
  } catch (error) {
    window.APP_COMMON.showMessage("reportsMessage", error.message);
  }
})();
