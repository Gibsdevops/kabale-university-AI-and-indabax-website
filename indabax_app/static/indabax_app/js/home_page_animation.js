// indabax_app/static/indabax_app/js/home_page_animation.js

document.addEventListener('DOMContentLoaded', function() {
    const hiddenTextSpan = document.getElementById('hiddenHomeMainHeadingText');
    const dynamicHeading = document.getElementById('dynamicHomeMainHeading');

    if (hiddenTextSpan && dynamicHeading) {
        const fullText = hiddenTextSpan.textContent.trim();
        const words = fullText.split(' ');
        
        let animatedHtml = '';
        words.forEach((word, index) => {
            // Updated: Use a consistent naming scheme if you want to apply specific colors
            // In your CSS, you can now define .word-1 { color: ... }, .word-2 { color: ... }, etc.
            animatedHtml += `<span class="animated-word word-${index + 1}" style="opacity: 0; transform: translateY(20px);">${word}</span> `;
        });
        
        dynamicHeading.innerHTML = animatedHtml;

        // Animate words
        const animatedWords = dynamicHeading.querySelectorAll('.animated-word');
        animatedWords.forEach((wordSpan, index) => {
            setTimeout(() => {
                wordSpan.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
                wordSpan.style.opacity = '1';
                wordSpan.style.transform = 'translateY(0)';
            }, index * 100); // Stagger animation
        });
    }
});