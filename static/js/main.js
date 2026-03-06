// Smooth Scrolling for Navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Flash message auto-dismiss
window.addEventListener('DOMContentLoaded', (event) => {
    const flashMessages = document.querySelectorAll('.flash');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s ease';
                setTimeout(() => msg.remove(), 500);
            });
        }, 5000); // 5 seconds
    }
});

// Simple mobile navigation toggle (burger menu - simplified for this implementation)
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-links');

if (burger) {
    burger.addEventListener('click', () => {
        nav.classList.toggle('nav-active');
        burger.classList.toggle('toggle');
    });
}

// Typing Animation
window.addEventListener('load', () => {
    const typingElement = document.getElementById('typing-text');
    if (typingElement) {
        const text = typingElement.getAttribute('data-text');
        let index = 0;
        const typingSpeed = 30; // ms per character

        function type() {
            if (index < text.length) {
                typingElement.textContent += text.charAt(index);
                index++;
                setTimeout(type, typingSpeed);
            }
        }

        // Start typing after a short delay
        setTimeout(type, 500);
    }
});
