document.addEventListener('DOMContentLoaded', () => {
  let transactions = [];
  const categories = {};
  const transactionsPerPage = 6;
  let currentPage = 1;
  let totalPages = 1;
  let filteredTransactions = [];

  // Fetch transactions and categories concurrently
  Promise.all([
	fetch('/api/v1/transactions')
	  .then(response => response.json())
	  .then(data => {
		transactions = data.transactions;
		filteredTransactions = transactions;
		totalPages = Math.ceil(transactions.length / transactionsPerPage);
	  }),
	fetch('/api/v1/categories')
	  .then(response => response.json())
	  .then(data => {
		data.categories.forEach(category => {
		  categories[category.id] = category.name;
		});
	  })
  ]).then(() => {
	// Sort transactions by date
	transactions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

	// Add transactions to transactions list
	updateTransactionsList(currentPage, filteredTransactions);

	// Add categories to select
	const categorySelect = document.getElementById('transaction-category');
	Object.entries(categories).forEach(([id, name]) => {
	  const option = document.createElement('option');
	  option.value = id;
	  option.text = name;
	  categorySelect.appendChild(option);
	});
  });

  const addTransactionBtn = document.getElementById('addTransactionBtn');
  const addTransactionModel = document.getElementById('addTransactionModel');
  const closeModel = document.getElementsByClassName('close')[0];
  const transactionForm = document.getElementById('transactionForm');
  const transactionsList = document.querySelector('.transactions-list');
  const prevPage = document.getElementById('prevPage');
  const nextPage = document.getElementById('nextPage');
  const pageInfo = document.getElementById('pageInfo');

  addTransactionBtn.onclick = () => {
	  addTransactionModel.style.display = 'block';
	  // make the date field default to today's date
	  const today = new Date().toISOString().split('T')[0];
	  document.getElementById('transaction-date').value = today;
  };

  closeModel.onclick = () => {
	addTransactionModel.style.display = 'none';
  };

  window.onclick = (event) => {
	if (event.target === addTransactionModel) {
		addTransactionModel.style.display = 'none';
	}
	if (event.target === editTransactionModel) {
	  editTransactionModel.style.display = 'none';
	}
  };

  // Submit transaction form
  transactionForm.onsubmit = (event) => {
	event.preventDefault();

	const date = document.getElementById('transaction-date').value;
	const amount = document.getElementById('transaction-amount').value;
	const category = document.getElementById('transaction-category').value;
	const type = document.getElementById('transactionType').value;

	const newTransaction = {
	  date,
	  amount,
	  category_id: category,
	  type
	};

	fetch('/api/v1/transactions', {
	  method: 'POST',
	  headers: {
		'Content-Type': 'application/json'
	  },
	  body: JSON.stringify(newTransaction)
	})
	  .then(response => response.json())
	  .then(data => {
		if (data.success) {
		  filteredTransactions.unshift(data.transaction);
		  totalPages = Math.ceil(filteredTransactions.length / transactionsPerPage);
		  updateTransactionsList(currentPage, filteredTransactions);
		  addTransactionModel.style.display = 'none';
		  transactionForm.reset();
		} else {
		  alert('Error adding transaction');
		}
	  })
	  .catch(error => {
		console.error('Error:', error);
		alert('Error adding transaction');
	  });
  };

  // pagination functionality

  prevPage.onclick = () => {
	if (currentPage > 1) {
	  currentPage--;
	  updateTransactionsList(currentPage, filteredTransactions);
	}
  };

  nextPage.onclick = () => {
	if (currentPage < totalPages) {
	  currentPage++;
	  updateTransactionsList(currentPage, filteredTransactions);
	}
  };

  function updateTransactionsList (page, currentTransactions) {
	const startIDX = (page - 1) * transactionsPerPage;
	const endIDX = startIDX + transactionsPerPage;
	currentTransactions = currentTransactions.slice(startIDX, endIDX);
	transactionsList.innerHTML = ''; // clear current transactions list

	currentTransactions.forEach(transaction => {
	  const transactionItem = document.createElement('div');
	  transactionItem.className = 'transaction-item';
	  transactionItem.innerHTML = `
				<div class="transaction-info">
					<span><p>Date: </p>${new Date(transaction.created_at).toLocaleDateString('en-GB')}</span>
					<span><p>Category Name: </P>${categories[transaction.category_id]}</span>
					<span><p>Type: </p>${transaction.amount > 0 ? 'Income' : 'Expense'}</span>
				</div>
				<div class="transaction-amount ${transaction.amount > 0 ? 'income' : 'expense'}">
					<span>${transaction.amount > 0 ? '+' : '-'}$${Math.abs(transaction.amount)}</span>
				</div>
				<div id="edit-transaction" class="edit-transaction">
					<button id="edit-transaction" class="edit-transaction-btn" data-id="${transaction.id}"> Edit </button>
				</div>
				<div id="delete-transaction" class="delete-transaction">
					<button id="delete-transaction" class="delete-transaction-btn" data-id="${transaction.id}"> Delete </button>
				</div>
			`;
	  transactionsList.appendChild(transactionItem);
	});

	// update pagination
	pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
	prevPage.disabled = currentPage === 1; // disable prev button if on first page
	nextPage.disabled = currentPage === totalPages; // disable next button if on last page
  }

  // Edit transaction
  const editTransactionModel = document.getElementById('editTransactionModel');
  const editTransactionForm = document.getElementById('editTransactionForm');
  const closeEditModel = document.getElementsByClassName('close')[1];

  closeEditModel.onclick = () => {
	editTransactionModel.style.display = 'none';
  };

  transactionsList.addEventListener('click', (event) => {
	if (event.target.id === 'edit-transaction') {
	  const transactionID = event.target.dataset.id;
	  const transaction = transactions.find(transaction => transaction.id === transactionID);
	  editTransactionModel.style.display = 'block';
	  editTransactionForm.dataset.id = transactionID;
	  document.getElementById('edit-transaction-date').value = (new Date(transaction.created_at)).toLocaleDateString('en-GB').split('/').reverse().join('-');
	  document.getElementById('edit-transaction-amount').value = Math.abs(transaction.amount);
	  // add categories to select and set selected category to transaction category
	  console.log('here');
	  const categorySelect = document.getElementById('edit-transaction-category');
	  categorySelect.innerHTML = '';
	  Object.entries(categories).forEach(([id, name]) => {
		const option = document.createElement('option');
		option.value = id;
		option.text = name;
		categorySelect.appendChild(option);
		if (id === transaction.category_id) {
		  option.selected = true;
		}
	  });
	  document.getElementById('edit-transactionType').value = transaction.amount > 0 ? 'Income' : 'Expense';
	}
  });

  editTransactionForm.onsubmit = (event) => {
	event.preventDefault();

	const date = document.getElementById('edit-transaction-date').value;
	const amount = document.getElementById('edit-transaction-amount').value;
	const category = document.getElementById('edit-transaction-category').value;
	const type = document.getElementById('edit-transactionType').value;
	const transactionID = editTransactionForm.dataset.id;

	const updatedTransaction = {
	  date,
	  amount,
	  category_id: category,
	  type
	};

	fetch(`/api/v1/transactions/${transactionID}`, {
	  method: 'PUT',
	  headers: {
		'Content-Type': 'application/json'
	  },
	  body: JSON.stringify(updatedTransaction)
	})
	  .then(response => response.json())
	  .then(data => {
		if (data.success) {
		  const transactionItem = document.querySelector(`.transaction-item div button[data-id="${transactionID}"]`).parentElement.parentElement;
		  transactionItem.querySelector('.transaction-info span:nth-child(1)').innerHTML = `<p>Date: </p>${new Date(data.transaction.created_at).toLocaleDateString('en-GB')}`;
		  transactionItem.querySelector('.transaction-info span:nth-child(2)').innerHTML = `<p>Category Name: </P>${categories[data.transaction.category_id]}`;
		  transactionItem.querySelector('.transaction-info span:nth-child(3)').innerHTML = `<p>Type: </p>${data.transaction.amount > 0 ? 'Income' : 'Expense'}`;
		  transactionItem.querySelector('.transaction-amount span').textContent = `${data.transaction.amount > 0 ? '+' : '-'}$${Math.abs(data.transaction.amount)}`;
		  editTransactionForm.reset();
		  editTransactionModel.style.display = 'none';
		} else {
		  alert('Error updating transaction');
		}
	  })
	  .catch(error => {
		console.error('Error:', error);
		alert('Error updating transaction');
	  });
  };

  // Delete transaction
  transactionsList.addEventListener('click', (event) => {
	if (event.target.id === 'delete-transaction') {
	  const transactionID = event.target.dataset.id;
	  if (confirm('Are you sure you want to delete this transaction?')) {
		fetch(`/api/v1/transactions/${transactionID}`, {
		  method: 'DELETE'
		})
		  .then(response => response.json())
		  .then(data => {
			if (data.success) {
			  const transactionItem = document.querySelector(`.transaction-item div button[data-id="${transactionID}"]`).parentElement.parentElement;
			  transactionItem.remove();
			  transactions = transactions.filter(transaction => transaction.id !== transactionID);
			  filteredTransactions = filteredTransactions.filter(transaction => transaction.id !== transactionID);
			  totalPages = Math.ceil(transactions.length / transactionsPerPage);
			  updateTransactionsList(currentPage, filteredTransactions);
			} else {
			  alert('Error deleting transaction');
			}
		  })
		  .catch(error => {
			console.error('Error:', error);
			alert('Error deleting transaction');
		  });
	  }
	}
  });

  // Search functionality
  const searchInput = document.getElementById('searchTransaction');
  const searchSelect = document.getElementById('sortTransaction');

  searchInput.oninput = () => {
	const searchValue = searchInput.value.toLowerCase();
	if (searchSelect.value === 'date') {
	  filteredTransactions = transactions.filter(transaction => new Date(transaction.created_at).toLocaleDateString('en-GB').includes(searchValue));
	} else if (searchSelect.value === 'category') {
	  filteredTransactions = transactions.filter(transaction => categories[transaction.category_id].toLowerCase().includes(searchValue));
	} else if (searchSelect.value === 'type') {
	  filteredTransactions = transactions.filter(transaction => transaction.amount > 0 ? 'Income'.toLowerCase().includes(searchValue) : 'Expense'.toLowerCase().includes(searchValue));
	} else if (searchSelect.value === 'amount') {
	  filteredTransactions = transactions.filter(transaction => Math.abs(transaction.amount).toString().includes(searchValue));
	}
	if (searchValue === '') {
	  filteredTransactions = transactions;
	}
	totalPages = Math.ceil(filteredTransactions.length / transactionsPerPage);
	updateTransactionsList(1, filteredTransactions);
  };

  searchInput.onchange = () => {
	const searchValue = searchInput.value.toLowerCase();
	if (searchSelect.value === 'date') {
	  filteredTransactions = transactions.filter(transaction => new Date(transaction.created_at).toLocaleDateString('en-GB').includes(searchValue));
	} else if (searchSelect.value === 'category') {
	  filteredTransactions = transactions.filter(transaction => categories[transaction.category_id].toLowerCase().includes(searchValue));
	} else if (searchSelect.value === 'type') {
	  filteredTransactions = transactions.filter(transaction => transaction.amount > 0 ? 'Income'.toLowerCase().includes(searchValue) : 'Expense'.toLowerCase().includes(searchValue));
	} else if (searchSelect.value === 'amount') {
	  filteredTransactions = transactions.filter(transaction => Math.abs(transaction.amount).toString().includes(searchValue));
	}
	if (searchValue === '') {
	  filteredTransactions = transactions;
	}
	totalPages = Math.ceil(filteredTransactions.length / transactionsPerPage);
	updateTransactionsList(1, filteredTransactions);
  };

	//Show minimized sidebar
	const toggleButton = document.createElement('div');
	toggleButton.classList.add('sidebar-toggle');
	toggleButton.innerHTML = '&#9776;';
	const header = document.getElementsByTagName('header')[0];
	header.insertBefore(toggleButton, header.firstChild);

  	const sidebar = document.querySelector('.sidebar');
	toggleButton.onclick = () => {
		sidebar.classList.toggle('show');
	};
	
	document.addEventListener('click', (event) => {
		if (!event.target.matches('.sidebar-toggle') && !event.target.matches('.sidebar a')) {
			sidebar.classList.remove('show');
		}
	});
});
