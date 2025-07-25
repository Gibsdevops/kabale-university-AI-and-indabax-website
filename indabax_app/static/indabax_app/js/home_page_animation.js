// indabax_app/static/indabax_app/js/home_page_animation.js

document.addEventListener('DOMContentLoaded', function() {
    const hiddenTextSpan = document.getElementById('hiddenHomeMainHeadingText');
    const dynamicHeading = document.getElementById('dynamicHomeMainHeading');

    if (hiddenTextSpan && dynamicHeading) {
        const fullText = hiddenTextSpan.textContent.trim();
        const words = fullText.split(' ');
        
        let animatedHtml = '';
        words.forEach((word, index) => {
            // Alternating colors for words
            const colorClass = index % 2 === 0 ? 'color-orange' : 'color-green'; 
            animatedHtml += `<span class="animated-word ${colorClass}" style="opacity: 0; transform: translateY(20px);">${word}</span> `;
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

