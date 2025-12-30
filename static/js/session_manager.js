/**
 * Session Management & Timeout Handler
 * Monitors user activity and warns before session timeout
 */

class SessionManager {
    constructor(options = {}) {
        this.sessionTimeout = options.sessionTimeout || 30 * 60 * 1000; // 30 minutes in ms
        this.warningTimeout = options.warningTimeout || 25 * 60 * 1000; // Warn at 25 minutes
        this.checkInterval = options.checkInterval || 60 * 1000; // Check every minute
        
        this.warningShown = false;
        this.lastActivityTime = Date.now();
        this.timeoutId = null;
        this.warningTimeoutId = null;
        
        this.init();
    }
    
    init() {
        // Track user activity
        document.addEventListener('click', () => this.resetInactivityTimer());
        document.addEventListener('keypress', () => this.resetInactivityTimer());
        document.addEventListener('mousemove', () => this.resetInactivityTimer());
        document.addEventListener('scroll', () => this.resetInactivityTimer());
        
        // Start monitoring
        this.startSessionMonitor();
    }
    
    resetInactivityTimer() {
        this.lastActivityTime = Date.now();
        
        // Hide warning if it was shown
        if (this.warningShown) {
            this.hideSessionWarning();
        }
    }
    
    startSessionMonitor() {
        this.timeoutId = setInterval(() => {
            const inactiveTime = Date.now() - this.lastActivityTime;
            
            // Show warning when approaching timeout
            if (inactiveTime >= this.warningTimeout && !this.warningShown) {
                this.showSessionWarning();
            }
            
            // Force logout on timeout
            if (inactiveTime >= this.sessionTimeout) {
                this.handleSessionTimeout();
            }
        }, this.checkInterval);
    }
    
    showSessionWarning() {
        this.warningShown = true;
        
        // Create warning modal
        const warningHTML = `
            <div class="modal fade" id="sessionWarningModal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content border-warning">
                        <div class="modal-header bg-warning bg-opacity-10">
                            <h5 class="modal-title">
                                <i class="bi bi-exclamation-triangle text-warning"></i>
                                Session Timeout Warning
                            </h5>
                        </div>
                        <div class="modal-body">
                            <p class="mb-2">
                                <strong>Your session is about to expire!</strong>
                            </p>
                            <p class="text-muted mb-3">
                                You will be automatically logged out in <span id="timeRemaining">5</span> minutes due to inactivity.
                            </p>
                            <p class="text-muted small">
                                Click "Stay Logged In" to continue your session or "Logout Now" to logout manually.
                            </p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" id="logoutBtn">
                                <i class="bi bi-box-arrow-right"></i> Logout Now
                            </button>
                            <button type="button" class="btn btn-primary" id="continueBtn">
                                <i class="bi bi-check-circle"></i> Stay Logged In
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if present
        const existingModal = document.getElementById('sessionWarningModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', warningHTML);
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('sessionWarningModal'));
        modal.show();
        
        // Bind events
        document.getElementById('continueBtn').addEventListener('click', () => {
            modal.hide();
            this.resetInactivityTimer();
        });
        
        document.getElementById('logoutBtn').addEventListener('click', () => {
            window.location.href = '/admin/logout';
        });
        
        // Start countdown timer
        this.startCountdownTimer();
    }
    
    hideSessionWarning() {
        const warningModal = document.getElementById('sessionWarningModal');
        if (warningModal) {
            const modal = bootstrap.Modal.getInstance(warningModal);
            if (modal) {
                modal.hide();
            }
            warningModal.remove();
        }
        this.warningShown = false;
    }
    
    startCountdownTimer() {
        let timeRemaining = 5; // 5 minutes
        const countdownInterval = setInterval(() => {
            timeRemaining--;
            const element = document.getElementById('timeRemaining');
            if (element) {
                element.textContent = timeRemaining;
            }
            
            if (timeRemaining <= 0) {
                clearInterval(countdownInterval);
            }
        }, 60000); // Update every minute
    }
    
    handleSessionTimeout() {
        // Hide warning if shown
        this.hideSessionWarning();
        
        // Show timeout alert
        const alertHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert" 
                 style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
                <i class="bi bi-exclamation-circle"></i>
                <strong>Session Expired!</strong>
                Your session has expired due to inactivity. You will be redirected to login page.
            </div>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', alertHTML);
        
        // Redirect to login after 3 seconds
        setTimeout(() => {
            window.location.href = '/admin/login';
        }, 3000);
    }
    
    destroy() {
        if (this.timeoutId) {
            clearInterval(this.timeoutId);
        }
        if (this.warningTimeoutId) {
            clearTimeout(this.warningTimeoutId);
        }
        this.hideSessionWarning();
    }
}

// Initialize session manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on admin pages
    if (window.location.pathname.startsWith('/admin')) {
        window.sessionManager = new SessionManager({
            sessionTimeout: 30 * 60 * 1000,    // 30 minutes
            warningTimeout: 25 * 60 * 1000,    // Warn at 25 minutes
            checkInterval: 60 * 1000             // Check every minute
        });
    }
});
