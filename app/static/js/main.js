// ATAK Kulübü - Main JavaScript

// Scroll pozisyonunu kaydet ve geri yükle
(function() {
    // Sayfa yüklendiğinde scroll pozisyonunu geri yükle
    const savedScrollPos = sessionStorage.getItem('scrollPosition');
    if (savedScrollPos) {
        setTimeout(() => {
            window.scrollTo(0, parseInt(savedScrollPos));
            sessionStorage.removeItem('scrollPosition');
        }, 100);
    }
    
    // Form gönderilmeden önce scroll pozisyonunu kaydet
    document.addEventListener('submit', function(e) {
        sessionStorage.setItem('scrollPosition', window.scrollY.toString());
    });
    
    // Link tıklanmadan önce scroll pozisyonunu kaydet (aynı sayfaysa)
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link && link.href) {
            const currentPath = window.location.pathname;
            const linkPath = new URL(link.href, window.location.origin).pathname;
            
            // Aynı sayfa içinde filtre/sayfalama gibi işlemler
            if (currentPath === linkPath || link.href.includes(currentPath)) {
                sessionStorage.setItem('scrollPosition', window.scrollY.toString());
            }
        }
    });
})();

document.addEventListener('DOMContentLoaded', function() {
    // Mobil menü toggle
    initMobileMenu();
    
    // Flash mesajları otomatik kapanma
    initAutoCloseAlerts();
    
    // Form validasyonu
    initFormValidation();
    
    // Smooth scroll
    initSmoothScroll();
    
    // Modal işlemleri
    initModals();
});

// Mobil Menü
function initMobileMenu() {
    const toggle = document.querySelector('.navbar-toggle');
    const nav = document.querySelector('.navbar-nav');
    
    if (toggle && nav) {
        toggle.addEventListener('click', function() {
            nav.classList.toggle('active');
        });
        
        // Dışarı tıklandığında menüyü kapat
        document.addEventListener('click', function(e) {
            if (!toggle.contains(e.target) && !nav.contains(e.target)) {
                nav.classList.remove('active');
            }
        });
    }
}

// Flash Mesajları Otomatik Kapanma
function initAutoCloseAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Close button ekle
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'alert-close';
        closeBtn.style.cssText = 'float: right; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: inherit; opacity: 0.7;';
        
        closeBtn.addEventListener('click', function() {
            alert.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        });
        
        alert.insertBefore(closeBtn, alert.firstChild);
        
        // 5 saniye sonra otomatik kapat
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    });
}

// Form Validasyonu
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                    
                    // Hata mesajı göster
                    let errorMsg = field.nextElementSibling;
                    if (!errorMsg || !errorMsg.classList.contains('error-msg')) {
                        errorMsg = document.createElement('span');
                        errorMsg.className = 'error-msg';
                        errorMsg.style.color = '#ef4444';
                        errorMsg.style.fontSize = '0.875rem';
                        errorMsg.textContent = 'Bu alan zorunludur';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                } else {
                    field.style.borderColor = '';
                    const errorMsg = field.nextElementSibling;
                    if (errorMsg && errorMsg.classList.contains('error-msg')) {
                        errorMsg.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Input değiştiğinde hata mesajını kaldır
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                this.style.borderColor = '';
                const errorMsg = this.nextElementSibling;
                if (errorMsg && errorMsg.classList.contains('error-msg')) {
                    errorMsg.remove();
                }
            });
        });
    });
}

// Smooth Scroll
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Modal İşlemleri
function initModals() {
    // Modal açma
    const modalTriggers = document.querySelectorAll('[data-modal]');
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const modalId = this.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'flex';
            }
        });
    });
    
    // Modal kapatma
    const modalCloses = document.querySelectorAll('.modal-close, [data-modal-close]');
    modalCloses.forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal-overlay');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Overlay'e tıklayınca kapat
    const modalOverlays = document.querySelectorAll('.modal-overlay');
    modalOverlays.forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) {
                this.style.display = 'none';
            }
        });
    });
    
    // ESC tuşu ile kapat
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal-overlay[style*="display: flex"]');
            if (openModal) {
                openModal.style.display = 'none';
            }
        }
    });
}

// Yardımcı Fonksiyonlar
function showLoading(button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Yükleniyor...';
    return originalText;
}

function hideLoading(button, originalText) {
    button.disabled = false;
    button.textContent = originalText;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Tarih formatlama
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return date.toLocaleDateString('tr-TR', options);
}

// Görsel yükleme önizleme
function initImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = input.nextElementSibling;
                    if (!preview || !preview.classList.contains('image-preview')) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview';
                        preview.style.cssText = 'max-width: 200px; margin-top: 1rem; border-radius: 8px; border: 1px solid var(--border-glow);';
                        input.parentNode.insertBefore(preview, input.nextSibling);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

// Onay dialogu
function confirmAction(message) {
    return confirm(message);
}

// AJAX Form Submit
function submitFormAjax(form, successCallback) {
    const formData = new FormData(form);
    const button = form.querySelector('button[type="submit"]');
    const originalText = showLoading(button);
    
    fetch(form.action, {
        method: form.method,
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoading(button, originalText);
        if (data.success) {
            showNotification(data.message, 'success');
            if (successCallback) successCallback(data);
        } else {
            showNotification(data.message, 'danger');
        }
    })
    .catch(error => {
        hideLoading(button, originalText);
        showNotification('Bir hata oluştu', 'danger');
        console.error('Error:', error);
    });
}

// Export fonksiyonlar
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showNotification = showNotification;
window.formatDate = formatDate;
window.confirmAction = confirmAction;
window.submitFormAjax = submitFormAjax;
