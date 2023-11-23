// empty value check
// Get the form element
const form = document.querySelector('#add_item_form');

// Add an event listener to the form submit event
form.addEventListener('submit', function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the value of the name field
    const name = document.querySelector('#add_item_name').value.trim();

    // Check if the name field is not empty
    if (name) {
        fetch('/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    } else {
        console.log('Name field is empty.');
    }
});

// Get items count in modal
// TODO
document.addEventListener('DOMContentLoaded', function() {
    var modals = document.querySelectorAll('.modal');
    var buttons = document.querySelectorAll('.open-modal');
    var closeButtons = document.querySelectorAll('.close');
  
    // Loop through each button and add a click event listener
    buttons.forEach(function(button, index) {
        button.addEventListener('click', function() {
            var shopId = button.dataset.shopId; // get the shop ID from the button's data attribute
            fetch('/get-value', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ shop_id: shopId })
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                var modalValue = document.getElementById('modal-value');
                modalValue.textContent = data.value; // display the value in the modal
                modals[index].style.display = 'block'; // show the modal
            });
        });
    });
  
    // Loop through each close button and add a click event listener
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var modal = this.closest('.modal');
            modal.style.display = 'none'; // hide the modal
        });
    });
  
    // When the user clicks anywhere outside of the modals, close them
    window.addEventListener('click', function(event) {
        modals.forEach(function(modal) {
            if (event.target == modal) {
                modal.style.display = 'none'; // hide the modal
            }
        });
    });
});
  