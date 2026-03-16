// Theme: default light, persist in localStorage
(function applyTheme() {
  var saved = localStorage.getItem("cafeholic-theme");
  if (saved === "dark") document.body.setAttribute("data-theme", "dark");
  else document.body.removeAttribute("data-theme");
})();

// Hero carousel: dishes to cycle through (fade transition, no horizontal slide)
var heroDishes = [
  { src: "photos/cholebhature.png", name: "Chole Bhature" },
  { src: "photos/Pav%20Bhaji.png", name: "Pav Bhaji" },
  { src: "photos/chilli-potato.png", name: "Chilly Potatoes" },
  { src: "photos/chowmein.png", name: "Chowmein" },
  { src: "photos/iced-coffee-in-plastic-cups-with-straw-transparent-background.png", name: "Cold Coffee" },
  { src: "photos/momos.png", name: "Veg Momos" },
  { src: "photos/cholerice.png", name: "Chhole Chawal" },
  { src: "photos/delicious-rajma-masala-with-rice-hearty-indian-dish_84443.png", name: "Rajma Chawal" },
  { src: "photos/dosa.png", name: "Dosa" },
  { src: "photos/idli.png", name: "Idli" },
  { src: "photos/vegbiryani.png", name: "Veg Biryani" },
  { src: "photos/paneertikka.png", name: "Paneer Tikka" },
  { src: "photos/samosa.png", name: "Samosa" },
  { src: "photos/alooparatha.jpeg.png", name: "Aloo Paratha" },
  { src: "photos/dal-rice.png", name: "Dal Rice" },
  { src: "photos/paneer-butter-masala.png", name: "Paneer Butter Masala" },
  { src: "photos/gulab-jamun.png", name: "Gulab Jamun" },
  { src: "photos/masala-dosa.png", name: "Masala Dosa" },
  { src: "photos/pani-puri.png", name: "Pani Puri" },
  { src: "photos/burger.png", name: "Burger" },
  { src: "photos/masala-chai.png", name: "Masala Chai" }
];

// Carousel image fallback: use inline placeholder so no extra network request (avoids loading hang)
document.addEventListener("DOMContentLoaded", function () {
  var placeholder = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect fill='%23f5f5f5' width='200' height='200'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%23999' font-size='14' font-family='sans-serif'%3ENo image%3C/text%3E%3C/svg%3E";
  document.querySelectorAll(".testimonial-image, .carousel img[src*='photos/'], .hero-carousel img").forEach(function (img) {
    img.addEventListener("error", function () {
      this.onerror = null;
      this.src = placeholder;
    });
    if (img.src && img.complete && img.naturalWidth === 0) img.src = placeholder;
  });

  // Hero fade carousel: build slides and cycle with fade
  var carouselEl = document.getElementById("heroCarousel");
  var innerEl = carouselEl ? carouselEl.querySelector(".hero-carousel-inner") : null;
  if (innerEl && heroDishes.length > 0) {
    heroDishes.forEach(function (dish, index) {
      var slide = document.createElement("div");
      slide.className = "hero-carousel-slide" + (index === 0 ? " active" : "");
      slide.setAttribute("aria-hidden", index !== 0);
      slide.innerHTML =
        "<div class=\"hero-image-wrap\"><img src=\"" + dish.src + "\" alt=\"" + (dish.name || "Dish") + "\"></div>" +
        "<h2 class=\"hero-dish-title\">" + (dish.name || "") + "</h2>";
      innerEl.appendChild(slide);
    });
    var slides = innerEl.querySelectorAll(".hero-carousel-slide");
    var current = 0;
    var interval = 4000;
    function nextSlide() {
      slides[current].classList.remove("active");
      slides[current].setAttribute("aria-hidden", "true");
      current = (current + 1) % slides.length;
      slides[current].classList.add("active");
      slides[current].setAttribute("aria-hidden", "false");
    }
    setInterval(nextSlide, interval);
  }

  // Hero tagline typing effect: 10 second wait before typing starts again
  var typingEl = document.getElementById("typing-text");
  if (typingEl) {
    var fullText = "Save yourself the time — order from the college cafeteria online!";
    var typeSpeed = 70;
    var waitAfterTyping = 10000; // 10 seconds
    var i = 0;
    function type() {
      if (i < fullText.length) {
        typingEl.textContent += fullText[i];
        i++;
        setTimeout(type, typeSpeed);
      } else {
        setTimeout(function () {
          typingEl.textContent = "";
          i = 0;
          setTimeout(type, typeSpeed);
        }, waitAfterTyping);
      }
    }
    type(); // start typing immediately
  }
});

var themeToggle = document.getElementById("themeToggle");
if (themeToggle) {
  themeToggle.addEventListener("click", function () {
    var isDark = document.body.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.body.removeAttribute("data-theme");
      localStorage.setItem("cafeholic-theme", "light");
    } else {
      document.body.setAttribute("data-theme", "dark");
      localStorage.setItem("cafeholic-theme", "dark");
    }
  });
}

// Sticky Navigation Menu JS Code
var nav = document.querySelector("nav");
var scrollBtn = document.querySelector(".scroll-button a");
if (nav) {
  window.onscroll = function () {
    if (document.documentElement.scrollTop > 20) {
      nav.classList.add("sticky");
      if (scrollBtn) scrollBtn.style.display = "block";
    } else {
      nav.classList.remove("sticky");
      if (scrollBtn) scrollBtn.style.display = "none";
    }
  };
}

// Side Navigation Menu JS Code
var body = document.querySelector("body");
var navBar = document.querySelector(".navibar");
var menuBtn = document.querySelector(".menu-btn");
var cancelBtn = document.querySelector(".cancel-btn");
if (menuBtn && cancelBtn && navBar) {
  menuBtn.onclick = function () {
    navBar.classList.add("active");
    menuBtn.style.opacity = "0";
    menuBtn.style.pointerEvents = "none";
    if (body) body.style.overflow = "hidden";
    if (scrollBtn) scrollBtn.style.pointerEvents = "none";
  };
  cancelBtn.onclick = function () {
    navBar.classList.remove("active");
    menuBtn.style.opacity = "1";
    menuBtn.style.pointerEvents = "auto";
    if (body) body.style.overflow = "auto";
    if (scrollBtn) scrollBtn.style.pointerEvents = "auto";
  };
}

// Side Navigation Bar Close When Clicking Nav Links
var navLinks = document.querySelectorAll(".menu li a");
for (var i = 0; i < navLinks.length; i++) {
  navLinks[i].addEventListener("click", function () {
    if (navBar) navBar.classList.remove("active");
    if (menuBtn) {
      menuBtn.style.opacity = "1";
      menuBtn.style.pointerEvents = "auto";
    }
  });
}
