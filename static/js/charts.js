// charts.js - Chart.js integration for IoT Verse

let charts = [];

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all charts on the page
    initCharts();
    
    // Handle window resize
    window.addEventListener('resize', function() {
        charts.forEach(chart => {
            if (chart) chart.resize();
        });
    });
});

function initCharts() {
    // Price history charts
    document.querySelectorAll('.price-chart').forEach(container => {
        const canvas = container.querySelector('canvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            const data = JSON.parse(container.dataset.chartData || '{}');
            
            if (data.labels && data.prices && data.prices.length > 0) {
                const chart = renderPriceChart(ctx, data.labels, data.prices);
                charts.push(chart);
            }
        }
    });
    
    // Dashboard stats chart
    const dashboardChart = document.getElementById('dashboard-stats-chart');
    if (dashboardChart) {
        const ctx = dashboardChart.getContext('2d');
        
        // Sample dashboard data - in real app, this would come from API
        const data = {
            labels: ['Products', 'In Stock', 'Out of Stock', 'Low Stock'],
            datasets: [{
                label: 'Inventory Stats',
                data: [150, 120, 20, 10],
                backgroundColor: [
                    'rgba(37, 99, 235, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(245, 158, 11, 0.8)'
                ],
                borderColor: [
                    'rgb(37, 99, 235)',
                    'rgb(16, 185, 129)',
                    'rgb(239, 68, 68)',
                    'rgb(245, 158, 11)'
                ],
                borderWidth: 1
            }]
        };
        
        const chart = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        charts.push(chart);
    }
}

function renderPriceChart(ctx, labels, prices) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Price ($)',
                data: prices,
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#2563eb',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    callbacks: {
                        label: function(context) {
                            return `Price: $${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#64748b'
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(100, 116, 139, 0.1)'
                    },
                    ticks: {
                        color: '#64748b',
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'nearest'
            }
        }
    });
}

function destroyCharts() {
    charts.forEach(chart => {
        if (chart) chart.destroy();
    });
    charts = [];
}

// Export functions for global use
window.charts = {
    init: initCharts,
    destroy: destroyCharts,
    renderPriceChart: renderPriceChart
};