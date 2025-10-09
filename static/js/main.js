/**
 * Project Pilgrims Hotel and Restaurant
 * Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    initializeMobileNav();
    
    // Alert Dismissal
    initializeAlertDismissal();
    
    // Smooth scrolling for anchor links
    initializeSmoothScrolling();
    
    // Initialize any dropdown menus
    initializeDropdowns();
    
    // Form validations
    initializeFormValidations();
    
    // Add scroll animation classes
    initializeScrollAnimations();
});

/**
 * Mobile Navigation functionality
 * Note: Main mobile navigation is handled in base.html to avoid conflicts
 */
function initializeMobileNav() {
    // Mobile navigation is handled in base.html
    // This function is kept for compatibility but does not interfere
    console.log('Mobile navigation initialized in base.html');
}

/**
 * Alert dismissal functionality
 */
function initializeAlertDismissal() {
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    
    if (alertCloseButtons.length > 0) {
        alertCloseButtons.forEach(button => {
            button.addEventListener('click', function() {
                const alert = this.closest('[role="alert"]');
                if (alert) {
                    // Add fade-out animation
                    alert.style.transition = 'opacity 300ms ease-in-out';
                    alert.style.opacity = '0';
                    
                    // Remove the element after animation completes
                    setTimeout(() => {
                        alert.remove();
                    }, 300);
                }
            });
        });
    }
}

/**
 * Smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                // Get height of sticky header if it exists
                const header = document.querySelector('header.sticky');
                const headerHeight = header ? header.offsetHeight : 0;
                
                // Calculate target position with offset for header
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                // Smooth scroll to target
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Dropdown menu functionality
 */
function initializeDropdowns() {
    const dropdownButtons = document.querySelectorAll('.dropdown-toggle');
    
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdownContent = this.nextElementSibling;
            
            // Toggle current dropdown
            dropdownContent.classList.toggle('hidden');
            
            // Close other dropdowns
            dropdownButtons.forEach(otherButton => {
                if (otherButton !== button) {
                    const otherContent = otherButton.nextElementSibling;
                    if (otherContent && !otherContent.classList.contains('hidden')) {
                        otherContent.classList.add('hidden');
                    }
                }
            });
            
            // Close dropdown when clicking outside
            const closeDropdown = function(event) {
                if (!button.contains(event.target) && !dropdownContent.contains(event.target)) {
                    dropdownContent.classList.add('hidden');
                    document.removeEventListener('click', closeDropdown);
                }
            };
            
            if (!dropdownContent.classList.contains('hidden')) {
                setTimeout(() => {
                    document.addEventListener('click', closeDropdown);
                }, 100);
            }
        });
    });
}

/**
 * Form validation functionality
 */
function initializeFormValidations() {
    const forms = document.querySelectorAll('form[data-validate="true"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Check all required inputs
            form.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    highlightInvalidInput(input);
                } else {
                    removeInvalidHighlight(input);
                    
                    // Validate email fields
                    if (input.type === 'email' && !isValidEmail(input.value)) {
                        isValid = false;
                        highlightInvalidInput(input, 'Please enter a valid email address');
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Live validation as user types
        form.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('input', function() {
                if (this.hasAttribute('required') && this.value.trim()) {
                    removeInvalidHighlight(this);
                    
                    // Validate email fields
                    if (this.type === 'email' && !isValidEmail(this.value)) {
                        highlightInvalidInput(this, 'Please enter a valid email address');
                    }
                }
            });
        });
    });
    
    // Newsletter form special handling
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            
            if (emailInput && emailInput.value && isValidEmail(emailInput.value)) {
                // Here you would typically send via AJAX
                // For now, just show success feedback
                const successMessage = document.createElement('div');
                successMessage.className = 'text-green-500 mt-2 text-sm';
                successMessage.textContent = 'Thank you for subscribing!';
                
                // Remove any existing messages
                const existingMessage = emailInput.parentNode.querySelector('.text-green-500, .text-red-500');
                if (existingMessage) {
                    existingMessage.remove();
                }
                
                emailInput.parentNode.appendChild(successMessage);
                emailInput.value = '';
                
                // Remove success message after a delay
                setTimeout(() => {
                    successMessage.remove();
                }, 3000);
            } else if (emailInput) {
                const errorMessage = document.createElement('div');
                errorMessage.className = 'text-red-500 mt-2 text-sm';
                errorMessage.textContent = 'Please enter a valid email address';
                
                // Remove any existing messages
                const existingMessage = emailInput.parentNode.querySelector('.text-green-500, .text-red-500');
                if (existingMessage) {
                    existingMessage.remove();
                }
                
                emailInput.parentNode.appendChild(errorMessage);
            }
        });
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Highlight invalid form input
 */
function highlightInvalidInput(input, message) {
    input.classList.add('border-red-500', 'bg-red-50');
    
    // Add error message if needed
    if (message && !input.nextElementSibling?.classList.contains('error-message')) {
        const errorSpan = document.createElement('span');
        errorSpan.className = 'text-red-500 text-sm mt-1 error-message';
        errorSpan.textContent = message;
        input.parentNode.insertBefore(errorSpan, input.nextSibling);
    }
}

/**
 * Remove invalid highlight from form input
 */
function removeInvalidHighlight(input) {
    input.classList.remove('border-red-500', 'bg-red-50');
    
    // Remove any error message
    const errorMessage = input.nextElementSibling;
    if (errorMessage?.classList.contains('error-message')) {
        errorMessage.remove();
    }
}

/**
 * Initialize scroll animations
 */
function initializeScrollAnimations() {
    // Elements to animate when they come into view
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length > 0) {
        // Set initial state
        animatedElements.forEach(el => {
            el.classList.add('opacity-0', 'translate-y-8');
            el.style.transition = 'opacity 600ms ease-out, transform 600ms ease-out';
        });
        
        // Check if elements are visible and trigger animations
        const checkIfInView = () => {
            animatedElements.forEach(el => {
                const rect = el.getBoundingClientRect();
                const windowHeight = window.innerHeight || document.documentElement.clientHeight;
                
                if (rect.top <= windowHeight * 0.85 && !el.classList.contains('has-animated')) {
                    el.classList.remove('opacity-0', 'translate-y-8');
                    el.classList.add('has-animated');
                }
            });
        };
        
        // Run once on load and then on scroll
        checkIfInView();
        window.addEventListener('scroll', checkIfInView);
    }
}