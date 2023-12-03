// // empty value check
// // Get the form element
// const form = document.querySelector('#add_item_form');

// // Add an event listener to the form submit event
// form.addEventListener('submit', function(event) {
//     // Prevent the default form submission behavior
//     event.preventDefault();

//     // Get the value of the name field
//     const name = document.querySelector('#add_item_name').value.trim();

//     // Check if the name field is not empty
//     if (name) {
//         fetch('/items', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ name })
//         })
//         .then(response => response.text())
//         .then(data => console.log(data))
//         .catch(error => console.error(error));
//     } else {
//         console.log('Name field is empty.');
//     }
// });

// Load shop items into modal
document.addEventListener("DOMContentLoaded", function() {
    const shopViewModals = document.querySelectorAll('[id^="shopView_"]');

    shopViewModals.forEach(function(shopViewModal) {
        shopViewModal.addEventListener("shown.bs.modal", function() {
            const shopViewModalId = shopViewModal.getAttribute("id");
        fetch("/shop_view_modal/" + shopViewModalId)
       .then(response => response.text())
       .then(data => {
        shopViewModal.querySelector("#items").innerHTML = data;
        });
      });
    });
  });
  