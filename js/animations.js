/**
 * ==============================================================================
 * SHA INNOVATIVE TECHNOLOGIES - APP-STYLE BRAND INTRO & SPLASH CONTROLLER
 * File: js/animations.js
 * Description: Premium app splash screen sequence (4.5s - 4.8s deliberate pacing).
 * Features: Large center logo reveal, subtle upward lift, progressive word-by-word
 * text reveal, brand lockup hold, smooth logo travel, and staged website emergence.
 * ==============================================================================
 */

(function () {
  'use strict';

  let hasCompletedIntro = false;
  let failsafeTimer = null;
  let previousBodyOverflow = '';

  document.addEventListener('DOMContentLoaded', () => {
    initIntroAnimation();
  });

  /**
   * 1. App-Style Splash Screen & Intro Animation Controller
   */
  async function initIntroAnimation() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isAlreadyPlayed = sessionStorage.getItem('shaIntroPlayed') === 'true';

    const overlay = document.getElementById('intro-overlay');
    const logoContainer = overlay?.querySelector('.intro-logo-container');
    const introLogo = document.getElementById('intro-logo');
    const companyName = document.getElementById('intro-company-name');
    const navLogo = document.querySelector('.site-header .nav-brand-img');

    // Fast-path: Skip intro if already played in this session or user prefers reduced motion
    if (isAlreadyPlayed || prefersReducedMotion || !overlay || !introLogo || !companyName || !navLogo) {
      if (overlay) overlay.style.display = 'none';
      if (navLogo) navLogo.style.opacity = '1';
      document.body.classList.remove(
        'intro-active',
        'intro-navbar-revealing',
        'intro-logo-docked',
        'intro-hero-revealing',
        'intro-cards-revealing'
      );
      initScrollReveals();
      return;
    }

    // Save previous overflow & lock body scrolling
    previousBodyOverflow = document.body.style.overflow || '';
    document.body.style.overflow = 'hidden';
    document.body.classList.add('intro-active');

    // Failsafe timeout: guarantee full recovery within 6 seconds under any unexpected circumstance
    failsafeTimer = setTimeout(() => {
      completeIntroSafely();
    }, 6000);

    // Fallback: If image fails to load
    introLogo.addEventListener('error', () => {
      completeIntroSafely();
    }, { once: true });

    // Window resize during intro safety
    const handleResize = () => {
      if (!hasCompletedIntro) {
        completeIntroSafely();
      }
    };
    window.addEventListener('resize', handleResize, { once: true });

    try {
      // -----------------------------------------------------------------------
      // PHASE 1 — LARGE LOGO REVEAL (0.00s - 1.20s)
      // -----------------------------------------------------------------------
      await wait(100);
      introLogo.classList.add('is-emerged');

      // Logo remains stable and commanding in center
      await wait(1100);

      // -----------------------------------------------------------------------
      // PHASE 2 — LOGO SUBTLE UPWARD SETTLE (1.20s - 1.45s)
      // -----------------------------------------------------------------------
      if (logoContainer) {
        logoContainer.classList.add('is-lifted');
      }
      await wait(250);

      // -----------------------------------------------------------------------
      // PHASE 3 — COMPANY NAME PROGRESSIVE REVEAL (1.45s - 2.15s)
      // -----------------------------------------------------------------------
      companyName.classList.add('is-revealing');
      await wait(700);

      // -----------------------------------------------------------------------
      // PHASE 4 — BRAND LOCKUP HOLD (2.15s - 2.85s)
      // -----------------------------------------------------------------------
      // Full lockup (Logo + SHA Innovative Technologies) holds cleanly
      await wait(700);

      // -----------------------------------------------------------------------
      // PHASE 5 — LOGO TO NAVBAR TRAVEL (2.85s - 3.85s)
      // -----------------------------------------------------------------------
      // Center company name gently dissolves up and fades out
      companyName.classList.remove('is-revealing');
      companyName.classList.add('is-fading');

      // Ensure navbar is laid out so target coordinates are accurate
      const startRect = introLogo.getBoundingClientRect();
      const targetRect = navLogo.getBoundingClientRect();

      // Guard check for valid coordinates
      if (startRect.width === 0 || targetRect.width === 0) {
        completeIntroSafely();
        return;
      }

      const startCenterX = startRect.left + startRect.width / 2;
      const startCenterY = startRect.top + startRect.height / 2;
      const targetCenterX = targetRect.left + targetRect.width / 2;
      const targetCenterY = targetRect.top + targetRect.height / 2;

      const deltaX = targetCenterX - startCenterX;
      const deltaY = targetCenterY - startCenterY;
      const scale = targetRect.height / startRect.height;

      // Animate logo with GPU translate3d and uniform scale directly to navbar logo
      introLogo.style.transformOrigin = '50% 50%';
      introLogo.style.transition = 'transform 1.00s cubic-bezier(0.25, 1, 0.5, 1)';
      introLogo.style.transform = `translate3d(${deltaX}px, ${deltaY}px, 0) scale(${scale})`;

      // At 750ms into travel: Reveal navbar structure (navbar logo stays strictly hidden)
      await wait(750);
      overlay.style.backgroundColor = 'transparent';
      document.body.classList.add('intro-navbar-revealing');

      // -----------------------------------------------------------------------
      // PHASE 6 — EXACT SEAMLESS DOCKING HANDOFF (3.85s)
      // -----------------------------------------------------------------------
      // Complete remaining 250ms of travel to reach exact destination
      await wait(250);

      // Instantaneous seamless handoff: activate real navbar logo, hide intro logo
      document.body.classList.add('intro-logo-docked');
      overlay.classList.add('is-docked');
      navLogo.style.opacity = '1';
      introLogo.style.opacity = '0';

      // Stabilization pause
      await wait(100);
      overlay.style.display = 'none';

      // -----------------------------------------------------------------------
      // PHASE 7 — HERO REVEAL (3.95s - 4.55s)
      // -----------------------------------------------------------------------
      await wait(100);
      document.body.classList.add('intro-hero-revealing');

      // Feature cards and lower page sections emerge
      await wait(600);
      document.body.classList.add('intro-cards-revealing');

      // -----------------------------------------------------------------------
      // PHASE 8 — FINAL COMPLETION & CLEANUP (4.75s)
      // -----------------------------------------------------------------------
      await wait(500);
      completeIntroSafely();


    } catch (err) {
      console.warn('Intro animation encountered an issue, executing failsafe recovery:', err);
      completeIntroSafely();
    }
  }

  /**
   * Safe completion cleanup — idempotent and reliable
   */
  function completeIntroSafely() {
    if (hasCompletedIntro) return;
    hasCompletedIntro = true;

    if (failsafeTimer) {
      clearTimeout(failsafeTimer);
      failsafeTimer = null;
    }

    const overlay = document.getElementById('intro-overlay');
    const navLogo = document.querySelector('.site-header .nav-brand-img');

    if (overlay) {
      overlay.style.display = 'none';
      overlay.style.pointerEvents = 'none';
    }

    if (navLogo) {
      navLogo.style.opacity = '1';
    }

    // Clean up temporary intro staging classes
    document.body.classList.remove(
      'intro-active',
      'intro-navbar-revealing',
      'intro-logo-docked',
      'intro-hero-revealing',
      'intro-cards-revealing'
    );

    // Restore body overflow
    document.body.style.overflow = previousBodyOverflow;

    // Record session completion
    try {
      sessionStorage.setItem('shaIntroPlayed', 'true');
    } catch (e) {
      // Ignore private mode storage restrictions
    }

    // Enable normal scroll reveal observer
    initScrollReveals();
  }

  /**
   * 2. Accessible Scroll Reveals Controller
   */
  function initScrollReveals() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const revealElements = document.querySelectorAll('.reveal:not(.is-visible)');
    if (!revealElements.length || !('IntersectionObserver' in window)) return;

    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -40px 0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, observerOptions);

    revealElements.forEach((el) => observer.observe(el));
  }

  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
})();



