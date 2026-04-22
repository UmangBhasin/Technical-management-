window.APP_COMMON.enforcePageFlow({ allowedRoles: ["admin"], pageType: "module" });
window.APP_COMMON.setupDashboardLink();
window.APP_COMMON.renderAppNav();

const addMembershipForm = document.getElementById("addMembershipForm");
const updateMembershipForm = document.getElementById("updateMembershipForm");
const membershipTable = document.getElementById("membershipTable");
const membershipPreview = document.getElementById("membershipPreview");
const membershipLookupId = document.getElementById("membershipLookupId");
const loadMembershipBtn = document.getElementById("loadMembershipBtn");

let selectedMembership = null;

function selectedRadioValue(name) {
  const selected = document.querySelector(`input[name='${name}']:checked`);
  return selected ? selected.value : "";
}

function renderMembershipPreview(row) {
  membershipPreview.innerHTML = `
    <strong>${row.member_name}</strong><br />
    ID: ${row.id}<br />
    Email: ${row.email}<br />
    Duration: ${row.membership_type}<br />
    Start: ${row.start_date}<br />
    End: ${row.end_date}<br />
    Status: ${row.status}
  `;
}

async function loadMemberships() {
  try {
    const data = await window.API.request("/memberships/", { method: "GET" });
    membershipTable.innerHTML = data
      .map(
        (item) => `<tr>
          <td>${item.id}</td>
          <td>${item.member_name}</td>
          <td>${item.email}</td>
          <td>${item.membership_type}</td>
          <td>${item.end_date}</td>
          <td>${item.status}</td>
          <td><button class="btn ghost" data-id="${item.id}">Use ID</button></td>
        </tr>`,
      )
      .join("");

    Array.from(membershipTable.querySelectorAll("button[data-id]")).forEach((button) => {
      button.addEventListener("click", () => {
        membershipLookupId.value = button.dataset.id;
      });
    });
  } catch (error) {
    window.APP_COMMON.showMessage("addMembershipMessage", error.message);
  }
}

addMembershipForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!window.APP_COMMON.validateMandatoryFields(["member_name", "email", "phone", "start_date", "status"], "addMembershipMessage")) {
    return;
  }

  const payload = {
    member_name: document.getElementById("member_name").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    duration: selectedRadioValue("duration"),
    start_date: document.getElementById("start_date").value,
    status: document.getElementById("status").value,
  };

  if (!payload.member_name || !payload.email || !payload.phone || !payload.start_date || !payload.duration) {
    window.APP_COMMON.showMessage("addMembershipMessage", "All fields are mandatory");
    return;
  }

  try {
    await window.API.request("/memberships/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    addMembershipForm.reset();
    window.APP_COMMON.showMessage("addMembershipMessage", "Membership added successfully", false);
    loadMemberships();
  } catch (error) {
    window.APP_COMMON.showMessage("addMembershipMessage", error.message);
  }
});

loadMembershipBtn.addEventListener("click", async () => {
  const id = Number(membershipLookupId.value);
  if (!id) {
    window.APP_COMMON.showMessage("updateMembershipMessage", "Membership ID is mandatory");
    return;
  }

  try {
    selectedMembership = await window.API.request(`/memberships/${id}`, { method: "GET" });
    renderMembershipPreview(selectedMembership);
    window.APP_COMMON.showMessage("updateMembershipMessage", "Membership loaded", false);
  } catch (error) {
    selectedMembership = null;
    membershipPreview.innerHTML = "";
    window.APP_COMMON.showMessage("updateMembershipMessage", error.message);
  }
});

updateMembershipForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const membershipId = Number(membershipLookupId.value);
  if (!membershipId) {
    window.APP_COMMON.showMessage("updateMembershipMessage", "Membership ID is mandatory for updates");
    return;
  }

  if (!selectedMembership || selectedMembership.id !== membershipId) {
    window.APP_COMMON.showMessage("updateMembershipMessage", "Load membership data using ID before updating");
    return;
  }

  const action = selectedRadioValue("update_action");
  const extensionDuration = selectedRadioValue("extension_duration") || "6 months";

  const payload = {
    membership_id: membershipId,
    action,
    extension_duration: extensionDuration,
  };

  try {
    const updated = await window.API.request(`/memberships/${membershipId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
    selectedMembership = updated;
    renderMembershipPreview(updated);
    window.APP_COMMON.showMessage("updateMembershipMessage", "Membership updated successfully", false);
    loadMemberships();
  } catch (error) {
    window.APP_COMMON.showMessage("updateMembershipMessage", error.message);
  }
});

loadMemberships();
