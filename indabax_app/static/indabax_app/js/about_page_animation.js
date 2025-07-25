// indabax_app/static/indabax_app/js/about_page_animation.js

document.addEventListener('DOMContentLoaded', function() {
    const hiddenTextSpan = document.getElementById('hiddenMainHeadingText');
    const dynamicHeading = document.getElementById('dynamicMainHeading');

    if (hiddenTextSpan && dynamicHeading) {
        const fullText = hiddenTextSpan.textContent.trim();
        const words = fullText.split(' ');
        
        let animatedHtml = '';
        words.forEach((word, index) => {
            // Apply different colors or a gradient
            const colorClass = index % 2 === 0 ? 'color-orange' : 'color-green'; // Example colors
            animatedHtml += `<span class="animated-word ${colorClass}" style="opacity: 0; transform: translateX(${index % 2 === 0 ? '-50px' : '50px'});">${word}</span> `;
        });
        
        dynamicHeading.innerHTML = animatedHtml;

        // Animate words
        const animatedWords = dynamicHeading.querySelectorAll('.animated-word');
        animatedWords.forEach((wordSpan, index) => {
            setTimeout(() => {
                wordSpan.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                wordSpan.style.opacity = '1';
                wordSpan.style.transform = 'translateX(0)';
            }, index * 150); // Stagger animation
        });
    }
});