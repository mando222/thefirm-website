/**
 * includes.js
 * Fetches shared header.html and footer.html, injects them into every
 * practice-area page, then wires up header scroll state and mobile menu.
 * To update the header or footer sitewide: edit assets/header.html or
 * assets/footer.html — no other file needs to change.
 */
(function () {
  const root = '../assets/';

  function inject(url, targetId, onDone) {
    fetch(url)
      .then(function (r) { return r.text(); })
      .then(function (html) {
        const el = document.getElementById(targetId);
        if (el) {
          el.outerHTML = html;
          if (onDone) onDone();
        }
      })
      .catch(function (err) {
        console.warn('[includes.js] Failed to load ' + url, err);
      });
  }

  function initHeader() {
    // Scroll state
    const header = document.getElementById('header');
    if (header) {
      const onScroll = function () {
        header.classList.toggle('scrolled', window.scrollY > 60);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }

    // Mobile menu
    const menu    = document.getElementById('mobileMenu');
    const burger  = document.getElementById('burger');
    const mmClose = document.getElementById('mmClose');
    if (menu && burger && mmClose) {
      const openMenu  = function () { menu.classList.add('open');    document.body.style.overflow = 'hidden'; };
      const closeMenu = function () { menu.classList.remove('open'); document.body.style.overflow = ''; };
      burger.addEventListener('click', openMenu);
      mmClose.addEventListener('click', closeMenu);
      menu.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', closeMenu);
      });
    }
  }

  inject(root + 'header.html', 'site-header', initHeader);
  inject(root + 'footer.html', 'site-footer');
})();
