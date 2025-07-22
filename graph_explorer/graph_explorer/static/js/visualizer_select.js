function selectVisualizer(visualizer_id) {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  fetch("/select-visualizer/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ visualizer_id }),
  })
    .then((response) => {
      if (!response.ok) {
        return response
          .json()
          .then((errData) => {
            showErrorModal(errData.error || "Server error");
          })
          .catch((err) => {
            showErrorModal(err.error || "Server error");
          });
      }
      location.reload();
    })
    .catch((error) => {
      showErrorModal(error || "Server error");
    });
}
