// -------------------------------------------------------------------------------------
function sendData() {
  const targetUrl = 'http://127.0.0.1:8500/user/contact_list/add-contact/';
  const theForm = document.getElementById("theform");
  const formData = new FormData(theForm);
  fetch(targetUrl, {
    method: "POST",
    body: formData
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not OK");
      }
      return response.json();
    })
    .then(data => {
      // console.log(data);  // Log the received JSON data
      // Handle the data or update the UI as needed
      // Close the modal after successful submission
      $('#addContactModal').modal('hide');
      
      // Update the contact list
      updateContactList();
      window.location.reload();

    })
    .catch(error => {
      console.log("Error:", error);
    });
}
function updateContactList() {
  // Perform a new fetch request to get the updated contact list data
  fetch('http://127.0.0.1:8500/user/contact_list/')
    .then(response => response.json())
    .then(data => {
      // Update the contact list UI with the new data
      // You can use JavaScript DOM manipulation or a frontend framework like React or Vue.js
      console.log("Updated contact list:", data);
    })
    .catch(error => {
      console.log("Error:", error);
    });
}
// -------------------------------------------------------------------------------------
// function bildfordata(){
//   let theform = document.getElementById("theform");
//   let data = new FormData(theform);
//   // logFormData(data);
//   data.append("name", document.getElementById("dataname").value);
//   data.append("number", document.getElementById("datanumber").value);
//   data.append("email", document.getElementById("dataemail").value);
//   logFormData(data);
// }

// function logFormData(data) {
//   for (let pair of data.entries()) {
//     console.log(`${pair[0]}, ${pair[1]}`);
//   }
// }