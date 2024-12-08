// static/js/chart_handler.js

// Chart configuration
const chartConfig = {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Sensor 1',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.3,
                fill: true
            },
            {
                label: 'Sensor 2',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.3,
                fill: true
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                enabled: true,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    size: 13
                },
                bodyFont: {
                    size: 12
                },
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            // Convert to meters if over 100cm
                            if (context.parsed.y > 100) {
                                label += `${(context.parsed.y / 100).toFixed(2)}m`;
                            } else {
                                label += `${context.parsed.y.toFixed(1)}cm`;
                            }
                        }
                        return label;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: 1700,
                title: {
                    display: true,
                    text: 'Distance (cm/m)',
                    font: {
                        size: 14
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                },
                ticks: {
                    callback: function(value) {
                        // Convert to meters if over 100cm
                        if (value > 100) {
                            return `${(value/100).toFixed(1)}m`;
                        }
                        return `${value}cm`;
                    },
                    stepSize: 200
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                },
                grid: {
                    display: false
                }
            }
        }
    }
};

// Initialize chart
const ctx = document.getElementById('distanceChart').getContext('2d');
const chart = new Chart(ctx, chartConfig);

// Data management
const maxDataPoints = 50;
let lastUpdateTime = new Date();
let connectionLost = false;
let connectionTimeout;

// Format value for display
function formatDistance(value) {
    if (value > 100) {
        return `${(value/100).toFixed(2)}m`;
    }
    return `${value.toFixed(1)}cm`;
}

// Update the connection status
function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connectionStatus');
    if (connected) {
        statusElement.textContent = 'Connected';
        statusElement.style.color = '#28a745';
        connectionLost = false;
    } else {
        statusElement.textContent = 'Disconnected';
        statusElement.style.color = '#dc3545';
        connectionLost = true;
    }
}

// Format the timestamp
function formatTime(date) {
    return date.toLocaleTimeString('en-US', { 
        hour12: true,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Update the chart and display values
function updateDisplay(data) {
    // Update current readings with formatted values
    document.getElementById('sensor1').textContent = formatDistance(data.sensor1);
    document.getElementById('sensor2').textContent = formatDistance(data.sensor2);
    
    // Update last update time
    lastUpdateTime = new Date();
    document.getElementById('lastUpdate').textContent = formatTime(lastUpdateTime);

    // Update chart
    const timestamp = formatTime(lastUpdateTime);
    
    // Add new data points
    chart.data.labels.push(timestamp);
    chart.data.datasets[0].data.push(data.sensor1);
    chart.data.datasets[1].data.push(data.sensor2);

    // Remove old data points if we have too many
    if (chart.data.labels.length > maxDataPoints) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }

    // Update the chart
    chart.update('quiet');
}

// Fetch data from the server
function fetchData() {
    fetch('/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateConnectionStatus(true);
            updateDisplay(data);
            clearTimeout(connectionTimeout);
            connectionTimeout = setTimeout(() => {
                if (!connectionLost) {
                    updateConnectionStatus(false);
                }
            }, 2000);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            updateConnectionStatus(false);
        });
}

// Start periodic data updates
setInterval(fetchData, 100);

// Initial fetch
fetchData();