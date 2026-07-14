/**
 * Smart Expense Tracker - Complete JavaScript
 * Includes Dark Mode, Animations, and Interactive Features
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Smart Expense Tracker Loaded!');

    // ============================================
    // DARK MODE TOGGLE - FIXED
    // ============================================
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;
    const footerThemeIcon = document.getElementById('footerThemeIcon');
    const footerThemeText = document.getElementById('footerThemeText');

    // Function to update dark mode
    function setTheme(theme) {
        htmlElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);

        // Update button icon
        const icon = darkModeToggle?.querySelector('i');
        if (icon) {
            if (theme === 'dark') {
                icon.className = 'fas fa-sun';
                icon.style.color = '#fee140';
            } else {
                icon.className = 'fas fa-moon';
                icon.style.color = '';
            }
        }

        // Update footer
        if (footerThemeIcon) {
            if (theme === 'dark') {
                footerThemeIcon.className = 'fas fa-moon';
                footerThemeIcon.style.color = '#fee140';
            } else {
                footerThemeIcon.className = 'fas fa-sun';
                footerThemeIcon.style.color = '#f5576c';
            }
        }
        if (footerThemeText) {
            footerThemeText.textContent = theme === 'dark' ? 'Dark Mode' : 'Light Mode';
        }

        console.log(`🌓 Theme changed to: ${theme}`);
    }

    // Check saved preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    // Toggle button click handler
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            setTheme(newTheme);

            // Animate the button
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = '';
            }, 500);
        });
    }

    // ============================================
    // NAVBAR SCROLL EFFECT
    // ============================================
    const navbar = document.getElementById('mainNav');
    if (navbar) {
        window.addEventListener('scroll', function() {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    // ============================================
    // SCROLL ANIMATIONS
    // ============================================
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.card, .stat-card, .welcome-card').forEach(el => {
        observer.observe(el);
    });

    // ============================================
    // AUTO-DISMISS ALERTS
    // ============================================
    document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
        setTimeout(() => {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) closeBtn.click();
        }, 5000);
    });

    // ============================================
    // KEYBOARD SHORTCUTS
    // ============================================
    document.addEventListener('keydown', function(e) {
        // Ctrl + N: New Expense
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            window.location.href = '/add';
        }
        // Ctrl + I: Income Manager
        if (e.ctrlKey && e.key === 'i') {
            e.preventDefault();
            window.location.href = '/income';
        }
        // Ctrl + B: Budget Planner
        if (e.ctrlKey && e.key === 'b') {
            e.preventDefault();
            window.location.href = '/budget';
        }
        // Ctrl + H: Home
        if (e.ctrlKey && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/';
        }
        // Ctrl + D: Toggle Dark Mode
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            if (darkModeToggle) darkModeToggle.click();
        }
    });

    // ============================================
    // DELETE CONFIRMATIONS
    // ============================================
    document.querySelectorAll('a[onclick*="confirm"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('⚠️ Are you sure you want to delete this item?\n\nThis action cannot be undone!')) {
                e.preventDefault();
                return false;
            }
        });
    });

    // ============================================
    // INCOME FORM - Toggle Recurring
    // ============================================
    const recurringCheckbox = document.getElementById('is_recurring');
    const frequencyDiv = document.getElementById('frequencyDiv');

    if (recurringCheckbox && frequencyDiv) {
        recurringCheckbox.addEventListener('change', function() {
            frequencyDiv.style.display = this.checked ? 'block' : 'none';
        });
    }

    // ============================================
    // DATE PICKER DEFAULTS
    // ============================================
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = today;
        }
        input.setAttribute('max', today);
    });

    // ============================================
    // LIVE SEARCH
    // ============================================
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let timeoutId;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                this.closest('form').submit();
            }, 500);
        });
    }

    console.log('✅ All features initialized!');
    console.log('💡 Keyboard Shortcuts:');
    console.log('  Ctrl+N - Add Expense');
    console.log('  Ctrl+I - Income Manager');
    console.log('  Ctrl+B - Budget Planner');
    console.log('  Ctrl+H - Home');
    console.log('  Ctrl+D - Toggle Dark Mode');
});