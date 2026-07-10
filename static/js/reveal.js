(function () {
  'use strict';

  // Не запускаємо якщо користувач не хоче анімацій
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var THRESHOLD = 0.15; // скільки елементу має бути видно (15%)

  if (!('IntersectionObserver' in window)) {
    // Fallback для старих браузерів — просто показуємо всі елементи
    document.querySelectorAll('[data-reveal]').forEach(function (el) {
      el.classList.add('is-visible');
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target); // спрацьовує лише один раз
        }
      });
    },
    { threshold: THRESHOLD, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    observer.observe(el);
  });
})();
