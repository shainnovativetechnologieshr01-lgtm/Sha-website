/**
 * ==============================================================================
 * SHA INNOVATIVE TECHNOLOGIES - MAIN APPLICATION BOOTSTRAP
 * File: js/main.js
 * Description: Core initialization, year updates, smooth anchors, and FAQ accordion.
 * ==============================================================================
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    initCopyrightYear();
    initSmoothAnchors();
    initFaqAccordion();
  });

  /**
   * 1. Auto-update copyright year in footer
   */
  function initCopyrightYear() {
    const yearEl = document.getElementById('current-year');
    if (yearEl) {
      yearEl.textContent = new Date().getFullYear();
    }
  }

  /**
   * 2. Smooth internal link scrolling with header offset
   */
  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (!targetId || targetId === '#') return;

        const targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          const headerOffset = 85;
          const elementPosition = targetEl.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  /**
   * 3. Accessible FAQ Accordion Controller
   */
  function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    if (!faqItems.length) return;

    faqItems.forEach((item) => {
      const questionBtn = item.querySelector('.faq-question');
      const answerPanel = item.querySelector('.faq-answer');

      if (!questionBtn || !answerPanel) return;

      questionBtn.addEventListener('click', () => {
        const isExpanded = questionBtn.getAttribute('aria-expanded') === 'true';

        // Close all other FAQ items for a clean corporate accordion behavior
        faqItems.forEach((otherItem) => {
          if (otherItem !== item) {
            const otherBtn = otherItem.querySelector('.faq-question');
            const otherAnswer = otherItem.querySelector('.faq-answer');
            if (otherBtn && otherAnswer) {
              otherBtn.setAttribute('aria-expanded', 'false');
              otherItem.classList.remove('is-active');
            }
          }
        });

        // Toggle current item
        if (isExpanded) {
          questionBtn.setAttribute('aria-expanded', 'false');
          item.classList.remove('is-active');
        } else {
          questionBtn.setAttribute('aria-expanded', 'true');
          item.classList.add('is-active');
        }
      });
    });
  }
})();
