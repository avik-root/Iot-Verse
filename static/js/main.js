// main.js - Main JavaScript for IoT Verse

document.addEventListener('DOMContentLoaded', function() {
    console.log('IoT Verse - v1.2.7.9 - Developed by MintFire');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
    
    // Price filter range
    const minPriceInput = document.querySelector('input[name="min_price"]');
    const maxPriceInput = document.querySelector('input[name="max_price"]');
    const priceRange = document.getElementById('priceRange');
    
    if (priceRange && minPriceInput && maxPriceInput) {
        noUiSlider.create(priceRange, {
            start: [parseInt(minPriceInput.value) || 0, parseInt(maxPriceInput.value) || 100000],
            connect: true,
            range: {
                'min': 0,
                'max': 100000
            },
            step: 100
        });
        
        priceRange.noUiSlider.on('update', function(values) {
            minPriceInput.value = Math.round(values[0]);
            maxPriceInput.value = Math.round(values[1]);
        });
    }
});

function showNotification(message, type = 'info') {
    // Create notification container if it doesn't exist
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.style.minWidth = '300px';
    alert.style.marginBottom = '10px';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

function getAvailabilityClass(availability) {
    switch (availability) {
        case 'In Stock': return 'badge-instock';
        case 'Out of Stock': return 'badge-outofstock';
        case 'Low Stock': return 'badge-lowstock';
        default: return 'bg-secondary';
    }
}

window.iotVerse = {
    showNotification: showNotification
};