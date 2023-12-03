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
  