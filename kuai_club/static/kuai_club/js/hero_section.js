// static/js/hero.js
document.addEventListener('DOMContentLoaded', function() {
    const heroCarousel = document.getElementById('heroCarousel');
    
    if (heroCarousel) {
        // Initialize the carousel with options
        const carousel = new bootstrap.Carousel(heroCarousel, {
            interval: 5000, // Change slide every 5 seconds
            pause: 'hover', // Pause on hover
            wrap: true, // Continuously cycle
            ride: 'carousel' // Autoplay
        });
        
        // Add smooth transition effect
        heroCarousel.addEventListener('slide.bs.carousel', function(e) {
            const nextSlide = e.relatedTarget;
            const content = nextSlide.querySelector('.hero-content');
            
            // Reset animations for the upcoming slide
            if (content) {
                content.style.opacity = 0;
                content.style.transform = 'translateY(20px)';
            }
        });
        
        heroCarousel.addEventListener('slid.bs.carousel', function(e) {
            const activeSlide = e.relatedTarget;
            const content = activeSlide.querySelector('.hero-content');
            
            // Animate the content when slide is shown
            if (content) {
                content.style.transition = 'all 0.8s ease';
                content.style.opacity = 1;
                content.style.transform = 'translateY(0)';
                
                // Animate each child element with a delay
                const children = content.children;
                Array.from(children).forEach((child, index) => {
                    child.style.transition = `all 0.8s ease ${index * 0.2}s`;
                    child.style.opacity = 1;
                    child.style.transform = 'translateY(0)';
                });
            }
        });
        
        // Force initial animation on page load
        const firstSlide = heroCarousel.querySelector('.carousel-item.active');
        if (firstSlide) {
            const content = firstSlide.querySelector('.hero-content');
            if (content) {
                content.style.opacity = 1;
                content.style.transform = 'translateY(0)';
            }
        }
    }
});


// Add this to your JS
document.addEventListener('DOMContentLoaded', function() {
  const colorStripe = document.querySelector('.color-stripe');
  
  if (colorStripe) {
    // Make animation faster on mobile
    function adjustStripeSpeed() {
      const speed = window.innerWidth < 768 ? 6 : 10;
      colorStripe.style.animationDuration = `${speed}s`;
    }
    
    adjustStripeSpeed();
    window.addEventListener('resize', adjustStripeSpeed);
  }
});