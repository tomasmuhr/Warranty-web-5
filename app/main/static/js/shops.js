// Load shop items into modal
document.addEventListener("DOMContentLoaded", function() {
    const shopViewModals = document.querySelectorAll('[id^="shopView_"]');

    shopViewModals.forEach(function(shopViewModal) {
        shopViewModal.addEventListener("shown.bs.modal", function() {
            const shopViewModalId = shopViewModal.getAttribute("id");
            const shop_id = shopViewModalId.split("_")[1];

            fetch("/shop_view_modal/" + shop_id)
            .then(response => response.text())
            .then(data => {
                shopViewModal.querySelector("#warranty-items-" + shop_id).innerHTML = data;
                // if (shopViewModal.querySelector("#warranty-items-" + shop_id)) {
                //     // element exists, set innerHTML
                //     console.log("Element exists");
                //   } else {
                //     // element doesn't exist, handle error
                //     console.log("Element doesn't exist");
                //   }
            });
        });
    });
});
  