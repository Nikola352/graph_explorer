function removeFilter(field, operator, value) {
  // Show skeleton loader
  if (window.skeletonLoader) {
    window.skeletonLoader.show();
  }
  
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/remove-filter/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      field,
      operator,
      value,
    }),
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

function removeSearch(search_term) {
  // Show skeleton loader
  if (window.skeletonLoader) {
    window.skeletonLoader.show();
  }
  
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/remove-search/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      search_term,
    }),
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
