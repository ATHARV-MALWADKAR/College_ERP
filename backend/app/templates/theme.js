// Theme management utilities
class ThemeManager {
    constructor() {
        this.themeKey = 'theme';
        this.lightTheme = 'light';
        this.darkTheme = 'dark';
        this.init();
    }

    init() {
        // Apply saved theme on page load
        this.applyTheme(this.getSavedTheme());

        // Listen for system theme changes
        this.watchSystemTheme();
    }

    getSavedTheme() {
        return localStorage.getItem(this.themeKey) || this.getSystemTheme();
    }

    getSystemTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches
            ? this.darkTheme
            : this.lightTheme;
    }

    setTheme(theme) {
        localStorage.setItem(this.themeKey, theme);
        this.applyTheme(theme);
        this.dispatchThemeChange(theme);
    }

    toggleTheme() {
        const currentTheme = this.getSavedTheme();
        const newTheme = currentTheme === this.darkTheme ? this.lightTheme : this.darkTheme;
        this.setTheme(newTheme);
    }

    applyTheme(theme) {
        const root = document.documentElement;

        if (theme === this.darkTheme) {
            root.classList.add('dark');
            root.classList.remove('light');
        } else {
            root.classList.add('light');
            root.classList.remove('dark');
        }

        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', theme === this.darkTheme ? '#0f172a' : '#ffffff');
        }
    }

    watchSystemTheme() {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            // Only auto-switch if no manual preference is saved
            if (!localStorage.getItem(this.themeKey)) {
                this.setTheme(e.matches ? this.darkTheme : this.lightTheme);
            }
        });
    }

    dispatchThemeChange(theme) {
        window.dispatchEvent(new CustomEvent('themeChange', { detail: { theme } }));
    }

    onThemeChange(callback) {
        window.addEventListener('themeChange', (e) => callback(e.detail.theme));
    }
}

// Initialize theme manager globally
window.themeManager = new ThemeManager();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}