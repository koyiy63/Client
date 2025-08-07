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

    // Close menu when clicking a link (mobile)
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      if (window.matchMedia('(max-width: 720px)').matches) {
        navLinks.style.display = 'none';
        navLinks.setAttribute('data-open', 'false');
      }
    }));
  }

  // Smooth scroll for same-page anchors
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  // Copy helpers
  document.querySelectorAll('[data-copy]').forEach(el => {
    el.addEventListener('click', async () => {
      const text = el.getAttribute('data-copy') || '';
      try {
        await navigator.clipboard.writeText(text);
        el.textContent = 'Copied!';
        setTimeout(() => (el.textContent = 'Copy'), 1200);
      } catch { /* ignore */ }
    });
  });

  // PWA registration
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/ielts-teacher-site/sw.js').catch(() => {});
  }
});