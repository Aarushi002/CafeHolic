// Theme: default light, persist in localStorage
(function applyTheme() {
  var saved = localStorage.getItem("cafeholic-theme");
  if (saved === "dark") document.body.setAttribute("data-theme", "dark");
  else document.body.removeAttribute("data-theme");
})();

// Carousel image fallback: show placeholder when photo is missing
document.addEventListener("DOMContentLoaded", function () {
  var placeholder = "photos/placeholder.svg";
  document.querySelectorAll(".testimonial-image, .carousel img[src*='photos/']").forEach(function (img) {
    img.addEventListener("error", function () {
      this.onerror = null;
      this.src = placeholder;
    });
    if (img.src && img.complete && img.naturalWidth === 0) img.src = placeholder;
  });
});

document.getElementById("themeToggle").addEventListener("click", function () {
  var isDark = document.body.getAttribute("data-theme") === "dark";
  if (isDark) {
    document.body.removeAttribute("data-theme");
    localStorage.setItem("cafeholic-theme", "light");
  } else {
    document.body.setAttribute("data-theme", "dark");
    localStorage.setItem("cafeholic-theme", "dark");
  }
});

// Sticky Navigation Menu JS Code
let nav = document.querySelector("nav");
let scrollBtn = document.querySelector(".scroll-button a");
let val;
window.onscroll = function() {
  if(document.documentElement.scrollTop > 20){
    nav.classList.add("sticky");
    if (scrollBtn) scrollBtn.style.display = "block";
  }else{
    nav.classList.remove("sticky");
    if (scrollBtn) scrollBtn.style.display = "none";
  }
}

// Side NavIgation Menu JS Code
let body = document.querySelector("body");
let navBar = document.querySelector(".navibar");
let menuBtn = document.querySelector(".menu-btn");
let cancelBtn = document.querySelector(".cancel-btn");
menuBtn.onclick = function(){
  navBar.classList.add("active");
  menuBtn.style.opacity = "0";
  menuBtn.style.pointerEvents = "none";
  body.style.overflow = "hidden";
  if (scrollBtn) scrollBtn.style.pointerEvents = "none";
}
cancelBtn.onclick = function(){
  navBar.classList.remove("active");
  menuBtn.style.opacity = "1";
  menuBtn.style.pointerEvents = "auto";
  body.style.overflow = "auto";
  if (scrollBtn) scrollBtn.style.pointerEvents = "auto";
}

// Side Navigation Bar Close While We Click On Navigation Links
let navLinks = document.querySelectorAll(".menu li a");
for (var i = 0; i < navLinks.length; i++) {
  navLinks[i].addEventListener("click" , function() {
    navBar.classList.remove("active");
    menuBtn.style.opacity = "1";
    menuBtn.style.pointerEvents = "auto";
  });
}
