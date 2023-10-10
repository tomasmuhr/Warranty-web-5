// // main script for bootstrap
// // Script for JS import for shown page
// var currentPage = window.location.pathname;
// var scriptElement = document.createElement("script");
// console.log("Current page: " + currentPage);

// if (currentPage === "/index" || currentPage === "/") {
//     console.log("Index page has no JavaScript.");
// } else {
//     var bootstrapName = currentPage.split("/")[1];
//     var pageName = currentPage.split("/")[2];
//     var JSName = "/js/" + bootstrapName + "." + pageName + ".js"

//     console.log("Bootstrap name: " + bootstrapName);
//     console.log("Page name:      " + pageName);
//     console.log("JS name:        " + JSName);

//     if (bootstrapName === "user") {
//         fetch("../main/js/user.profile.js")
//             .then(response => {
//                 if (response.ok) {
//                     console.log("Script loaded.");
//                     scriptElement.src = "../main/js/user.profile.js";
//                 } else {
//                     console.log("Script by bootstrap prefix_url not found: " + JSName);
//                 }
//             })
//             .catch(error => {
//                 console.error(error);
//             });
//     } else {
//         fetch("../main/" + JSName)
//             .then(response => {
//                 if (response.ok) {
//                     console.log("Script loaded.");
//                     scriptElement.src = "../main/" + JSName;
//                 } else {
//                     console.log("Script by pagename not found: " + JSName);
//                 }
//             })
//             .catch(error => {
//                 console.error(error);
//             });
//     }
// }

// document.body.appendChild(scriptElement);

// Dark Mode Switch
const darkModeSwitch = document.getElementById('darkModeSwitch');
const body = document.body;

darkModeSwitch.addEventListener('change', () => {
    if (darkModeSwitch.checked) {
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
    }
});