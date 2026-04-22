window.APP_COMMON.enforcePageFlow({ allowedRoles: ["admin"], pageType: "module" });
window.APP_COMMON.setupDashboardLink();
window.APP_COMMON.renderAppNav();

const maintenanceForm = document.getElementById("maintenanceForm");
const maintenanceTable = document.getElementById("maintenanceTable");
const userMaintenanceForm = document.getElementById("userMaintenanceForm");
const userMaintenanceTable = document.getElementById("userMaintenanceTable");

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

  if (!window.APP_COMMON.validateMandatoryFields(["title", "description", "maintenance_date", "status", "cost"], "maintenanceMessage")) {
    return;
  }

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

function fillManagedUserForm(user) {
  document.getElementById("managedUserId").value = user.id;
  document.getElementById("managedUserName").value = user.full_name;
  document.getElementById("managedUserEmail").value = user.email;
  document.getElementById("managedUserRole").value = user.role;
  document.getElementById("managedUserActive").checked = Boolean(user.is_active);
  document.getElementById("managedUserPassword").value = "";
}

async function loadManagedUsers() {
  try {
    const users = await window.API.request("/maintenance/users", { method: "GET" });
    userMaintenanceTable.innerHTML = users
      .map(
        (user) => `<tr>
          <td>${user.full_name}</td>
          <td>${user.email}</td>
          <td>${user.role}</td>
          <td>${user.is_active ? "active" : "inactive"}</td>
          <td>
            <button class="btn ghost" data-action="edit" data-id="${user.id}">Edit</button>
            <button class="btn ghost" data-action="delete" data-id="${user.id}">Delete</button>
          </td>
        </tr>`,
      )
      .join("");

    Array.from(userMaintenanceTable.querySelectorAll("button[data-action='edit']")).forEach((button) => {
      button.addEventListener("click", () => {
        const selected = users.find((u) => u.id === Number(button.dataset.id));
        if (selected) {
          fillManagedUserForm(selected);
        }
      });
    });

    Array.from(userMaintenanceTable.querySelectorAll("button[data-action='delete']")).forEach((button) => {
      button.addEventListener("click", async () => {
        const shouldDelete = window.confirm("Delete this user?");
        if (!shouldDelete) {
          return;
        }

        try {
          await window.API.request(`/maintenance/users/${button.dataset.id}`, { method: "DELETE" });
          window.APP_COMMON.showMessage("userMaintenanceMessage", "User deleted", false);
          loadManagedUsers();
        } catch (error) {
          window.APP_COMMON.showMessage("userMaintenanceMessage", error.message);
        }
      });
    });
  } catch (error) {
    window.APP_COMMON.showMessage("userMaintenanceMessage", error.message);
  }
}

userMaintenanceForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const userId = document.getElementById("managedUserId").value;
  const password = document.getElementById("managedUserPassword").value;

  if (!window.APP_COMMON.validateMandatoryFields(["managedUserName", "managedUserEmail", "managedUserPassword"], "userMaintenanceMessage")) {
    return;
  }

  if (password.length < 8) {
    window.APP_COMMON.showMessage("userMaintenanceMessage", "Password must be at least 8 characters");
    return;
  }

  const payload = {
    full_name: document.getElementById("managedUserName").value.trim(),
    email: document.getElementById("managedUserEmail").value.trim(),
    role: document.getElementById("managedUserRole").value,
    is_active: document.getElementById("managedUserActive").checked,
    password: password,
  };

  const path = userId ? `/maintenance/users/${userId}` : "/maintenance/users";
  const method = userId ? "PUT" : "POST";

  try {
    await window.API.request(path, {
      method,
      body: JSON.stringify(payload),
    });
    userMaintenanceForm.reset();
    document.getElementById("managedUserId").value = "";
    window.APP_COMMON.showMessage("userMaintenanceMessage", "User saved", false);
    loadManagedUsers();
  } catch (error) {
    window.APP_COMMON.showMessage("userMaintenanceMessage", error.message);
  }
});

loadManagedUsers();
