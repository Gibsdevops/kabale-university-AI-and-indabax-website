// indabax_app_style.js

// This entire block of code is for a custom slider.
// We are commenting it out to avoid conflicts with Bootstrap's Carousel.

/*
const slider = document.getElementById('slider');
const nextBtn = document.querySelector('.slide-arrow.next');
const prevBtn = document.querySelector('.slide-arrow.prev');

// Line 8 would be one of these:
// nextBtn.addEventListener('click', () => { // <--- LIKELY CAUSE OF THE ERROR IF THIS LINE IS ACTIVE
//     slider.scrollBy({ left: slideWidth, behavior: 'smooth' });
// });

// prevBtn.addEventListener('click', () => {
//     slider.scrollBy({ left: -slideWidth, behavior: 'smooth' });
// });

let scrollAmount = 0; // If this line number isn't 8, adjust comment
const slideWidth = 320; // This should match the width you set for .slide in CSS

nextBtn.addEventListener('click', () => {
    slider.scrollBy({ left: slideWidth, behavior: 'smooth' });
});

prevBtn.addEventListener('click', () => {
    slider.scrollBy({ left: -slideWidth, behavior: 'smooth' });
});

// Auto-slide every 4 seconds
setInterval(() => {
    // This part is a bit tricky with scrollBy and may need adjustment for true looping
    // For now, it will just scroll by one slide width.
    slider.scrollBy({ left: slideWidth, behavior: 'smooth' });
}, 4000);
*/ // <--- ENSURE THIS CLOSING COMMENT IS PRESENT AND CORRECTLY PLACED

// You can add any other custom JavaScript for your app below this commented section if needed.
// For example:
// console.log("indabax_app_style.js is loaded, custom slider code is commented out.");