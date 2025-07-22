function selectVisualizer(visualizer_id) {
  // Show skeleton loader
  if (window.skeletonLoader) {
    window.skeletonLoader.show();
  }
  
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
