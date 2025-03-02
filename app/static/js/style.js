document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu toggle
  const navbarBurger = document.querySelector('.navbar-burger');
  const navbarMenu = document.querySelector('.navbar-menu');
  
  navbarBurger.addEventListener('click', () => {
    navbarBurger.classList.toggle('is-active');
    navbarMenu.classList.toggle('is-active');
  });
  
  // Navbar scroll effect
  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
      navbar.classList.add('navbar-scrolled');
    } else {
      navbar.classList.remove('navbar-scrolled');
    }
  });
  
  // Add hover animation to dropdown items with delay
  const dropdownItems = document.querySelectorAll('.dropdown-item');
  dropdownItems.forEach((item, index) => {
    item.style.transitionDelay = `${index * 0.05}s`;
  });
  
  // Add active state for current page
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-item:not(.has-dropdown)');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath) {
      link.classList.add('is-active');
    }
  });
});