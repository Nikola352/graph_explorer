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
            showErrorModal("Error:", errData.error || "Server error");
          })
          .catch((err) => {
            showErrorModal("Error:", err.error || "Server error");
          });
      }
      location.reload();
    })
    .catch((error) => {
      showErrorModal("Error:", error || "Server error");
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

        if (workspace.data_source) {
          loadDataSourceConfiguration(
            workspace.data_source,
            workspace.data_source_config || {}
          );
        }
      } else {
        document.getElementById("workspace-form-title").textContent =
          "Create Workspace";
      }

      addWorkspaceFormSubmitListener();
      addDataSourceChangeListener();
    });
}

function closeWorkspaceForm() {
  const modal = document.getElementById("workspace-form-modal");
  if (modal) {
    modal.remove();
  }
}

function addDataSourceChangeListener() {
  const dataSourceSelect = document.getElementById(
    "workspace-datasource-select"
  );
  if (!dataSourceSelect) return;

  dataSourceSelect.addEventListener("change", function (e) {
    const selectedDataSource = e.target.value;
    if (selectedDataSource) {
      loadDataSourceConfiguration(selectedDataSource);
    } else {
      hideDataSourceConfiguration();
    }
  });
}

function loadDataSourceConfiguration(dataSourceId, existingConfig = {}) {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch(`/data-source-config?data_source_id=${dataSourceId}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.params && data.params.length > 0) {
        displayDataSourceConfiguration(data.params, existingConfig);
      } else {
        hideDataSourceConfiguration();
      }
    })
    .catch((error) => {
      showErrorModal("Error loading data source configuration:", error);
      //console.error("Error loading data source configuration:", error);
      hideDataSourceConfiguration();
    });
}

function displayDataSourceConfiguration(params, existingConfig = {}) {
  const container = document.getElementById("datasource-config-container");
  const fieldsContainer = document.getElementById("datasource-config-fields");

  if (!container || !fieldsContainer) return;

  fieldsContainer.innerHTML = "";

  params.forEach((param) => {
    const fieldDiv = createConfigurationField(
      param,
      existingConfig[param.name]
    );
    fieldsContainer.appendChild(fieldDiv);
  });

  container.style.display = "block";
}

function hideDataSourceConfiguration() {
  const container = document.getElementById("datasource-config-container");
  if (container) {
    const inputs = container.querySelectorAll("input");
    inputs.forEach((input) => {
      input.removeAttribute("required");
    });
    container.style.display = "none";
  }
}

function createConfigurationField(param, existingValue) {
  const fieldDiv = document.createElement("div");
  fieldDiv.className = "field";

  const label = document.createElement("label");
  label.className = "label";
  label.textContent = param.display_name;
  if (param.required) {
    label.innerHTML += ' <span class="has-text-danger">*</span>';
  }

  const controlDiv = document.createElement("div");
  controlDiv.className = "control";

  let inputElement;
  const fieldName = `config_${param.name}`;
  const currentValue =
    existingValue !== undefined ? existingValue : param.default;

  switch (param.value_type) {
    case "str":
    case "url":
    case "email":
      inputElement = document.createElement("input");
      inputElement.className = "input";
      inputElement.type =
        param.value_type === "email"
          ? "email"
          : param.value_type === "url"
          ? "url"
          : "text";
      inputElement.name = fieldName;
      inputElement.placeholder = `Enter ${param.display_name.toLowerCase()}`;
      if (currentValue) inputElement.value = currentValue;
      break;

    case "password":
      inputElement = document.createElement("input");
      inputElement.className = "input";
      inputElement.type = "password";
      inputElement.name = fieldName;
      inputElement.placeholder = `Enter ${param.display_name.toLowerCase()}`;
      if (currentValue) inputElement.value = currentValue;
      break;

    case "int":
    case "float":
      inputElement = document.createElement("input");
      inputElement.className = "input";
      inputElement.type = "number";
      if (param.value_type === "float") {
        inputElement.step = "any";
      }
      inputElement.name = fieldName;
      inputElement.placeholder = `Enter ${param.display_name.toLowerCase()}`;
      if (currentValue !== undefined) inputElement.value = currentValue;
      break;

    case "bool":
      const checkboxDiv = document.createElement("div");
      checkboxDiv.className = "field";

      const checkboxLabel = document.createElement("label");
      checkboxLabel.className = "checkbox";

      inputElement = document.createElement("input");
      inputElement.type = "checkbox";
      inputElement.name = fieldName;
      inputElement.value = "true";

      if (currentValue === true || currentValue === "true") {
        inputElement.checked = true;
      }

      checkboxLabel.appendChild(inputElement);
      checkboxLabel.appendChild(
        document.createTextNode(` ${param.display_name}`)
      );

      controlDiv.appendChild(checkboxLabel);
      fieldDiv.appendChild(label);
      fieldDiv.appendChild(controlDiv);
      return fieldDiv;

    case "date":
      inputElement = document.createElement("input");
      inputElement.className = "input";
      inputElement.type = "date";
      inputElement.name = fieldName;
      if (currentValue) inputElement.value = currentValue;
      break;

    case "datetime":
      inputElement = document.createElement("input");
      inputElement.className = "input";
      inputElement.type = "datetime-local";
      inputElement.name = fieldName;
      if (currentValue) inputElement.value = currentValue;
      break;

    case "choice":
      const selectDiv = document.createElement("div");
      selectDiv.className = "select";

      inputElement = document.createElement("select");
      inputElement.name = fieldName;

      // Add default option
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = `Select ${param.display_name.toLowerCase()}`;
      defaultOption.disabled = true;
      defaultOption.selected = !currentValue;
      inputElement.appendChild(defaultOption);

      // Add options
      param.options.forEach((option) => {
        const optionElement = document.createElement("option");
        optionElement.value = option.value;
        optionElement.textContent = option.display;
        if (currentValue === option.value) {
          optionElement.selected = true;
        }
        inputElement.appendChild(optionElement);
      });

      selectDiv.appendChild(inputElement);
      controlDiv.appendChild(selectDiv);
      fieldDiv.appendChild(label);
      fieldDiv.appendChild(controlDiv);
      return fieldDiv;

    default:
      inputElement = document.createElement("input");
      inputElement.className = "input";
      inputElement.type = "text";
      inputElement.name = fieldName;
      inputElement.placeholder = `Enter ${param.display_name.toLowerCase()}`;
      if (currentValue) inputElement.value = currentValue;
  }

  if (param.required && inputElement.type !== "checkbox") {
    inputElement.required = true;
  }

  controlDiv.appendChild(inputElement);
  fieldDiv.appendChild(label);
  fieldDiv.appendChild(controlDiv);

  return fieldDiv;
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

    // Collect configuration parameters
    const config = {};
    const formData = new FormData(form);

    for (let [key, value] of formData.entries()) {
      if (key.startsWith("config_")) {
        const paramName = key.substring(7); // Remove "config_" prefix
        config[paramName] = value;
      }
    }

    // Handle checkboxes (they won't appear in FormData if unchecked)
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach((checkbox) => {
      if (checkbox.name.startsWith("config_")) {
        const paramName = checkbox.name.substring(7);
        config[paramName] = checkbox.checked;
      }
    });

    const requestData = {
      name,
      data_source_id,
      workspace_id,
      config,
    };

    fetch(form.action, {
      method: workspace_id ? "PUT" : "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        if (!response.ok) {
          return response
            .json()
            .then((errData) => {
              showErrorModal("Error:", errData.error || "Server error");
            })
            .catch((err) => {
              showErrorModal("Error:", err.error || "Server error");
            });
        }
        location.reload();
      })
      .catch((error) => {
        showErrorModal("Error:", err.error || "Server error");
      });
  });
}

function deleteWorkspace(workspace_id) {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch(`delete-workspace/${workspace_id}/`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => {
      if (!response.ok) {
        return response
          .json()
          .then((errData) => {
            showErrorModal("Error:", errData.error || "Server error");
          })
          .catch((err) => {
            showErrorModal("Error:", err.error || "Server error");
          });
      }

      const workspaceElement = document.querySelector(
        `.workspace-row[data-workspace-id="${workspace_id}"]`
      );

      if (workspaceElement) {
        workspaceElement.remove();
      }

      //console.log("Successfully deleted the workspace.");
    })
    .catch((error) => {
      showErrorModal("Error:", error || "Server error");
    });
}

function refreshDataSource() {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch(`refresh-data-source/`, {
    method: "PUT",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => {
      if (!response.ok) {
        return response
          .json()
          .then((errData) => {
            showErrorModal("Error:", errData.error || "Server error");
          })
          .catch((err) => {
            showErrorModal("Error:", err.error || "Server error");
          });
      }
      location.reload();
    })
    .catch((error) => {
      showErrorModal("Error:", error);
    });
}
