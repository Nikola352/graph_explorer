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
    `  help` +
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
              e.tgt
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
    cliModal.style.display = "none";
    window.location.reload();
  }, 900);
}

function showCliError(data) {
  let errIcon = '<span class="icon">❌</span> ';
  if (data.usage) {
    cliResult.innerHTML =
      errIcon +
      (data.error || "Error") +
      '<br><pre style="margin:0;font-size:1em;white-space:pre-wrap;">' +
      data.usage +
      "</pre>";
  } else {
    cliResult.innerHTML = errIcon + (data.error || "Unknown error.");
  }
  cliResult.className = "cli-modal-result error";
}

cliExecuteBtn.onclick = async () => {
  const command = cliInput.value.trim();
  if (!command) {
    cliResult.innerHTML =
      '<span class="icon">⚠️</span> Please enter a command.';
    cliResult.className = "cli-modal-result error";
    return;
  }
  cliResult.innerHTML = '<span class="cli-modal-spinner"></span> Executing...';
  cliResult.className = "cli-modal-result";

  try {
    const resp = await fetch("/cli/execute/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command }),
    });
    const data = await resp.json();

    if (data.success) {
      showCliSuccess(data.result, data.nodes, data.edges);
    } else {
      showCliError(data);
    }
  } catch (e) {
    cliResult.innerHTML = '<span class="icon">❌</span> Network/server error.';
    cliResult.className = "cli-modal-result error";
  }
};

// Close modal on Escape
window.addEventListener("keydown", (e) => {
  if (cliModal.style.display === "flex" && e.key === "Escape")
    cliModal.style.display = "none";
});
