document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('filter-form');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const attribute = document.getElementById('filter-attribute-input').value;
    const operator = document.querySelector('select[name="operator"]').value;
    const value = document.getElementById('filter-value-input').value;

    fetch(form.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify({
        attribute: attribute,
        operator: operator,
        value: value,
      })
    })
      .then(response => response.text())
      .then(data => {
        console.log("Server responded with:", data);
        // Optionally update DOM here
      })
      .catch(error => {
        console.error("Error:", error);
      });
  });
});
