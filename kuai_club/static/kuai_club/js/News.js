        class NewsSlider {
            constructor() {
                this.currentSlide = 0;
                this.cards = document.querySelectorAll('.news-card');
                this.backgroundSlides = document.querySelectorAll('.background-slide');
                this.indicators = document.querySelectorAll('.indicator');
                this.totalSlides = this.cards.length;
                this.autoPlayInterval = null;
                this.isTransitioning = false;
                
                this.init();
            }

            init() {
                this.setupEventListeners();
                this.startAutoPlay();
                this.updateSlider();
            }

            setupEventListeners() {
                // Navigation buttons
                document.getElementById('prevBtn').addEventListener('click', () => this.prevSlide());
                document.getElementById('nextBtn').addEventListener('click', () => this.nextSlide());

                // Indicators
                this.indicators.forEach((indicator, index) => {
                    indicator.addEventListener('click', () => this.goToSlide(index));
                });

                // Pause auto-play on hover
                const section = document.querySelector('.news-slider-section');
                section.addEventListener('mouseenter', () => this.pauseAutoPlay());
                section.addEventListener('mouseleave', () => this.startAutoPlay());

                // Keyboard navigation
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'ArrowLeft') this.prevSlide();
                    if (e.key === 'ArrowRight') this.nextSlide();
                });

                // Touch/swipe support
                let startX = 0;
                let endX = 0;
                
                section.addEventListener('touchstart', (e) => {
                    startX = e.touches[0].clientX;
                });
                
                section.addEventListener('touchend', (e) => {
                    endX = e.changedTouches[0].clientX;
                    this.handleSwipe(startX, endX);
                });
            }

            handleSwipe(startX, endX) {
                const threshold = 50;
                const diff = startX - endX;
                
                if (Math.abs(diff) > threshold) {
                    if (diff > 0) {
                        this.nextSlide();
                    } else {
                        this.prevSlide();
                    }
                }
            }

            nextSlide() {
                if (this.isTransitioning) return;
                this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
                this.updateSlider();
            }

            prevSlide() {
                if (this.isTransitioning) return;
                this.currentSlide = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
                this.updateSlider();
            }

            goToSlide(index) {
                if (this.isTransitioning || index === this.currentSlide) return;
                this.currentSlide = index;
                this.updateSlider();
            }

            updateSlider() {
                this.isTransitioning = true;
                
                // Update cards
                this.cards.forEach((card, index) => {
                    card.classList.remove('active', 'prev', 'next');
                    
                    if (index === this.currentSlide) {
                        card.classList.add('active');
                    } else if (index === (this.currentSlide - 1 + this.totalSlides) % this.totalSlides) {
                        card.classList.add('prev');
                    } else if (index === (this.currentSlide + 1) % this.totalSlides) {
                        card.classList.add('next');
                    }
                });

                // Update background slides with fade effect
                this.backgroundSlides.forEach((slide, index) => {
                    slide.classList.remove('active');
                    if (index === this.currentSlide) {
                        slide.classList.add('active');
                    }
                });

                // Update indicators
                this.indicators.forEach((indicator, index) => {
                    indicator.classList.remove('active');
                    if (index === this.currentSlide) {
                        indicator.classList.add('active');
                    }
                });

                // Reset transition flag after animation completes
                setTimeout(() => {
                    this.isTransitioning = false;
                }, 800);
            }

            startAutoPlay() {
                this.pauseAutoPlay();
                this.autoPlayInterval = setInterval(() => {
                    this.nextSlide();
                }, 5000); // Change slide every 5 seconds
            }

            pauseAutoPlay() {
                if (this.autoPlayInterval) {
                    clearInterval(this.autoPlayInterval);
                    this.autoPlayInterval = null;
                }
            }

            destroy() {
                this.pauseAutoPlay();
                // Remove event listeners if needed
            }
        }

        // Initialize the slider when the page loads
        document.addEventListener('DOMContentLoaded', () => {
            new NewsSlider();
        });

        // Add smooth scrolling and performance optimizations
        document.addEventListener('scroll', () => {
            requestAnimationFrame(() => {
                // Add any scroll-based animations here if needed
            });
        });
  