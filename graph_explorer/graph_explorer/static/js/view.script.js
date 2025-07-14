function dispatchNodeFocusEvent(nodeId) {
  let event = new CustomEvent("node-focus", { detail: nodeId });
  document.dispatchEvent(event);
}