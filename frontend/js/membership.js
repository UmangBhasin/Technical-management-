window.APP_COMMON.requireAuth(["admin", "user"]);
window.APP_COMMON.setupDashboardLink();

const membershipForm = document.getElementById("membershipForm");
const membershipTable = document.getElementById("membershipTable");

function validateMembershipDates(startDate, endDate) {
  return new Date(endDate) >= new Date(startDate);
}

function fillMembershipForm(row) {
  document.getElementById("membershipId").value = row.id;
  document.getElementById("member_name").value = row.member_name;
  document.getElementById("email").value = row.email;
  document.getElementById("phone").value = row.phone;
  document.getElementById("membership_type").value = row.membership_type;
  document.getElementById("start_date").value = row.start_date;
  document.getElementById("end_date").value = row.end_date;
  document.getElementById("status").value = row.status;
}

async function loadMemberships() {
  try {
    const data = await window.API.request("/memberships/", { method: "GET" });
    membershipTable.innerHTML = data
      .map(
        (item) => `<tr>
          <td>${item.member_name}</td>
          <td>${item.email}</td>
          <td>${item.membership_type}</td>
          <td>${item.status}</td>
          <td><button class="btn ghost" data-id="${item.id}">Edit</button></td>
        </tr>`,
      )
      .join("");

    Array.from(membershipTable.querySelectorAll("button[data-id]")).forEach((button) => {
      button.addEventListener("click", () => {
        const selected = data.find((x) => x.id === Number(button.dataset.id));
        if (selected) {
          fillMembershipForm(selected);
        }
      });
    });
  } catch (error) {
    window.APP_COMMON.showMessage("membershipMessage", error.message);
  }
}

membershipForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    member_name: document.getElementById("member_name").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    membership_type: document.getElementById("membership_type").value.trim(),
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value,
    status: document.getElementById("status").value,
  };

  if (!validateMembershipDates(payload.start_date, payload.end_date)) {
    window.APP_COMMON.showMessage("membershipMessage", "End date must be on or after start date");
    return;
  }

  const id = document.getElementById("membershipId").value;
  const path = id ? `/memberships/${id}` : "/memberships/";
  const method = id ? "PUT" : "POST";

  try {
    await window.API.request(path, {
      method,
      body: JSON.stringify(payload),
    });
    membershipForm.reset();
    document.getElementById("membershipId").value = "";
    window.APP_COMMON.showMessage("membershipMessage", "Saved successfully", false);
    loadMemberships();
  } catch (error) {
    window.APP_COMMON.showMessage("membershipMessage", error.message);
  }
});

loadMemberships();
