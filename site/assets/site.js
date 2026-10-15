/* Amélioration progressive : le contenu reste lisible sans JavaScript. */
(() => {
  'use strict';

  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  const navigationLinks = Array.from(navigation.querySelectorAll('a[href^="#"]'));
  document.body.classList.add('js-ready');

  function closeMenu() {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
  }

  menuButton.addEventListener('click', () => {
    const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
    navigation.classList.toggle('is-open', !isOpen);
    menuButton.setAttribute('aria-expanded', String(!isOpen));
  });

  navigationLinks.forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && navigation.classList.contains('is-open')) {
      closeMenu();
      menuButton.focus();
    }
  });

  const conceptButtons = Array.from(document.querySelectorAll('[data-concept]'));
  const conceptPanels = Array.from(document.querySelectorAll('.concept-panel'));

  function activateConcept(id) {
    conceptButtons.forEach((button) => {
      const active = button.dataset.concept === id;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    conceptPanels.forEach((panel) => {
      panel.hidden = panel.id !== id;
    });
  }

  conceptButtons.forEach((button, index) => {
    button.addEventListener('click', () => activateConcept(button.dataset.concept));
    button.addEventListener('keydown', (event) => {
      let nextIndex = index;
      if (event.key === 'ArrowDown' || event.key === 'ArrowRight') {
        nextIndex = (index + 1) % conceptButtons.length;
      } else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') {
        nextIndex = (index - 1 + conceptButtons.length) % conceptButtons.length;
      } else if (event.key === 'Home') {
        nextIndex = 0;
      } else if (event.key === 'End') {
        nextIndex = conceptButtons.length - 1;
      } else {
        return;
      }
      event.preventDefault();
      conceptButtons[nextIndex].focus();
      activateConcept(conceptButtons[nextIndex].dataset.concept);
    });
  });
  activateConcept('incorporation');

  function updateCurrentSection() {
    const anchor = Math.min(window.innerHeight * 0.3, 230);
    let current = '';
    navigationLinks.forEach((link) => {
      const section = document.querySelector(link.getAttribute('href'));
      if (section && section.getBoundingClientRect().top <= anchor) {
        current = link.getAttribute('href');
      }
    });
    navigationLinks.forEach((link) => {
      if (link.getAttribute('href') === current) {
        link.setAttribute('aria-current', 'location');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  }

  let scheduled = false;
  window.addEventListener('scroll', () => {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(() => {
        updateCurrentSection();
        scheduled = false;
      });
    }
  }, { passive: true });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 640) closeMenu();
    updateCurrentSection();
  });
  updateCurrentSection();
})();
