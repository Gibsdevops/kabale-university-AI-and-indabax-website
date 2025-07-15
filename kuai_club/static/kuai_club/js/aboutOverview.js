// static/js/about_section.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize About Section
    initializeAboutSection();
});

function initializeAboutSection() {
    // Add scroll animations
    addScrollAnimations();
    
    // Add hover effects
    addHoverEffects();
    
    // Add parallax effect
    addParallaxEffect();
    
    // Add card interactions
    addCardInteractions();
}

// Scroll Animation Observer
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all about cards and headings
    const aboutCards = document.querySelectorAll('.about-card');
    const aboutHeadings = document.querySelectorAll('.about-heading');
    
    aboutCards.forEach(card => observer.observe(card));
    aboutHeadings.forEach(heading => observer.observe(heading));
}

// Enhanced Hover Effects
function addHoverEffects() {
    const aboutCards = document.querySelectorAll('.about-card');
    
    aboutCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Add subtle glow effect
            this.style.boxShadow = '0 15px 30px rgba(0, 123, 255, 0.2)';
            
            // Scale image slightly
            const image = this.querySelector('.about-image, .about-image-placeholder');
            if (image) {
                image.style.transform = 'scale(1.05)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            // Reset effects
            this.style.boxShadow = '';
            
            const image = this.querySelector('.about-image, .about-image-placeholder');
            if (image) {
                image.style.transform = 'scale(1)';
            }
        });
    });
}

// Parallax Effect for Background
function addParallaxEffect() {
    const aboutSection = document.querySelector('.about-overview-section');
    
    if (!aboutSection) return;
    
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const sectionTop = aboutSection.offsetTop;
        const sectionHeight = aboutSection.offsetHeight;
        const windowHeight = window.innerHeight;
        
        // Check if section is in viewport
        if (scrolled + windowHeight > sectionTop && scrolled < sectionTop + sectionHeight) {
            const parallaxSpeed = 0.5;
            const yPos = -(scrolled - sectionTop) * parallaxSpeed;
            
            // Apply parallax to background pattern
            const beforeElement = aboutSection.querySelector('::before');
            if (beforeElement) {
                aboutSection.style.backgroundPosition = `0 ${yPos}px`;
            }
        }
    });
}

// Card Interactions and Animations
function addCardInteractions() {
    const aboutCards = document.querySelectorAll('.about-card');
    
    aboutCards.forEach((card, index) => {
        // Add staggered animation delay
        card.style.animationDelay = `${index * 0.1}s`;
        
        // Add click ripple effect
        card.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
    });
}

// Create Ripple Effect
function createRippleEffect(event, element) {
    const rect = element.getBoundingClientRect();
    const ripple = document.createElement('span');
    const size = Math.max(rect.width, rect.height);
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (event.clientX - rect.left - size / 2) + 'px';
    ripple.style.top = (event.clientY - rect.top - size / 2) + 'px';
    ripple.classList.add('ripple');
    
    // Add ripple styles
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.background = 'rgba(0, 123, 255, 0.3)';
    ripple.style.transform = 'scale(0)';
    ripple.style.animation = 'ripple 0.6s linear';
    ripple.style.pointerEvents = 'none';
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    // Remove ripple after animation
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add CSS for ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Counter Animation for Statistics (if needed)
function animateCounters() {
    const counters = document.querySelectorAll('.about-counter');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const increment = target / 100;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        // Start animation when element is in view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(counter);
                }
            });
        });
        
        observer.observe(counter);
    });
}

// Smooth Scroll for Learn More Button
document.addEventListener('DOMContentLoaded', function() {
    const learnMoreBtn = document.querySelector('.about-learn-more-btn');
    
    if (learnMoreBtn) {
        learnMoreBtn.addEventListener('click', function(e) {
            // Add loading state
            this.style.transform = 'scale(0.95)';
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }
});

// Responsive Image Loading
function handleResponsiveImages() {
    const images = document.querySelectorAll('.about-image');
    
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        img.addEventListener('error', function() {
            // Create fallback icon if image fails to load
            const placeholder = document.createElement('div');
            placeholder.className = 'about-image-placeholder';
            placeholder.innerHTML = '<i class="fas fa-image"></i>';
            this.parentNode.replaceChild(placeholder, this);
        });
    });
}

// Initialize responsive images
document.addEventListener('DOMContentLoaded', handleResponsiveImages);

// Performance optimization: Throttle scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Apply throttling to scroll events
window.addEventListener('scroll', throttle(addParallaxEffect, 16));

// Accessibility improvements
function addAccessibilityFeatures() {
    const aboutCards = document.querySelectorAll('.about-card');
    
    aboutCards.forEach(card => {
        // Add keyboard navigation
        card.setAttribute('tabindex', '0');
        
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // Add focus styles
        card.addEventListener('focus', function() {
            this.style.outline = '2px solid #007bff';
            this.style.outlineOffset = '2px';
        });
        
        card.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', addAccessibilityFeatures);