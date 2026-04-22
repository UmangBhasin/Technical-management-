window.APP_COMMON.requireAuth(["admin"]);
window.APP_COMMON.setupDashboardLink();

const maintenanceForm = document.getElementById("maintenanceForm");
const maintenanceTable = document.getElementById("maintenanceTable");

function fillMaintenanceForm(row) {
  document.getElementById("maintenanceId").value = row.id;
  document.getElementById("title").value = row.title;
  document.getElementById("description").value = row.description;
  document.getElementById("maintenance_date").value = row.maintenance_date;
  document.getElementById("status").value = row.status;
  document.getElementById("cost").value = row.cost;
}

async function loadMaintenance() {
  try {
    const data = await window.API.request("/maintenance/", { method: "GET" });
    maintenanceTable.innerHTML = data
      .map(
        (item) => `<tr>
          <td>${item.title}</td>
          <td>${item.maintenance_date}</td>
          <td>${item.status}</td>
          <td>INR ${Number(item.cost).toFixed(2)}</td>
          <td><button class="btn ghost" data-id="${item.id}">Edit</button></td>
        </tr>`,
      )
      .join("");

    Array.from(maintenanceTable.querySelectorAll("button[data-id]")).forEach((button) => {
      button.addEventListener("click", () => {
        const selected = data.find((x) => x.id === Number(button.dataset.id));
        if (selected) {
          fillMaintenanceForm(selected);
        }
      });
    });
  } catch (error) {
    window.APP_COMMON.showMessage("maintenanceMessage", error.message);
  }
}

maintenanceForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    title: document.getElementById("title").value.trim(),
    description: document.getElementById("description").value.trim(),
    maintenance_date: document.getElementById("maintenance_date").value,
    status: document.getElementById("status").value,
    cost: Number(document.getElementById("cost").value),
  };

  if (payload.cost < 0) {
    window.APP_COMMON.showMessage("maintenanceMessage", "Cost must be zero or higher");
    return;
  }

  const id = document.getElementById("maintenanceId").value;
  const path = id ? `/maintenance/${id}` : "/maintenance/";
  const method = id ? "PUT" : "POST";

  try {
    await window.API.request(path, {
      method,
      body: JSON.stringify(payload),
    });
    maintenanceForm.reset();
    document.getElementById("maintenanceId").value = "";
    window.APP_COMMON.showMessage("maintenanceMessage", "Saved successfully", false);
    loadMaintenance();
  } catch (error) {
    window.APP_COMMON.showMessage("maintenanceMessage", error.message);
  }
});

loadMaintenance();
