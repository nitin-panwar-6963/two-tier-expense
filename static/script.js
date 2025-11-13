async function fetchExpenses() {
  const search = document.getElementById('search').value;
  const start_date = document.getElementById('start_date').value;
  const end_date = document.getElementById('end_date').value;

  const params = new URLSearchParams({ search, start_date, end_date });
  const res = await fetch(`/api/expenses?${params.toString()}`);
  const data = await res.json();

  const tbody = document.querySelector('#expensesTable tbody');
  tbody.innerHTML = '';

  if (data.expenses.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5">No matching expenses found.</td></tr>';
  } else {
    data.expenses.forEach(e => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${e.expense_date}</td>
        <td>${e.title}</td>
        <td>${e.category}</td>
        <td>₹${e.amount.toFixed(2)}</td>
        <td>
          <a href="/edit/${e.id}" class="small">Edit</a>
          <button class="small danger delete-btn" data-id="${e.id}">Delete</button>
        </td>`;
      tbody.appendChild(tr);
    });
  }

  document.getElementById('total').textContent = data.total.toFixed(2);
}

document.addEventListener('DOMContentLoaded', () => {
  fetchExpenses();

  document.getElementById('filterBtn').addEventListener('click', fetchExpenses);
  document.getElementById('search').addEventListener('input', fetchExpenses);

  document.addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-btn')) {
      const id = e.target.dataset.id;
      if (!confirm('Delete this expense?')) return;
      const res = await fetch(`/delete/${id}`, { method: 'POST' });
      const j = await res.json();
      if (j.status === 'ok') fetchExpenses();
      else alert('Delete failed: ' + (j.message || 'unknown'));
    }
  });
});

