document.addEventListener('DOMContentLoaded', function () {
  // Fetch the income of the user for this month
  fetch('/api/v1/income-month')
    .then(response => response.json())
    .then(data => {
      document.getElementById('income').textContent = parseFloat(data.income).toFixed(3);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

  // Fetch the expenses of the user for this month
  fetch('/api/v1/expenses-month')
    .then(response => response.json())
    .then(data => {
      document.getElementById('expenses').textContent = parseFloat(data.expenses).toFixed(3);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

  let categories = [];
  let transactions = [];

  // Fetch categories and transactions then create charts
  Promise.all([
    fetch('/api/v1/categories').then(response => response.json()),
    fetch('/api/v1/transactions').then(response => response.json())
  ])
    .then(([categoriesData, transactionsData]) => {
      categories = categoriesData.categories;
      transactions = transactionsData.transactions;

      createCharts();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

  function getRandomColor () {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  function generateRandomColors (count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
      colors.push(getRandomColor());
    }
    return colors;
  }

  function filterTransactionsByCurrentYear (transactions) {
    const currentYear = new Date().getFullYear();
    return transactions.filter(transaction => {
      const transactionYear = new Date(transaction.created_at).getFullYear();
      return transactionYear === currentYear;
    });
  }

  function groupTransactionsByMonth (transactions) {
    const months = Array(12).fill(0).map(() => ({ income: null, expenses: null, incomeDates: [], expensesDates: [] }));
    transactions.forEach(transaction => {
      const month = new Date(transaction.created_at).getMonth();
      if (transaction.amount > 0) {
        months[month].income += parseFloat(transaction.amount);
        months[month].incomeDates.push(transaction.created_at);
      } else {
        months[month].expenses += Math.abs(parseFloat(transaction.amount));
        months[month].expensesDates.push(transaction.created_at);
      }
    });
    return months;
  }

  function createCharts () {
    const currentYearTransactions = filterTransactionsByCurrentYear(transactions);
    const monthlyData = groupTransactionsByMonth(currentYearTransactions);

    const incomeData = monthlyData.map(month => month.income);
    const expensesData = monthlyData.map(month => month.expenses);

    // Income VS Expenses Chart
    const VSchart = document.getElementById('incomeExpensesChart').getContext('2d');
    const incomeExpensesChart = new Chart(VSchart, {
      type: 'line',
      data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [{
          label: 'Income',
          backgroundColor: 'green',
          borderColor: 'green',
          fill: false,
          data: incomeData,
          spanGaps: true
        }, {
          label: 'Expenses',
          backgroundColor: 'red',
          borderColor: 'red',
          fill: false,
          data: expensesData,
          spanGaps: true
        }]
      },
      options: {
        scales: {
          x: {
            beginAtZero: true
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                const index = context.dataIndex;
                const dataset = context.dataset.label;
                let label = dataset + ': ' + context.parsed.y.toFixed(2);
                if (dataset === 'Income') {
                  label += '\nDates: ' + monthlyData[index].incomeDates.join(', ');
                } else if (dataset === 'Expenses') {
                  label += '\nDates: ' + monthlyData[index].expensesDates.join(', ');
                }
                return label;
              }
            }
          }
        }
      }
    });

    // Spending Categories Chart
    const Cchart = document.getElementById('spendingCategoriesChart').getContext('2d');
    const spendingCategoriesChart = new Chart(Cchart, {
      type: 'doughnut',
      data: {
        labels: categories.map(category => category.name),
        datasets: [{
          label: 'Spending Categories',
          backgroundColor: generateRandomColors(categories.length),
          data: categories.map(category => parseFloat(category.current_balance))
        }]
      }
    });
  }

  // Toggel Button
  const toggleButton = document.createElement('div');
  toggleButton.classList.add('sidebar-toggle');
  toggleButton.innerHTML = '&#9776;';
  document.body.appendChild(toggleButton);

  const sidebar = document.querySelector('.sidebar');
  const header = document.querySelector('header');

  header.appendChild(toggleButton);
  toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('show');
  });

  // Close Sidebar when click anything outside it
  document.addEventListener('click', (e) => {
    if (!toggleButton.contains(e.target)) {
      sidebar.classList.remove('show');
    }
  });
});
