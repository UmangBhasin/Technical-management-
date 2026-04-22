window.APP_COMMON.enforcePageFlow({ allowedRoles: ["admin", "user"], pageType: "module" });
window.APP_COMMON.setupDashboardLink();
window.APP_COMMON.renderAppNav();

const userReportTable = document.getElementById("userReportTable");
const membershipReportTable = document.getElementById("membershipReportTable");
const transactionReportTable = document.getElementById("transactionReportTable");
const chartContainer = document.getElementById("chartContainer");

let userRows = [];
let membershipRows = [];
let transactionRows = [];

function rowsToCsv(rows, columns) {
  if (!rows.length) {
    return "";
  }
  const header = columns.map((col) => col.label).join(",");
  const lines = rows.map((row) => columns.map((col) => `"${String(col.value(row)).replace(/"/g, '""')}"`).join(","));
  return [header, ...lines].join("\n");
}

function downloadCsv(fileName, csvText) {
  if (!csvText) {
    window.APP_COMMON.showMessage("reportsMessage", "No data available to export");
    return;
  }

  const blob = new Blob([csvText], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", fileName);
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function bindExportButtons() {
  document.getElementById("exportUsersCsvBtn").addEventListener("click", () => {
    const csv = rowsToCsv(userRows, [
      { label: "ID", value: (r) => r.id },
      { label: "Name", value: (r) => r.full_name },
      { label: "Email", value: (r) => r.email },
      { label: "Role", value: (r) => r.role },
      { label: "Status", value: (r) => (r.is_active ? "active" : "inactive") },
      { label: "Created At", value: (r) => new Date(r.created_at).toISOString() },
    ]);
    downloadCsv("user-report.csv", csv);
  });

  document.getElementById("exportMembershipCsvBtn").addEventListener("click", () => {
    const csv = rowsToCsv(membershipRows, [
      { label: "ID", value: (r) => r.id },
      { label: "Member", value: (r) => r.member_name },
      { label: "Email", value: (r) => r.email },
      { label: "Duration", value: (r) => r.membership_type },
      { label: "Start Date", value: (r) => r.start_date },
      { label: "End Date", value: (r) => r.end_date },
      { label: "Status", value: (r) => r.status },
    ]);
    downloadCsv("membership-report.csv", csv);
  });

  document.getElementById("exportTransactionCsvBtn").addEventListener("click", () => {
    const csv = rowsToCsv(transactionRows, [
      { label: "ID", value: (r) => r.id },
      { label: "User ID", value: (r) => r.user_id },
      { label: "User", value: (r) => r.user_name },
      { label: "Member", value: (r) => r.member_name },
      { label: "Amount", value: (r) => r.amount },
      { label: "Type", value: (r) => r.transaction_type },
      { label: "Date", value: (r) => new Date(r.transaction_date).toISOString() },
    ]);
    downloadCsv("transaction-report.csv", csv);
  });
}

async function loadUserReport() {
  userRows = await window.API.request("/reports/users", { method: "GET" });
  if (!userRows.length) {
    userReportTable.innerHTML = '<tr><td colspan="6">No user data available</td></tr>';
    return;
  }
  userReportTable.innerHTML = userRows
    .map(
      (row) => `<tr>
        <td>${row.id}</td>
        <td>${row.full_name}</td>
        <td>${row.email}</td>
        <td>${row.role}</td>
        <td>${row.is_active ? "active" : "inactive"}</td>
        <td>${new Date(row.created_at).toLocaleString()}</td>
      </tr>`,
    )
    .join("");
}

async function loadMembershipReport() {
  membershipRows = await window.API.request("/reports/memberships", { method: "GET" });
  if (!membershipRows.length) {
    membershipReportTable.innerHTML = '<tr><td colspan="7">No membership data available</td></tr>';
    return;
  }
  membershipReportTable.innerHTML = membershipRows
    .map(
      (row) => `<tr>
        <td>${row.id}</td>
        <td>${row.member_name}</td>
        <td>${row.email}</td>
        <td>${row.membership_type}</td>
        <td>${row.start_date}</td>
        <td>${row.end_date}</td>
        <td>${row.status}</td>
      </tr>`,
    )
    .join("");
}

async function loadTransactionReport() {
  transactionRows = await window.API.request("/reports/transactions", { method: "GET" });
  if (!transactionRows.length) {
    transactionReportTable.innerHTML = '<tr><td colspan="6">No transaction data available</td></tr>';
    return;
  }
  transactionReportTable.innerHTML = transactionRows
    .map(
      (row) => `<tr>
        <td>${row.id}</td>
        <td>${row.user_name}</td>
        <td>${row.member_name}</td>
        <td>INR ${Number(row.amount).toFixed(2)}</td>
        <td>${row.transaction_type}</td>
        <td>${new Date(row.transaction_date).toLocaleString()}</td>
      </tr>`,
    )
    .join("");
}

function renderCharts() {
  if (!chartContainer) {
    return;
  }

  if (!transactionRows.length) {
    chartContainer.innerHTML = '<p class="subtext">No chart data available.</p>';
    return;
  }

  const grouped = transactionRows.reduce((acc, row) => {
    acc[row.transaction_type] = (acc[row.transaction_type] || 0) + Number(row.amount);
    return acc;
  }, {});

  const max = Math.max(...Object.values(grouped));
  const bars = Object.entries(grouped)
    .map(([name, total]) => {
      const width = Math.max(8, Math.round((total / max) * 100));
      return `<div class="chart-row"><span>${name}</span><div class="chart-track"><div class="chart-bar" style="width:${width}%"></div></div><strong>INR ${total.toFixed(2)}</strong></div>`;
    })
    .join("");

  chartContainer.innerHTML = bars;
}

(async function loadReports() {
  try {
    await Promise.all([loadUserReport(), loadMembershipReport(), loadTransactionReport()]);
    bindExportButtons();
    renderCharts();
  } catch (error) {
    window.APP_COMMON.showMessage("reportsMessage", error.message);
  }
})();
