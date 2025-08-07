document.addEventListener('DOMContentLoaded', () => {
  // Reveal on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('reveal'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.card').forEach(el => observer.observe(el));

  // Mobile nav
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('navlinks');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.getAttribute('data-open') === 'true';
      nav.style.display = open ? 'none' : 'flex';
      nav.setAttribute('data-open', String(!open));
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', ()=>{
      if (window.matchMedia('(max-width: 720px)').matches) {
        nav.style.display = 'none';
        nav.setAttribute('data-open', 'false');
      }
    }));
  }

  // Smooth anchors
  document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id && id !== '#') {
      const t = document.querySelector(id);
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
    }
  }));
});