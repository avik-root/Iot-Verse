// admin.js - Admin Panel JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('IoT Verse Admin Panel');
    
    // CSV upload zone
    const uploadZone = document.querySelector('.upload-zone');
    const fileInput = document.querySelector('input[name="csv_file"]');
    
    if (uploadZone && fileInput) {
        uploadZone.addEventListener('click', () => fileInput.click());
        
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = '#2563eb';
            uploadZone.style.backgroundColor = 'rgba(37, 99, 235, 0.1)';
        });
        
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.style.borderColor = '#cbd5e1';
            uploadZone.style.backgroundColor = '#f8fafc';
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = '#cbd5e1';
            uploadZone.style.backgroundColor = '#f8fafc';
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                const fileName = e.dataTransfer.files[0].name;
                uploadZone.innerHTML = `
                    <i class="bi bi-file-earmark-check display-4 text-success"></i>
                    <p class="mt-2">${fileName}</p>
                    <small class="text-muted">Ready to upload</small>
                `;
            }
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files.length) {
                const fileName = this.files[0].name;
                uploadZone.innerHTML = `
                    <i class="bi bi-file-earmark-check display-4 text-success"></i>
                    <p class="mt-2">${fileName}</p>
                    <small class="text-muted">Ready to upload</small>
                `;
            }
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                if (window.iotVerse && window.iotVerse.showNotification) {
                    window.iotVerse.showNotification('Please fill in all required fields', 'danger');
                } else {
                    alert('Please fill in all required fields');
                }
            }
        });
    });
    
    // Image preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = input.closest('.mb-3').querySelector('.image-preview');
                    if (!preview) {
                        const img = document.createElement('img');
                        img.className = 'image-preview img-thumbnail mt-2';
                        img.style.maxWidth = '200px';
                        input.closest('.mb-3').appendChild(img);
                    }
                    input.closest('.mb-3').querySelector('.image-preview').src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

function exportData(format) {
    if (format === 'json') {
        window.open('/api/products', '_blank');
    } else if (format === 'csv') {
        // Convert JSON to CSV
        fetch('/api/products')
            .then(response => response.json())
            .then(data => {
                const csv = convertToCSV(data);
                downloadCSV(csv, 'iot_products.csv');
            });
    }
}

function convertToCSV(data) {
    const headers = ['ID', 'Name', 'Price (INR)', 'Quantity', 'Availability', 'Type', 'Description'];
    const rows = data.map(item => [
        item.id,
        `"${item.name.replace(/"/g, '""')}"`,
        item.price,
        item.quantity,
        item.availability,
        `"${item.type.replace(/"/g, '""')}"`,
        `"${item.description.replace(/"/g, '""')}"`
    ]);
    
    return [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
}

function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

window.admin = {
    confirmDelete: confirmDelete,
    exportData: exportData
};