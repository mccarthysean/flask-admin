"use strict";

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

// // GET is the default method, so we don't need to set it
// fetch('/hello/')
//     .then(function (response) {
//         return response.text();
//     }).then(function (text) {
//         console.log('GET response text:');
//         console.log(text); // Print the greeting as text
//     });
// // Send the same request as above, but get the response as JSON
// fetch('/hello/')
//     .then(function (response) {
//         return response.json(); // But parse it as JSON this time
//     })
//     .then(function (json) {
//         console.log('GET response as JSON:');
//         console.log(json); // Here’s our JSON object
//     })
// // POST from the browser to Python
// fetch('/hello/', {
//     // Declare what type of data we're sending
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     // Specify the method
//     method: 'POST',
//     // A JSON payload
//     body: JSON.stringify({
//         "greeting": "Hello from the browser!"
//     })
// }).then(function (response) { // At this point, Flask has printed our JSON
//     return response.text();
// }).then(function (text) {
//     console.log('POST response: ');
//     // Should be 'OK' if everything was successful
//     console.log(text);
// });
console.log(_typeof(10));
$("h1").css("color", "red");