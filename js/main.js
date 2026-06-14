function initNavScroll() {
  const navbar = document.getElementById("navbar");
  window.addEventListener("scroll", () => {
    navbar.style.borderBottomColor = window.scrollY > 20 ? "#2a2a3a" : "transparent";
  }, { passive: true });
}

document.addEventListener("DOMContentLoaded", initNavScroll);
