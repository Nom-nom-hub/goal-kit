// JavaScript for Goal-Dev-Spec website

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all website features
    initNavigation();
    initSmoothScrolling();
    initScrollAnimations();
    initCodeBlockHighlighting();
    initHamburgerMenu();
    initScrollToTop();
});

// Navigation functionality
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Close mobile menu if open
            const hamburger = document.querySelector('.hamburger');
            const navMenu = document.querySelector('.nav-menu');
            
            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
            }
        });
    });
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear');
            }
        });
    }, observerOptions);
    
    // Observe elements that should fade in
    document.querySelectorAll('.philosophy-card, .step, .feature-card, .install-option').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

// Code block highlighting
function initCodeBlockHighlighting() {
    // Add syntax highlighting effect to code blocks
    document.querySelectorAll('pre code').forEach(block => {
        // This is a simplified syntax highlighting
        // In a real implementation, you might use a library like Prism.js or highlight.js
        highlightCodeBlock(block);
    });
}

function highlightCodeBlock(block) {
    // Get the text content
    let code = block.innerHTML;
    
    // Simple syntax highlighting for demonstration
    code = code.replace(/(goal|cd|pip)/g, '<mark>$1</mark>');
    code = code.replace(/(".*?")/g, '<span class="string">$1</span>');
    code = code.replace(/(init|create|plan|tasks|track|list|show)/g, '<span class="command">$1</span>');
    
    block.innerHTML = code;
}

// Hamburger menu for mobile
function initHamburgerMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            
            // Animate hamburger
            hamburger.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    }
}

// Scroll to top button
function initScrollToTop() {
    // Create scroll to top button
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollToTopBtn.className = 'scroll-to-top';
    scrollToTopBtn.title = 'Scroll to top';
    document.body.appendChild(scrollToTopBtn);
    
    // Hide button initially
    scrollToTopBtn.style.display = 'none';
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollToTopBtn.style.display = 'block';
        } else {
            scrollToTopBtn.style.display = 'none';
        }
    });
    
    // Scroll to top functionality
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Additional interactive features
function initInteractiveFeatures() {
    // Feature card hover effects
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
    
    // Philosophy card hover effects
    const philosophyCards = document.querySelectorAll('.philosophy-card');
    philosophyCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

// Initialize interactive features after DOM is fully loaded
document.addEventListener('DOMContentLoaded', initInteractiveFeatures);

// Analytics (placeholder for future implementation)
function trackEvent(eventName, properties = {}) {
    // Placeholder for analytics tracking
    // In a real implementation, this would send data to an analytics service
    console.log(`Event tracked: ${eventName}`, properties);
}

// Form handling (for potential contact forms)
function initFormHandling() {
    const contactForms = document.querySelectorAll('form');
    contactForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const formObject = Object.fromEntries(formData);
            
            // Placeholder for form submission
            trackEvent('form_submit', { formType: this.dataset.formType || 'unknown' });
            
            // Show success message (this would be replaced with actual submission)
            alert('Thank you for your message! (This is a demo)');
            
            // Reset form
            this.reset();
        });
    });
}

// Initialize form handling
document.addEventListener('DOMContentLoaded', initFormHandling);

// Theme toggle functionality (for dark/light theme)
function initThemeToggle() {
    const themeToggle = document.createElement('button');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    themeToggle.className = 'theme-toggle';
    themeToggle.title = 'Toggle theme';
    
    // Check for saved theme preference or respect OS preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
    
    // Position it in the header
    const header = document.querySelector('.header');
    if (header) {
        header.appendChild(themeToggle);
    }
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update icon based on theme
        const icon = themeToggle.querySelector('i');
        if (newTheme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
        
        trackEvent('theme_toggle', { theme: newTheme });
    });
}

// Initialize theme toggle
document.addEventListener('DOMContentLoaded', initThemeToggle);

// Utility function to check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Progress bar for page scroll (optional visual element)
function initProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.body.offsetHeight;
        const winHeight = window.innerHeight;
        const scrollPercent = scrollTop / (docHeight - winHeight);
        const scrollPercentRounded = Math.round(scrollPercent * 100);
        
        progressBar.style.width = `${scrollPercentRounded}%`;
    });
}

// Initialize progress bar
document.addEventListener('DOMContentLoaded', initProgressBar);