// indabax_app/static/indabax_app/js/hero_background_rotator.js
document.addEventListener('DOMContentLoaded', function() {
    const heroBannerContainer = document.querySelector('#homeAnimatedTitleContainer');
    if (!heroBannerContainer) return; // Exit if element not found

    // Get URLs from data attribute
    let backgroundImages = JSON.parse(heroBannerContainer.dataset.backgroundUrls || '[]');
    const defaultBackground = heroBannerContainer.dataset.defaultBackground;

    // Fallback if no images are set in the admin
    if (backgroundImages.length === 0 && defaultBackground) {
        backgroundImages.push(defaultBackground);
    }
    // You can add more static defaults directly here if needed:
    // if (backgroundImages.length === 0) {
    //    backgroundImages.push('/static/indabax_app/images/default_ai_background.jfif');
    //    backgroundImages.push('/static/indabax_app/images/another_default.jfif');
    // }


    let currentImageIndex = 0;

    function changeBackground() {
        heroBannerContainer.style.backgroundImage = `url('${backgroundImages[currentImageIndex]}')`;
        currentImageIndex = (currentImageIndex + 1) % backgroundImages.length;
    }

    // Set initial background
    if (backgroundImages.length > 0) { // Only run if there's at least one image
        changeBackground();
        setInterval(changeBackground, 7000); // Adjust time as needed
    }
});