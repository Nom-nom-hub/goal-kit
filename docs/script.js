// Scroll animation for elements
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);

    // Observe elements that should animate on scroll
    document.querySelectorAll('.feature-card, .doc-card, .workflow, .installation, .hero, .quickstart, .documentation').forEach(el => {
        el.classList.add('scroll-animate');
        observer.observe(el);
    });

    // Add typing animation to the terminal command
    const terminalCommand = document.querySelector('.terminal-command');
    if (terminalCommand) {
        const originalText = terminalCommand.textContent;
        terminalCommand.textContent = '';
        
        let i = 0;
        const typingSpeed = 50;
        
        const typeWriter = () => {
            if (i < originalText.length) {
                terminalCommand.textContent += originalText.charAt(i);
                i++;
                setTimeout(typeWriter, typingSpeed);
            }
        };
        
        // Start typing after a short delay
        setTimeout(typeWriter, 1000);
    }

    // Add click effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            // Remove ripple after animation
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});