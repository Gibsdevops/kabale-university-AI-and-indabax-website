
        document.addEventListener("DOMContentLoaded", function () {
            const cards = document.querySelectorAll("#partners .card");
            
            // Enhanced animation with stagger effect
            const animateCards = () => {
                cards.forEach((card, index) => {
                    setTimeout(() => {
                        card.classList.add('animate');
                    }, index * 150);
                });
            };

            // Intersection Observer for scroll-triggered animations
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCards();
                        observer.disconnect();
                    }
                });
            }, observerOptions);

            const partnersSection = document.querySelector('#partners');
            if (partnersSection) {
                observer.observe(partnersSection);
            }

            // Add hover effects for better interactivity
            cards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-10px) scale(1.02)';
                });
                
                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0) scale(1)';
                });
            });

            // Add click tracking for analytics (optional)
            const websiteLinks = document.querySelectorAll('#partners .website-link');
            websiteLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    // Add analytics tracking here if needed
                    console.log('Partner website clicked:', this.href);
                });
            });
        });
 