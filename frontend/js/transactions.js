window.APP_COMMON.enforcePageFlow({ allowedRoles: ["admin", "user"], pageType: "module" });
window.APP_COMMON.setupDashboardLink();
window.APP_COMMON.renderAppNav();

const transactionForm = document.getElementById("transactionForm");
const transactionTable = document.getElementById("transactionTable");
const userSelect = document.getElementById("user_id");
const memberSelect = document.getElementById("member_id");

let memberships = [];
let managedUsers = [];
let currentUser = null;

async function loadMembershipOptions() {
  memberships = await window.API.request("/transactions/memberships", { method: "GET" });
  memberSelect.innerHTML = memberships
    .map((m) => `<option value="${m.id}">${m.member_name} (${m.membership_type}) [${m.status}]</option>`)
    .join("");
}

async function loadUserOptions() {
  const role = window.APP_COMMON.currentRole();

  if (role === "admin") {
    managedUsers = await window.API.request("/maintenance/users", { method: "GET" });
    userSelect.innerHTML = managedUsers
      .map((u) => `<option value="${u.id}">${u.full_name} (${u.email})</option>`)
      .join("");
    return;
  }

  currentUser = await window.API.request("/auth/me", { method: "GET" });
  userSelect.innerHTML = `<option value="${currentUser.id}">${currentUser.full_name} (${currentUser.email})</option>`;
  userSelect.disabled = true;
}

function memberNameById(memberId) {
  const member = memberships.find((m) => m.id === memberId);
  return member ? member.member_name : `#${memberId}`;
}

function fillTransactionForm(row) {
  document.getElementById("transactionId").value = row.id;
  document.getElementById("user_id").value = row.user_id;
  document.getElementById("member_id").value = row.member_id;
  document.getElementById("amount").value = row.amount;
  document.getElementById("transaction_type").value = row.transaction_type;
  document.getElementById("notes").value = row.notes || "";
}

async function loadTransactions() {
  try {
    const data = await window.API.request("/transactions/", { method: "GET" });
    transactionTable.innerHTML = data
      .map(
        (item) => `<tr>
          <td>${item.user_id}</td>
          <td>${memberNameById(item.member_id)}</td>
          <td>INR ${Number(item.amount).toFixed(2)}</td>
          <td>${item.transaction_type}</td>
          <td>${new Date(item.transaction_date).toLocaleString()}</td>
          <td><button class="btn ghost" data-id="${item.id}">Edit</button></td>
        </tr>`,
      )
      .join("");

    Array.from(transactionTable.querySelectorAll("button[data-id]")).forEach((button) => {
      button.addEventListener("click", () => {
        const selected = data.find((x) => x.id === Number(button.dataset.id));
        if (selected) {
          fillTransactionForm(selected);
        }
      });
    });
  } catch (error) {
    window.APP_COMMON.showMessage("transactionMessage", error.message);
  }
}

transactionForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!window.APP_COMMON.validateMandatoryFields(["user_id", "member_id", "amount", "transaction_type", "notes"], "transactionMessage")) {
    return;
  }

  const payload = {
    user_id: Number(document.getElementById("user_id").value),
    member_id: Number(document.getElementById("member_id").value),
    amount: Number(document.getElementById("amount").value),
    transaction_type: document.getElementById("transaction_type").value.trim(),
    notes: document.getElementById("notes").value.trim(),
  };

  if (!payload.user_id || !payload.member_id || !payload.transaction_type) {
    window.APP_COMMON.showMessage("transactionMessage", "All required fields must be provided");
    return;
  }

  if (payload.amount <= 0 || Number.isNaN(payload.amount)) {
    window.APP_COMMON.showMessage("transactionMessage", "Amount must be greater than zero");
    return;
  }

  const id = document.getElementById("transactionId").value;
  const path = id ? `/transactions/${id}` : "/transactions/";
  const method = id ? "PUT" : "POST";

  try {
    userSelect.disabled = false;
    await window.API.request(path, {
      method,
      body: JSON.stringify(payload),
    });
    transactionForm.reset();
    document.getElementById("transactionId").value = "";
    if (window.APP_COMMON.currentRole() !== "admin" && currentUser) {
      userSelect.value = String(currentUser.id);
      userSelect.disabled = true;
    }
    window.APP_COMMON.showMessage("transactionMessage", "Saved successfully", false);
    await loadUserOptions();
    await loadMembershipOptions();
    await loadTransactions();
  } catch (error) {
    window.APP_COMMON.showMessage("transactionMessage", error.message);
  }
});

(async function init() {
  try {
    await loadUserOptions();
    await loadMembershipOptions();
    await loadTransactions();
  } catch (error) {
    window.APP_COMMON.showMessage("transactionMessage", error.message);
  }
})();
