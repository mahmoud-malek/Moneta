
// a sript for the login page
// it will be used to validate the login form
// stop the form from submitting if there are any errors
// and display the errors on the page
// prevent action on the form
// get the form element
const form = document.getElementById('login_form');

// get the email and password input elements
const email = document.getElementById('email');
const password = document.getElementById('password');

// get the error elements
const emailError = document.getElementById('email_error');
const passwordError = document.getElementById('password_error');

// add an event listener to the form
form.addEventListener('submit', (e) => {
  // initialize an array to store the error messages
  const messages = [];

  // check if the email input is empty
  if (email.value === '' || email.value == null) {
    messages.push('Email is required');
  }

  // check if the password input is empty
  if (password.value === '' || password.value == null) {
    messages.push('Password is required');
  }

  // check if the password is less than 6 characters
  if (password.value.length < 6) {
    messages.push('Password must be at least 6 characters');
  }

  // check if the password is more than 20 characters
  if (password.value.length > 20) {
    messages.push('Password must be less than 20 characters');
  }

  // check if there are any errors
  if (messages.length > 0) {
    // prevent the form from submitting
    e.preventDefault();

    // display the error messages
    emailError.innerText = messages[0];
    passwordError.innerText = messages[1];
  }
});
