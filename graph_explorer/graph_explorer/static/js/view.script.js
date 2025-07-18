let lastDispatchedNodeId = null;

function dispatchNodeFocusEvent(nodeId) {
  if (lastDispatchedNodeId === nodeId) return;
  lastDispatchedNodeId = nodeId;
  
  let event = new CustomEvent("node-focus", { detail: nodeId });
  document.dispatchEvent(event);
}
