let currentPage = 1;
let chart = null;

// Upload and analyze file
document.getElementById('uploadBtn').addEventListener('click', async () => {
  const fileInput = document.getElementById('uploadFile');
  if (!fileInput.files.length) return alert('Select a file first');
  
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  const res = await fetch('/api/upload', { method: 'POST', body: formData });
  const data = await res.json();

  if (res.ok) {
    document.getElementById('fileInfo').innerHTML = `
      <strong>Columns:</strong> ${data.analysis.columns.join(', ')} <br>
      <strong>Rows:</strong> ${data.analysis.rows} <br>
      <strong>Types:</strong> ${JSON.stringify(data.analysis.dtypes)}
    `;
    alert('File uploaded and analyzed successfully!');
    loadData();  // load first page automatically
  } else {
    alert(data.error || 'Upload failed');
  }
});

// Load data and update table & chart
async function loadData() {
  const start = document.getElementById('start').value;
  const end = document.getElementById('end').value;
  const search = document.getElementById('search').value;
  const per_page = document.getElementById('perPage').value;

  const res = await fetch(`/api/get-data?start=${start}&end=${end}&search=${search}&page=${currentPage}&per_page=${per_page}`);
  const data = await res.json();

  if (data.error) return alert(data.error);

  // Populate table
  const tbody = document.querySelector('#dataTable tbody');
  tbody.innerHTML = '';
  data.data.forEach(row => {
    tbody.innerHTML += `
      <tr>
        <td>${row.date}</td>
        <td>${row.total_cases || ''}</td>
        <td>${row.new_cases || ''}</td>
      </tr>
    `;
  });

  document.getElementById('pageInfo').innerText = `Page ${data.page} of ${Math.ceil(data.total/per_page)}`;

  // Update chart
  updateChart(data.data);
}

// Update Chart.js chart
function updateChart(data) {
  const labels = data.map(row => row.date);
  const totalCases = data.map(row => row.total_cases || 0);
  const newCases = data.map(row => row.new_cases || 0);

  const ctx = document.getElementById('casesChart').getContext('2d');

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Total Cases',
          data: totalCases,
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.2,
        },
        {
          label: 'New Cases',
          data: newCases,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          tension: 0.2,
        }
      ]
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      stacked: false,
      plugins: {
        title: {
          display: true,
          text: 'COVID-19 Cases Trend'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// Pagination buttons
document.getElementById('prevPage').addEventListener('click', () => {
  if (currentPage > 1) { currentPage--; loadData(); }
});
document.getElementById('nextPage').addEventListener('click', () => {
  currentPage++; loadData();
});
