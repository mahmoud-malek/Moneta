// js file for categories page

document.addEventListener('DOMContentLoaded', () => {
  // Initialize variables
  let categories = [];
  let currentPage = 1;
  let totalPages = 1;
  let filteredCategories = [];
  const categoriesPerPage = 6;

  // Fetch categories
  fetch('/api/v1/categories')
    .then(response => response.json())
    .then(data => {
      categories = data.categories;
      // Sort categories by date
      categories.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      totalPages = Math.ceil(categories.length / categoriesPerPage);
      filteredCategories = categories;
      updateFilteredCategoriesList(currentPage, categories);
    });

  // Add category button
  const addCategoryBtn = document.getElementById('addCategoryBtn');
  const addCategoryModel = document.getElementById('addCategoryModel');
  const closeModel = document.getElementsByClassName('close')[0];
  const categoryForm = document.getElementById('categoryForm');
  const categoriesList = document.querySelector('.categories-list');
  const prevPage = document.getElementById('prevPage');
  const nextPage = document.getElementById('nextPage');
  const pageInfo = document.getElementById('pageInfo');

  addCategoryBtn.onclick = () => {
    addCategoryModel.style.display = 'block';
  };

  closeModel.onclick = () => {
    addCategoryModel.style.display = 'none';
  };

  window.onclick = (event) => {
    if (event.target === addCategoryModel) {
      addCategoryModel.style.display = 'none';
    }
  };

  // Add category form
  categoryForm.onsubmit = (event) => {
    event.preventDefault();
    const name = document.getElementById('category-name').value;
    const date = document.getElementById('category-date').value;
    const balance = document.getElementById('category-balance').value;
    const description = document.getElementById('category-description').value;

    const newCategory = {
      name,
      date,
      balance,
      description
    };

    fetch('/api/v1/categories', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newCategory)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Error adding category');
        }
        return response.json();
      })
      .then(data => {
        if (data.success === true) {
          filteredCategories.unshift(data.category);
          totalPages = Math.ceil(filteredCategories.length / categoriesPerPage);
          updateFilteredCategoriesList(currentPage, filteredCategories);
          addCategoryModel.style.display = 'none';
        } else {
          alert('Error adding category');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  // Update categories list
  const updateCategoriesList = (page) => {
    currentPage = page;
    categoriesList.innerHTML = ''; // Clear list
    const start = (page - 1) * categoriesPerPage;
    const end = start + categoriesPerPage;
    const paginatedCategories = categories.slice(start, end);
    paginatedCategories.forEach(category => {
      const categoryItem = document.createElement('div');
      categoryItem.className = 'category-item';
      categoryItem.innerHTML = `
				<div class="category-info">
					<span><p>Date: </P> ${new Date(category.created_at).toLocaleDateString('en-GB')}</span>
					<span><p>Name: </P>${category.name}</span>
					<span><p>Category_Balance: </p>${category.current_balance}</span>
					<span><p>Number of Transactions: </p>${category.transaction_count}</span>
				</div>
				<div id="edit-category" class="edit-category">
					<button id="edit-category" class="edit-category-btn" data-id="${category.id}"> Edit </button>
				</div>
				<div id="delete-category" class="delete-category">
					<button id="delete-category" class="delete-category-btn" data-id="${category.id}"> Delete </button>
				</div>
			`;
      categoriesList.appendChild(categoryItem);
    });

    // Update page info
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    prevPage.disabled = currentPage === 1;
    nextPage.disabled = currentPage === totalPages;
  };

  // Pagination

  prevPage.onclick = () => {
    if (currentPage > 1) {
      currentPage--;
      updateFilteredCategoriesList(currentPage, filteredCategories);
    }
  };

  nextPage.onclick = () => {
    if (currentPage < totalPages) {
      currentPage++;
      updateFilteredCategoriesList(currentPage, filteredCategories);
    }
  };

  // Delete category
  // Listen for clicks on the categoriesList container
  categoriesList.addEventListener('click', function (event) {
    // Check if the clicked element is a delete button or if the click came from within a delete button
    const deleteBtn = event.target.closest('.delete-category-btn');
    if (deleteBtn) {
      const categoryId = deleteBtn.getAttribute('data-id');
      const category = categories.find(category => category.id.toString() === categoryId);
      if (category) {
        const confirmation = confirm(`Are you sure you want to delete ${category.name}?`);
        if (confirmation) {
          fetch(`/api/v1/categories/${categoryId}`, {
            method: 'DELETE'
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Error deleting category');
              }
              return response.json();
            })
            .then(data => {
              if (data.success === true) {
                filteredCategories = filteredCategories.filter(category => category.id.toString() !== categoryId);
                categories = categories.filter(category => category.id.toString() !== categoryId);
                totalPages = Math.ceil(filteredCategories.length / categoriesPerPage);
                updateFilteredCategoriesList(currentPage, filteredCategories);
              } else {
                alert('Error deleting category');
              }
            })
            .catch(error => {
              console.error('Error:', error);
            });
        }
      }
    }
  });

  // Edit category
  const editCategoryModel = document.getElementById('editCategoryModel');
  const editCategoryForm = document.getElementById('editCategoryForm');
  const closeEditModel = document.getElementsByClassName('close')[1];

  closeEditModel.onclick = () => {
    editCategoryModel.style.display = 'none';
  };

  window.onclick = (event) => {
    if (event.target === editCategoryModel) {
      editCategoryModel.style.display = 'none';
    }
  };

  // Listen for clicks on the categoriesList container
  categoriesList.addEventListener('click', function (event) {
    // Check if the clicked element is an edit button or if the click came from within an edit button
    const editBtn = event.target.closest('.edit-category-btn');
    if (editBtn) {
      const categoryId = editBtn.getAttribute('data-id');
      const category = categories.find(category => category.id.toString() === categoryId);
      if (category) {
        // Display the edit category model
        document.getElementById('edit-category-name').value = category.name;
        document.getElementById('edit-category-date').value = (new Date(category.created_at)).toLocaleDateString('en-GB').split('/').reverse().join('-');
        document.getElementById('edit-category-balance').value = category.current_balance;
        document.getElementById('edit-category-description').value = category.description;
        document.getElementById('edit-category-id').value = categoryId;
        editCategoryModel.style.display = 'block';
      }
    }
  });

  // Update category form
  editCategoryForm.onsubmit = (event) => {
    event.preventDefault();
    const name = document.getElementById('edit-category-name').value;
    const date = document.getElementById('edit-category-date').value;
    const balance = document.getElementById('edit-category-balance').value;
    const description = document.getElementById('edit-category-description').value;
    const categoryId = document.getElementById('edit-category-id').value;

    const updatedCategory = {
      name,
      date,
      balance,
      description
    };

    fetch(`/api/v1/categories/${categoryId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedCategory)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Error updating category');
        }
        return response.json();
      })
      .then(data => {
        if (data.success === true) {
          const index = filteredCategories.findIndex(category => category.id.toString() === categoryId);
          categories[index] = data.category;
          filteredCategories[index] = data.category;
          updateFilteredCategoriesList(currentPage, filteredCategories);
          editCategoryModel.style.display = 'none'; // Correctly close the edit modal
          alert('Category updated successfully');
        } else {
          alert('Error updating category');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  // Search categories
  const searchInput = document.getElementById('searchCategory');
  const sortSelect = document.getElementById('sortCategory');

  searchInput.oninput = () => {
    const searchValue = searchInput.value.toLowerCase();
    filteredCategories = categories;
    if (sortSelect.value === 'date') {
      filteredCategories = filteredCategories.filter(category => category.created_at.toLowerCase().includes(searchValue));
    } else if (sortSelect.value === 'name') {
      filteredCategories = filteredCategories.filter(category => category.name.toLowerCase().includes(searchValue));
    } else if (sortSelect.value === 'balance') {
      filteredCategories = filteredCategories.filter(category => category.current_balance.toString().toLowerCase().includes(searchValue));
    } else if (sortSelect.value === 'numberOfTransactions') {
      filteredCategories = filteredCategories.filter(category => category.transaction_count.toString().includes(searchValue));
    }
    if (searchValue === '') {
      updateFilteredCategoriesList(1, categories);
    }
    totalPages = Math.ceil(filteredCategories.length / categoriesPerPage);
    updateFilteredCategoriesList(1, filteredCategories);
  };

  sortSelect.onchange = () => {
    const searchValue = searchInput.value.toLowerCase();
    filteredCategories = categories;
    if (sortSelect.value === 'date') {
      filteredCategories.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    } else if (sortSelect.value === 'name') {
      filteredCategories.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortSelect.value === 'balance') {
      filteredCategories.sort((a, b) => a.current_balance - b.current_balance);
    } else if (sortSelect.value === 'numberOfTransactions') {
      filteredCategories.sort((a, b) => a.transaction_count - b.transaction_count);
    }
    if (searchValue === '') {
      updateFilteredCategoriesList(1, categories);
    }
    filteredCategories = filteredCategories.filter(category => category.name.toLowerCase().includes(searchValue));
    totalPages = Math.ceil(filteredCategories.length / categoriesPerPage);
    updateFilteredCategoriesList(1, filteredCategories);
  };

  // update filtered categories list
  const updateFilteredCategoriesList = (page, filteredCategories) => {
    currentPage = page;
    categoriesList.innerHTML = ''; // Clear list
    const start = (page - 1) * categoriesPerPage;
    const end = start + categoriesPerPage;
    const paginatedCategories = filteredCategories.slice(start, end);
    paginatedCategories.forEach(category => {
      const categoryItem = document.createElement('div');
      categoryItem.className = 'category-item';
      categoryItem.innerHTML = `
				<div class="category-info">
					<span><p>Date: </P> ${new Date(category.created_at).toLocaleDateString('en-GB')}</span>
					<span><p>Name: </P>${category.name}</span>
					<span><p>Category_Balance: </p>${category.current_balance}</span>
					<span><p>Number of Transactions: </p>${category.transaction_count}</span>
				</div>
				<div id="edit-category" class="edit-category">
					<button id="edit-category" class="edit-category-btn" data-id="${category.id}"> Edit </button>
				</div>
				<div id="delete-category" class="delete-category">
					<button id="delete-category" class="delete-category-btn" data-id="${category.id}"> Delete </button>
				</div>
			`;
      categoriesList.appendChild(categoryItem);
    });

    // Update page info
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    prevPage.disabled = currentPage === 1;
    nextPage.disabled = currentPage === totalPages;
  };
});
