document.addEventListener('DOMContentLoaded', () => {
  const editButtons = document.querySelectorAll('.edit-btn');
  const editModal = document.getElementById('editModal');
  const modalFieldName = document.getElementById('modalFieldName');
  const editForm = document.getElementById('editForm');
  const editValue = document.getElementById('editValue');
  const passwordFields = document.querySelector('.password-fields');
  const closeBtn = document.querySelector('.close');
  let currentField = '';

  editButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      currentField = event.target.getAttribute('data-field');
      modalFieldName.textContent = currentField;

      if (currentField === 'password') {
        passwordFields.style.display = 'block';
        editValue.style.display = 'none';
      } else {
        passwordFields.style.display = 'none';
        editValue.style.display = 'block';
        editValue.value = document.getElementById(currentField).value;
      }

      editModal.style.display = 'block';
    });
  });

  closeBtn.addEventListener('click', () => {
    editModal.style.display = 'none';
  });

  window.addEventListener('click', (event) => {
    if (event.target === editModal) {
      editModal.style.display = 'none';
    }
  });

  editForm.addEventListener('submit', (event) => {
    event.preventDefault();

    if (currentField === 'password') {
      const currentPassword = document.getElementById('currentPassword').value;
      const newPassword = document.getElementById('newPassword').value;

      fetch('/api/v1/change-password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          old_password: currentPassword,
          new_password: newPassword
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Password updated successfully');
            editModal.style.display = 'none';
          } else {
            alert(data.message || 'Error updating password');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Error updating password');
        });
    } else {
      const newValue = editValue.value;
      const updateData = {};
      updateData[currentField] = newValue;

      fetch('/api/v1/edit-profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Profile updated successfully');
            document.getElementById(currentField).value = newValue;
            editModal.style.display = 'none';
          } else {
            alert(data.message || 'Error updating profile');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Error updating profile');
        });
    }
  });
});
