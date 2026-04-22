window.APP_COMMON.requireAuth(["admin", "user"]);
window.APP_COMMON.setupDashboardLink();

const transactionForm = document.getElementById("transactionForm");
const transactionTable = document.getElementById("transactionTable");
const memberSelect = document.getElementById("member_id");

let memberships = [];

async function loadMembershipOptions() {
  memberships = await window.API.request("/memberships/", { method: "GET" });
  memberSelect.innerHTML = memberships
    .map((m) => `<option value="${m.id}">${m.member_name} (${m.membership_type})</option>`)
    .join("");
}

function memberNameById(memberId) {
  const member = memberships.find((m) => m.id === memberId);
  return member ? member.member_name : `#${memberId}`;
}

function fillTransactionForm(row) {
  document.getElementById("transactionId").value = row.id;
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

  const payload = {
    member_id: Number(document.getElementById("member_id").value),
    amount: Number(document.getElementById("amount").value),
    transaction_type: document.getElementById("transaction_type").value.trim(),
    notes: document.getElementById("notes").value.trim() || null,
  };

  if (payload.amount <= 0) {
    window.APP_COMMON.showMessage("transactionMessage", "Amount must be greater than zero");
    return;
  }

  const id = document.getElementById("transactionId").value;
  const path = id ? `/transactions/${id}` : "/transactions/";
  const method = id ? "PUT" : "POST";

  try {
    await window.API.request(path, {
      method,
      body: JSON.stringify(payload),
    });
    transactionForm.reset();
    document.getElementById("transactionId").value = "";
    window.APP_COMMON.showMessage("transactionMessage", "Saved successfully", false);
    await loadMembershipOptions();
    await loadTransactions();
  } catch (error) {
    window.APP_COMMON.showMessage("transactionMessage", error.message);
  }
});

(async function init() {
  try {
    await loadMembershipOptions();
    await loadTransactions();
  } catch (error) {
    window.APP_COMMON.showMessage("transactionMessage", error.message);
  }
})();
