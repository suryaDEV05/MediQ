/* =========================================
   MOBILE NAVIGATION
========================================= */

const menuToggle = document.querySelector(".menu-toggle");
const navMenu = document.querySelector(".nav-menu");

if(menuToggle){

    menuToggle.addEventListener("click", () => {

        navMenu.classList.toggle("active");

    });

}


/* =========================================
   CLOSE MENU ON LINK CLICK
========================================= */

const navLinks = document.querySelectorAll(".nav-menu a");

navLinks.forEach(link => {

    link.addEventListener("click", () => {

        navMenu.classList.remove("active");

    });

});


/* =========================================
   PRODUCT SEARCH FILTER
========================================= */

const searchInput = document.querySelector(".product-search");

if(searchInput){

    searchInput.addEventListener("keyup", () => {

        let filterValue = searchInput.value.toLowerCase();

        let productCards = document.querySelectorAll(".product-card");

        productCards.forEach(card => {

            let title = card.querySelector("h3").innerText.toLowerCase();

            let category = card.querySelector(".product-category")
            .innerText.toLowerCase();

            if(
                title.includes(filterValue) ||
                category.includes(filterValue)
            ){

                card.style.display = "block";

            }
            else{

                card.style.display = "none";

            }

        });

    });

}


/* =========================================
   HEADER SCROLL EFFECT
========================================= */

const header = document.querySelector(".header");

window.addEventListener("scroll", () => {

    if(window.scrollY > 80){

        header.style.boxShadow =
        "0 12px 35px rgba(0,0,0,0.08)";

        header.style.background =
        "rgba(255,255,255,0.96)";

    }
    else{

        header.style.boxShadow = "none";

        header.style.background =
        "rgba(255,255,255,0.92)";

    }

});


/* =========================================
   SMOOTH SCROLL
========================================= */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        const target = document.querySelector(
            this.getAttribute("href")
        );

        if(target){

            target.scrollIntoView({
                behavior:"smooth"
            });

        }

    });

});


/* =========================================
   FADE-IN ANIMATION ON SCROLL
========================================= */

const fadeElements = document.querySelectorAll(
    ".product-card, .feature-box, .category-card, .why-card"
);

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

},{
    threshold:0.15
});

fadeElements.forEach(el => {

    el.classList.add("hidden");

    observer.observe(el);

});


/* =========================================
   ADD ANIMATION STYLES VIA JS
========================================= */

const style = document.createElement("style");

style.innerHTML = `

.hidden{

    opacity:0;
    transform:translateY(40px);
    transition:all 0.8s ease;

}

.show{

    opacity:1;
    transform:translateY(0);

}

`;

document.head.appendChild(style);


/* =========================================
   WHATSAPP AUTO PRODUCT MESSAGE
========================================= */

const whatsappButtons = document.querySelectorAll(
    ".whatsapp-product-btn"
);

// Use the site's updated WhatsApp number
const SITE_WHATSAPP_NUMBER = "919848453938";

whatsappButtons.forEach(button => {

    button.addEventListener("click", (e) => {

        const card = button.closest(".product-card");
        if (!card) return;

        const titleEl = card.querySelector("h3") || card.querySelector(".product-content h3");
        const productName = titleEl ? titleEl.innerText.trim() : 'this product';

        const message = `Hello Srinivas.N, I am interested in ${productName}. Please share details and pricing.`;
        const encodedMessage = encodeURIComponent(message);

        // If button is an <a>, update href; otherwise open in new tab
        if (button.tagName.toLowerCase() === 'a'){
            button.href = `https://wa.me/${SITE_WHATSAPP_NUMBER}?text=${encodedMessage}`;
        } else {
            window.open(`https://wa.me/${SITE_WHATSAPP_NUMBER}?text=${encodedMessage}`, '_blank');
        }

    });

});


/* =========================================
   HERO BUTTON RIPPLE EFFECT
========================================= */

const buttons = document.querySelectorAll(
    ".primary-btn, .secondary-btn, .product-btn, .cta-btn"
);

buttons.forEach(button => {

    button.addEventListener("mouseenter", () => {

        button.style.transform = "translateY(-4px)";

    });

    button.addEventListener("mouseleave", () => {

        button.style.transform = "translateY(0px)";

    });

});


/* =========================================
   PRODUCT CARD HOVER GLOW
========================================= */

const productCards = document.querySelectorAll(".product-card");

productCards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.boxShadow =
        "0 25px 60px rgba(10,88,202,0.18)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.boxShadow =
        "0 12px 40px rgba(2,6,23,0.08)";

    });

});


/* =========================================
   ACTIVE NAV LINK ON SCROLL
========================================= */

const sections = document.querySelectorAll("section");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop - 200;

        if(window.scrollY >= sectionTop){

            current = section.getAttribute("id");

        }

    });

    navLinks.forEach(link => {

        link.classList.remove("active");

        if(
            link.getAttribute("href")
            .includes(current)
        ){

            link.classList.add("active");

        }

    });

});


/* =========================================
   LOADING ANIMATION
========================================= */

window.addEventListener("load", () => {

    document.body.style.opacity = "1";

});

document.body.style.opacity = "0";

document.body.style.transition =
"opacity 0.5s ease";


/* =========================================
   FLOATING WHATSAPP TOOLTIP
========================================= */

const floatingWhatsapp =
document.querySelector(".floating-whatsapp");

if(floatingWhatsapp){

    floatingWhatsapp.setAttribute(
        "title",
        "Chat with MEDIQ on WhatsApp"
    );

}


/* =========================================
   CONSOLE BRANDING
========================================= */

console.log(
    "%cMEDIQ Healthcare Equipment Website Loaded",
    "color:#0a58ca;font-size:18px;font-weight:bold;"
);

console.log(
    "%cPremium Industry Grade Medical Equipment Website",
    "color:#e63946;font-size:14px;"
);