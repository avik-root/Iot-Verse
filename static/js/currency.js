// Currency conversion functionality

// Currency symbols mapping
const currencySymbols = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'AUD': 'A$',
    'CAD': 'C$',
    'CHF': 'Fr',
    'CNY': '¥',
    'HKD': 'HK$',
    'SGD': 'S$',
    'AED': 'د.إ',
    'SAR': '﷼',
    'BTC': '₿'
};

// Initialize currency from localStorage
function initializeCurrency() {
    const savedCurrency = localStorage.getItem('selectedCurrency') || 'INR';
    const savedSymbol = localStorage.getItem('selectedSymbol') || '₹';

    const currencyDisplay = document.getElementById('currencyDisplay');
    const currencyIcon = document.getElementById('currencyIcon');

    if (currencyDisplay) {
        currencyDisplay.textContent = savedCurrency;
    }
    if (currencyIcon) {
        currencyIcon.textContent = savedSymbol;
    }
}

// Change currency
function changeCurrency(currency, symbol) {
    // Get symbol from mapping if not provided
    const currencySymbol = symbol || currencySymbols[currency] || currency;

    // Save to localStorage
    localStorage.setItem('selectedCurrency', currency);
    localStorage.setItem('selectedSymbol', currencySymbol);

    // Update display
    const currencyDisplay = document.getElementById('currencyDisplay');
    const currencyIcon = document.getElementById('currencyIcon');

    if (currencyDisplay) {
        currencyDisplay.textContent = currency;
    }
    if (currencyIcon) {
        currencyIcon.textContent = currencySymbol;
    }

    // Convert all prices on the page
    convertAllPrices(currency);

    // Show notification
    showCurrencyNotification(currency, currencySymbol);
}

// Convert all prices on the page
function convertAllPrices(targetCurrency) {
    if (targetCurrency === 'INR') {
        // Reset to original INR prices
        restoreOriginalPrices();
        return;
    }

    // Get all price elements
    const priceElements = document.querySelectorAll('[data-price-inr]');

    priceElements.forEach(element => {
        const priceInr = parseFloat(element.getAttribute('data-price-inr'));
        const originalText = element.getAttribute('data-original-text') || element.textContent;

        // Store original text if not already stored
        if (!element.getAttribute('data-original-text')) {
            element.setAttribute('data-original-text', originalText);
        }

        // Convert price via API
        fetch('/api/convert-currency', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: priceInr,
                currency: targetCurrency
            })
        })
            .then(response => response.json())
            .then(data => {
                const symbol = data.symbol;
                const converted = data.converted_amount;

                // Format the converted price WITHOUT the ₹ symbol
                let formattedPrice;
                if (converted < 1) {
                    formattedPrice = `${symbol}${converted.toFixed(4)}`;
                } else if (converted < 1000) {
                    formattedPrice = `${symbol}${converted.toFixed(2)}`;
                } else {
                    formattedPrice = `${symbol}${converted.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;
                }

                // Update element - replace all content with new formatted price
                element.textContent = formattedPrice;
                element.setAttribute('data-converted-currency', targetCurrency);
            })
            .catch(error => {
                console.error('Currency conversion error:', error);
            });
    });
}

// Restore original prices
function restoreOriginalPrices() {
    const priceElements = document.querySelectorAll('[data-price-inr]');

    priceElements.forEach(element => {
        const originalText = element.getAttribute('data-original-text');
        if (originalText) {
            // Use original text which already includes ₹ symbol
            element.textContent = originalText;
            element.removeAttribute('data-converted-currency');
        }
    });
}

// Show currency notification
function showCurrencyNotification(currency, symbol) {
    const currencySymbol = symbol || currencySymbols[currency] || currency;
    const notification = document.createElement('div');
    notification.className = 'currency-notification';
    notification.textContent = `Currency changed to ${currencySymbol} ${currency}`;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: linear-gradient(135deg, #00ff99 0%, #00ffff 100%);
        color: #0a0e27;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(0, 255, 153, 0.5);
        z-index: 10000;
        font-weight: bold;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .currency-notification {
        font-size: 14px;
    }
`;
document.head.appendChild(style);

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeCurrency();
    // Store original text for all price elements (which already include ₹)
    const priceElements = document.querySelectorAll('[data-price-inr]');
    priceElements.forEach(element => {
        if (!element.getAttribute('data-original-text')) {
            element.setAttribute('data-original-text', element.textContent);
        }
    });
});

// Also apply saved currency on page load
window.addEventListener('load', () => {
    const savedCurrency = localStorage.getItem('selectedCurrency');
    if (savedCurrency && savedCurrency !== 'INR') {
        convertAllPrices(savedCurrency);
    }
});
