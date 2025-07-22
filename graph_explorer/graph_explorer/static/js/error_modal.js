window.showErrorModal = function (message) {
  var modal = document.getElementById("error-modal");
  var msgSpan = document.getElementById("error-modal-message");
  msgSpan.textContent = message || "Unknown error";
  modal.style.display = "flex";
  document.getElementById("error-modal-close").onclick = function () {
    modal.style.display = "none";
  };
  document.getElementById("error-modal-ok").onclick = function () {
    modal.style.display = "none";
  };
  modal.onclick = function (e) {
    if (e.target === modal) modal.style.display = "none";
  };
};
