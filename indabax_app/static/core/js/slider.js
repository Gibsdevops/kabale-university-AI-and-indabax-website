const slider = document.getElementById('slider');
const nextBtn = document.querySelector('.slide-arrow.next');
const prevBtn = document.querySelector('.slide-arrow.prev');

let scrollAmount = 0;
const slideWidth = 320;

nextBtn.addEventListener('click', () => {
  slider.scrollBy({ left: slideWidth, behavior: 'smooth' });
});

prevBtn.addEventListener('click', () => {
  slider.scrollBy({ left: -slideWidth, behavior: 'smooth' });
});

// Auto-slide every 4 seconds
setInterval(() => {
  slider.scrollBy({ left: slideWidth, behavior: 'smooth' });
}, 4000);
