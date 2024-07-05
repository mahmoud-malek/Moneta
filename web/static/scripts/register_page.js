document.addEventListener('DOMContentLoaded', function () {
  // check for the variale success if present then show it and
  // after 1 second redirect to dashboard
  const success = document.getElementById('successMessage').value;
  if (success) {
    setTimeout(function () {
      window.location.href = '/dashboard';
    }, 1500);
  }
});
