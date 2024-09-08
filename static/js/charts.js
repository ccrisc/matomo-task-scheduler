// Wait for DOMContentLoaded to ensure elements are present before working with them
document.addEventListener('DOMContentLoaded', function() {
    const deviceCtx = document.getElementById('deviceChart').getContext('2d');
    const browserCtx = document.getElementById('browserChart').getContext('2d');

    const deviceChart = new Chart(deviceCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Visits by Device Type',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const browserChart = new Chart(browserCtx, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
                label: 'Visits by Browser',
                data: [],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        }
    });

    // Event listener for form submission
    document.getElementById('filter-form').addEventListener('submit', function (e) {
        e.preventDefault();

        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;

        fetch('/api/stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({start_date: startDate, end_date: endDate})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data:', data); // Debugging line

            // Update device chart
            const deviceData = data.reduce((acc, cur) => {
                acc.labels.push(cur.device_type);
                acc.data.push(cur.total_visits);
                return acc;
            }, {labels: [], data: []});

            console.log('Device data:', deviceData); // Debugging line

            deviceChart.data.labels = deviceData.labels;
            deviceChart.data.datasets[0].data = deviceData.data;
            deviceChart.update();

            // Update browser chart
            const browserData = data.reduce((acc, cur) => {
                acc.labels.push(cur.browser_name);
                acc.data.push(cur.total_visits);
                return acc;
            }, {labels: [], data: []});

            console.log('Browser data:', browserData); // Debugging line

            browserChart.data.labels = browserData.labels;
            browserChart.data.datasets[0].data = browserData.data;
            browserChart.update();
        })
        .catch(error => console.error('Error fetching data:', error)); // Debugging line
    });
});
