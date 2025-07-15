document.addEventListener('DOMContentLoaded', function () {
  const filterForm = document.getElementById('filter-form');
  const searchForm = document.getElementById('search-form');
  
  
  if (filterForm) filterForm.addEventListener('submit', handleFilterSubmit);
  if (searchForm) searchForm.addEventListener('submit', handleSearchSubmit);
});

function handleFilterSubmit(e){
   e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const attribute = document.getElementById('filter-attribute-input').value;
    const operator = document.querySelector('select[name="operator"]').value;
    const value = document.getElementById('filter-value-input').value;

    const filterForm = document.getElementById('filter-form');

    fetch(filterForm.action, {
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
        window.location.reload()
      })
      .catch(error => {
        console.error("Error:", error);
      });
}
        
function handleSearchSubmit(e){
   e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const query = document.getElementById('search-input').value;

    const searchForm = document.getElementById('search-form');


    fetch(searchForm.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify({
        query: query
      })
    })
      .then(response => response.text())
      .then(data => {
        console.log("Server responded with:", data);
        window.location.reload()
      })
      .catch(error => {
        console.error("Error:", error);
      });
}