// Navbar cambia de color al hacer scroll
window.addEventListener("scroll", function() {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
});

// Animación de fade-in al hacer scroll
document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll("section");

    const revealSection = () => {
        sections.forEach((section) => {
            const sectionTop = section.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (sectionTop < windowHeight - 100) {
                section.style.opacity = "1";
                section.style.transform = "translateY(0)";
            }
        });
    };

    window.addEventListener("scroll", revealSection);
    revealSection();
});

// Efecto de escribir en el Header
const textElement = document.querySelector(".typing");
const text = "Bienvenido a Ciudades Inteligentes";
let index = 0;

function typeEffect() {
    textElement.innerHTML = text.substring(0, index);
    index++;
    if (index <= text.length) {
        setTimeout(typeEffect, 100);
    }
}

document.addEventListener("DOMContentLoaded", typeEffect);
