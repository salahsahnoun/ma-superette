document.addEventListener('DOMContentLoaded', () => {

  // ── Navbar scroll shadow ────────────────────────
  const navbar = document.querySelector('.site-navbar');
  if (navbar) {
    const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ── Mobile menu toggle ──────────────────────────
  const toggle = document.getElementById('mobileToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  if (toggle && mobileMenu) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      mobileMenu.classList.toggle('open');
    });
  }

  // ── Quantity +/- buttons ────────────────────────
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const control = btn.closest('.qty-control');
      const input   = control.querySelector('.qty-num');
      const delta   = parseInt(btn.dataset.delta, 10);
      const min     = parseInt(input.min, 10) || 0;
      const max     = parseInt(input.max, 10) || 99;
      input.value   = Math.min(max, Math.max(min, (parseInt(input.value, 10) || 1) + delta));
    });
  });

  // ── AOS init ────────────────────────────────────
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 680, once: true, offset: 40, easing: 'ease-out-cubic' });
  }

  // ── Flash message auto-close ────────────────────
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => el.style.opacity = '0', 4000);
    setTimeout(() => el.remove(), 4500);
  });

});
