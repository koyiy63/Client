document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navlinks');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const expanded = navLinks.getAttribute('data-open') === 'true';
      navLinks.setAttribute('data-open', String(!expanded));
      navLinks.style.display = expanded ? 'none' : 'flex';
    });
  }
});