// Theme Management System
class ThemeManager {
    constructor() {
        this.storageKey = 'quiz_app_theme';
        this.init();
    }

    init() {
        // Load saved theme or default to light
        this.currentTheme = this.loadTheme();
        this.applyTheme(this.currentTheme);
        this.setupThemeToggle();
    }

    loadTheme() {
        const saved = localStorage.getItem(this.storageKey);
        return saved || 'light';
    }

    saveTheme(theme) {
        localStorage.setItem(this.storageKey, theme);
        this.currentTheme = theme;
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.updateToggleIcon(theme);
        this.updateThemeStyles(theme);
    }

    updateToggleIcon(theme) {
        const icon = document.querySelector('.fa-sun');
        const moonIcon = document.querySelector('.fa-moon');
        
        if (theme === 'dark') {
            icon.style.display = 'none';
            moonIcon.style.display = 'inline';
        } else {
            icon.style.display = 'inline';
            moonIcon.style.display = 'none';
        }
    }

    updateThemeStyles(theme) {
        // Enhanced dark mode styles
        if (theme === 'dark') {
            document.documentElement.style.setProperty('--bg-primary', '#1a1a2e');
            document.documentElement.style.setProperty('--bg-secondary', '#2d2d2d');
            document.documentElement.style.setProperty('--bg-tertiary', '#404040');
            document.documentElement.style.setProperty('--text-primary', '#ffffff');
            document.documentElement.style.setProperty('--text-secondary', '#b0b0b0');
            document.documentElement.style.setProperty('--text-tertiary', '#808080');
            document.documentElement.style.setProperty('--accent-primary', '#4a9eff');
            document.documentElement.style.setProperty('--accent-secondary', '#5c7cfa');
            document.documentElement.style.setProperty('--border-color', '#404040');
            document.documentElement.style.setProperty('--shadow-color', 'rgba(0, 0, 0, 0.3)');
            document.documentElement.style.setProperty('--card-bg', '#2d2d2d');
            document.documentElement.style.setProperty('--hover-bg', '#404040');
        } else {
            // Light mode colors
            document.documentElement.style.setProperty('--bg-primary', '#ffffff');
            document.documentElement.style.setProperty('--bg-secondary', '#f8f9fa');
            document.documentElement.style.setProperty('--bg-tertiary', '#e9ecef');
            document.documentElement.style.setProperty('--text-primary', '#2c3e50');
            document.documentElement.style.setProperty('--text-secondary', '#6c757d');
            document.documentElement.style.setProperty('--text-tertiary', '#495057');
            document.documentElement.style.setProperty('--accent-primary', '#007bff');
            document.documentElement.style.setProperty('--accent-secondary', '#0056b3');
            document.documentElement.style.setProperty('--border-color', '#dee2e6');
            document.documentElement.style.setProperty('--shadow-color', 'rgba(0, 0, 0, 0.1)');
            document.documentElement.style.setProperty('--card-bg', '#ffffff');
            document.documentElement.style.setProperty('--hover-bg', '#f8f9fa');
        }
    }

    setupThemeToggle() {
        const toggle = document.getElementById('theme-toggle');
        if (!toggle) return;

        // Set initial state
        toggle.checked = this.currentTheme === 'dark';

        toggle.addEventListener('change', () => {
            const newTheme = toggle.checked ? 'dark' : 'light';
            this.switchTheme(newTheme);
        });
    }

    switchTheme(theme) {
        this.applyTheme(theme);
        this.saveTheme(theme);
        this.currentTheme = theme;
        
        // Add transition effect
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    toggle() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.switchTheme(newTheme);
    }
}

// Notification System
class NotificationManager {
    constructor() {
        this.containerId = 'notification-container';
        this.container = null;
        this.init();
    }

    init() {
        this.container = document.getElementById(this.containerId);
    }

    show(message, type = 'info', duration = 5000) {
        if (!this.container) return;

        const notification = document.createElement('div');
        notification.className = `notification ${type} notification-enter`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fa-solid fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
                <span>${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fa-solid fa-times"></i>
                </button>
            </div>
        `;

        this.container.appendChild(notification);

        // Trigger animation
        requestAnimationFrame(() => {
            notification.classList.add('notification-show');
        });

        // Auto-remove
        setTimeout(() => {
            this.remove(notification);
        }, duration);
    }

    remove(notification) {
        if (notification && notification.parentElement) {
            notification.classList.add('notification-exit');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.parentElement.removeChild(notification);
                }
            }, 300);
        }
    }
}

// Initialize managers
const themeManager = new ThemeManager();
const notificationManager = new NotificationManager();

// Global functions for backward compatibility
function showNotification(message, type = 'info') {
    notificationManager.show(message, type);
}

function toggleTheme() {
    themeManager.toggle();
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    themeManager.init();
    notificationManager.init();
});
