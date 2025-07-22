const cliModal = document.getElementById("cli-modal");
const cliResult = document.getElementById("cli-result");
const cliInput = document.getElementById("cli-command-input");
const cliCloseBtn = document.getElementById("cli-close-btn");
const cliExecuteBtn = document.getElementById("cli-execute-btn");
const cliHelpBtn = document.getElementById("cli-help-btn");

document.getElementById("open-cli-modal-btn").onclick = () => {
  cliModal.style.display = "flex";
  cliResult.innerHTML = "";
  cliResult.className = "cli-modal-result";
  setTimeout(() => cliInput.focus(), 100);
};

cliCloseBtn.onclick = () => {
  cliModal.style.display = "none";
};

cliHelpBtn.onclick = () => {
  cliResult.innerHTML =
    '<span class="icon">❓</span>' +
    `<pre style="margin:0;font-size:1em;white-space:pre-wrap;">Graph CLI - commands:\n` +
    `  create-node --id &lt;id&gt; [--data '{json}']\n` +
    `      Example: create-node --id 1 --data '{\"name\": \"Test\"}'\n` +
    `  delete-node --id &lt;id&gt;\n` +
    `  create-edge --src &lt;id&gt; --tgt &lt;id&gt; [--data '{json}']\n` +
    `      Example: create-edge --src 1 --tgt 2 --data '{\"weight\": 5}'\n` +
    `  delete-edge --src &lt;id&gt; --tgt &lt;id&gt;\n` +
    `  clear-graph\n` +
    `</pre>`;
  cliResult.className = "cli-modal-result";
};

function updateGraphInfo(nodes, edges) {
  const nodesList = document.querySelector(".cli-modal-graphinfo-list");
  if (nodesList)
    nodesList.innerHTML =
      nodes
        .map(
          (n) =>
            `<li>ID: <b>${
              n.id
            }</b>, data: <span style='color:#1a699e'>${JSON.stringify(
              n.data
            )}</span></li>`
        )
        .join("") || "<li><i>No nodes</i></li>";
  const edgesList = document.querySelectorAll(".cli-modal-graphinfo-list")[1];
  if (edgesList)
    edgesList.innerHTML =
      edges
        .map(
          (e) =>
            `<li>${e.src} &rarr; ${
              e.target
            }, data: <span style='color:#1a699e'>${JSON.stringify(
              e.data
            )}</span></li>`
        )
        .join("") || "<li><i>No edges</i></li>";
}

function showCliSuccess(result, nodes, edges) {
  cliResult.innerHTML = '<span class="icon">✅</span> ' + result;
  cliResult.className = "cli-modal-result success";
  if (nodes && edges) {
    updateGraphInfo(nodes, edges);
  }
  setTimeout(() => {
    // Show skeleton loader before reloading
    if (window.skeletonLoader) {
      window.skeletonLoader.show();
    }
    cliModal.style.display = "none";
    window.location.reload();
  }, 900);
}

function showCliError(data) {
  let errIcon = '<span class="icon">❌</span> ';
  if (data.usage) {
    cliResult.innerHTML =
      errIcon +
      (data.message || "Error") +
      '<br><pre style="margin:0;font-size:1em;white-space:pre-wrap;">' +
      data.usage +
      "</pre>";
  } else {
    cliResult.innerHTML = errIcon + (data.message || "Unknown error.");
  }
  cliResult.className = "cli-modal-result error";
}

function parseCommand(commandString) {
  const parts = [];
  let current = "";
  let inQuotes = false;
  let quoteChar = "";

  for (let i = 0; i < commandString.length; i++) {
    const char = commandString[i];

    if ((char === "'" || char === '"') && !inQuotes) {
      inQuotes = true;
      quoteChar = char;
      current += char;
    } else if (char === quoteChar && inQuotes) {
      inQuotes = false;
      current += char;
    } else if (char === " " && !inQuotes) {
      if (current.trim()) {
        parts.push(current.trim());
        current = "";
      }
    } else {
      current += char;
    }
  }

  if (current.trim()) {
    parts.push(current.trim());
  }

  const command = parts[0];
  const args = {};

  for (let i = 1; i < parts.length; i += 2) {
    if (i + 1 < parts.length) {
      const key = parts[i].replace("--", "");
      let value = parts[i + 1];

      if (
        (value.startsWith("'") && value.endsWith("'")) ||
        (value.startsWith('"') && value.endsWith('"'))
      ) {
        value = value.slice(1, -1);
      }

      args[key] = value;
    }
  }

  return { command, args };
}

cliExecuteBtn.onclick = async () => {
  const commandString = cliInput.value.trim();

  if (!commandString) {
    cliResult.innerHTML =
      '<span class="icon">⚠️</span> Please enter a command.';
    cliResult.className = "cli-modal-result error";
    return;
  }

  cliResult.innerHTML = '<span class="cli-modal-spinner"></span> Executing...';
  cliResult.className = "cli-modal-result";

  try {
    const { command, args } = parseCommand(commandString);

    const requestBody = { command, args };

    const resp = await fetch("/cli/execute/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });
    const data = await resp.json();

    if (data.success) {
      showCliSuccess(data.message, data.graph_nodes, data.graph_edges);
    } else {
      showCliError(data);
    }
  } catch (e) {
    cliResult.innerHTML = '<span class="icon">❌</span> Network/server error.';
    cliResult.className = "cli-modal-result error";
  }
};

// Close modal
window.addEventListener("keydown", (e) => {
  if (cliModal.style.display === "flex" && e.key === "Escape")
    cliModal.style.display = "none";
});
