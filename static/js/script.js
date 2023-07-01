const forms = document.querySelector(".forms"),
pwShowHide = document.querySelectorAll(".eye-icon"),
links = document.querySelectorAll(".link");

pwShowHide.forEach(eyeIcon => {
eyeIcon.addEventListener("click", () => {
  let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");
  
  pwFields.forEach(password => {
      if(password.type === "password"){
          password.type = "text";
          eyeIcon.classList.replace("bx-hide", "bx-show");
          return;
      }
      password.type = "password";
      eyeIcon.classList.replace("bx-show", "bx-hide");
  })
  
})
})      

links.forEach(link => {
link.addEventListener("click", e => {
 e.preventDefault(); //preventing form submit
 forms.classList.toggle("show-signup");
})
})
document.addEventListener('DOMContentLoaded', function() {
  // Get references to the delete form and button
  var deleteForm = document.getElementById('deleteForm');
  var deleteButton = document.getElementById('deleteButton');

  // Add click event listener to the delete button
  deleteButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the selected contact IDs
    var selectedContactIds = Array.from(document.querySelectorAll('input[name="contact_ids"]:checked')).map(function(checkbox) {
      return checkbox.value;
    });

    // Check if any contacts are selected
    if (selectedContactIds.length > 0) {
      // Send an AJAX request to delete the selected contacts
      var xhr = new XMLHttpRequest();
      xhr.open('POST', deleteForm.action);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.onload = function() {
        if (xhr.status === 204) {
          // Successful deletion
          location.reload(); // Refresh the page
        } else {
          // Error occurred during deletion
          alert('Error deleting selected contacts.');
        }
      };
      xhr.send(JSON.stringify({ selected_contacts: selectedContactIds }));
    } else {
      alert('Please select at least one contact to delete.');
    }
  });
});