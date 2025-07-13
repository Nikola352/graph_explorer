function selectWorkspace(workspace_id) {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch("/select-workspace/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ workspace_id }),
  })
    .then((response) => {
      if (!response.ok) {
        return response
          .json()
          .then((errData) => {
            console.error("Error:", errData.error || "Server error");
          })
          .catch((err) => {
            console.error("Error:", err.error || "Server error");
          });
      }
      location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function openWorkspaceForm(workspace = null) {
  fetch("/workspace-form/")
    .then((response) => response.text())
    .then((html) => {
      document.body.insertAdjacentHTML("beforeend", html);
      if (workspace) {
        document.getElementById("workspace-form-title").textContent =
          "Edit Workspace";
        document.getElementById("workspace-name-input").value = workspace.name;
        document.getElementById("workspace-datasource-select").value =
          workspace.data_source;
        document.getElementById("workspace-id-input").value = workspace.id;
      } else {
        document.getElementById("workspace-form-title").textContent =
          "Create Workspace";
      }

      addWorkspaceFormSubmitListener();
    });
}

function closeWorkspaceForm() {
  const modal = document.getElementById("workspace-form-modal");
  if (modal) {
    modal.remove();
  }
}

function addWorkspaceFormSubmitListener() {
  const form = document.getElementById("workspace-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;
    const name = document.getElementById("workspace-name-input").value;
    const data_source_id = document.getElementById(
      "workspace-datasource-select"
    ).value;
    const workspace_id = document.getElementById("workspace-id-input").value;

    fetch(form.action, {
      method: workspace_id ? "PUT" : "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ name, data_source_id, workspace_id }),
    })
      .then((response) => {
        if (!response.ok) {
          return response
            .json()
            .then((errData) => {
              console.error("Error:", errData.error || "Server error");
            })
            .catch((err) => {
              console.error("Error:", err.error || "Server error");
            });
        }
        location.reload();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
}
