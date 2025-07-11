// University Navbar JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Navbar scroll effect
    function handleNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    // Enhanced hover functionality for navigation items
    function initializeNavHover() {
    const navItems = document.querySelectorAll('.nav-hover-content');
    let hoverTimeout;

    navItems.forEach(item => {
        const targetId = item.getAttribute('data-hover-target');
        const targetPanel = document.getElementById(targetId);
        if (!targetPanel) return;

        // Show on hover in
        item.addEventListener('mouseenter', function () {
            clearTimeout(hoverTimeout);
            targetPanel.style.display = 'block';
            targetPanel.classList.add('show');
        });

        // Hide on hover out
        item.addEventListener('mouseleave', function () {
            hoverTimeout = setTimeout(() => {
                if (!targetPanel.matches(':hover')) {
                    targetPanel.style.display = 'none';
                    targetPanel.classList.remove('show');
                }
            }, 200);
        });

        // Keep showing if mouse enters the panel
        targetPanel.addEventListener('mouseenter', function () {
            clearTimeout(hoverTimeout);
            targetPanel.style.display = 'block';
            targetPanel.classList.add('show');
        });

        // Hide when mouse leaves the panel
        targetPanel.addEventListener('mouseleave', function () {
            hoverTimeout = setTimeout(() => {
                targetPanel.style.display = 'none';
                targetPanel.classList.remove('show');
            }, 200);
        });
    });
}

    // Mobile menu enhancements
    function initializeMobileMenu() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        const navItems = document.querySelectorAll('.nav-hover-content');

        if (window.innerWidth <= 991.98) {
            navItems.forEach(item => {
                const targetId = item.getAttribute('data-hover-target');
                const targetPanel = document.getElementById(targetId);
                
                if (targetPanel) {
                    // Convert hover to click for mobile
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        
                        // Toggle panel visibility
                        if (targetPanel.classList.contains('show')) {
                            targetPanel.classList.remove('show');
                        } else {
                            // Hide other panels
                            document.querySelectorAll('.hover-content-panel').forEach(panel => {
                                panel.classList.remove('show');
                            });
                            targetPanel.classList.add('show');
                        }
                    });
                }
            });
        }
    }

    // Search functionality
    function initializeSearch() {
        const searchModal = document.getElementById('searchModal');
        const searchInput = searchModal.querySelector('input[type="text"]');
        const searchForm = searchModal.querySelector('form');

        // Focus input when modal opens
        searchModal.addEventListener('shown.bs.modal', function() {
            searchInput.focus();
        });

        // Handle search form submission
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            
            if (query) {
                // Here you would typically send the search query to your backend
                console.log('Searching for:', query);
                
                // Close modal and show loading state
                const modal = bootstrap.Modal.getInstance(searchModal);
                modal.hide();
                
                // You can implement actual search functionality here
                // For example, redirect to search results page
                // window.location.href = `/search?q=${encodeURIComponent(query)}`;
            }
        });

        // Clear search when modal is hidden
        searchModal.addEventListener('hidden.bs.modal', function() {
            searchInput.value = '';
        });
    }

    // Active menu item highlighting
    function highlightActiveMenuItem() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && (currentPath === href || (href !== '/' && currentPath.startsWith(href)))) {
                link.classList.add('active');
            }
        });
    }

    // Smooth animations for dropdown links
    function initializeDropdownAnimations() {
        const dropdownLinks = document.querySelectorAll('.hover-content-panel a');
        
        dropdownLinks.forEach((link, index) => {
            link.style.animationDelay = `${index * 0.05}s`;
            
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(5px)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
            });
        });
    }

    // Quick Links dropdown functionality
    function initializeQuickLinks() {
        const quickLinksDropdown = document.querySelector('.quick-links-dropdown');
        if (quickLinksDropdown) {
            const links = quickLinksDropdown.querySelectorAll('.dropdown-item');
            
            links.forEach(link => {
                link.addEventListener('click', function(e) {
                    // Add loading state
                    const originalText = this.textContent;
                    this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                    
                    // Simulate loading (remove this in production)
                    setTimeout(() => {
                        this.textContent = originalText;
                    }, 1000);
                });
            });
        }
    }

    // Social media links enhancement
    function initializeSocialLinks() {
        const socialLinks = document.querySelectorAll('.social-link');
        
        socialLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Add a subtle animation when clicked
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }

    // Contact links enhancement
    function initializeContactLinks() {
        const emailLinks = document.querySelectorAll('a[href^="mailto:"]');
        const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
        
        emailLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Optional: Track email clicks
                console.log('Email clicked:', this.href);
            });
        });
        
        phoneLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Optional: Track phone clicks
                console.log('Phone clicked:', this.href);
            });
        });
    }

    // Performance optimization - throttle scroll events
    function throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Initialize all functionality
    function init() {
        initializeNavHover();
        initializeMobileMenu();
        initializeSearch();
        highlightActiveMenuItem();
        initializeDropdownAnimations();
        initializeQuickLinks();
        initializeSocialLinks();
        initializeContactLinks();
        
        // Add scroll event listener with throttling
        window.addEventListener('scroll', throttle(handleNavbarScroll, 16));
        
        // Handle window resize
        window.addEventListener('resize', throttle(() => {
            initializeMobileMenu();
        }, 250));
    }

    // Start everything
    init();

    // Accessibility improvements
    document.addEventListener('keydown', function(e) {
        // ESC key closes all dropdowns
        if (e.key === 'Escape') {
            document.querySelectorAll('.hover-content-panel').forEach(panel => {
                panel.classList.remove('show');
            });
        }
        
        // Enter key on nav items opens dropdown
        if (e.key === 'Enter' && e.target.classList.contains('nav-link')) {
            const parentItem = e.target.closest('.nav-hover-content');
            if (parentItem) {
                const targetId = parentItem.getAttribute('data-hover-target');
                const targetPanel = document.getElementById(targetId);
                if (targetPanel) {
                    targetPanel.classList.toggle('show');
                }
            }
        }
    });

    // Add loading states for navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            // Only add loading state for actual navigation (not dropdown triggers)
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') {
                const icon = this.querySelector('i');
                if (!icon) {
                    this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>' + this.textContent;
                }
            }
        });
    });
});

// Additional utility functions
window.UniversityNavbar = {
    // Method to programmatically show a dropdown
    showDropdown: function(targetId) {
        const panel = document.getElementById(targetId);
        if (panel) {
            document.querySelectorAll('.hover-content-panel').forEach(p => p.classList.remove('show'));
            panel.classList.add('show');
        }
    },
    
    // Method to hide all dropdowns
    hideAllDropdowns: function() {
        document.querySelectorAll('.hover-content-panel').forEach(panel => {
            panel.classList.remove('show');
        });
    },
    
    // Method to update active menu item
    setActiveMenuItem: function(selector) {
        document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        const activeLink = document.querySelector(selector);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
};