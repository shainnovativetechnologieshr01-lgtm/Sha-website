/**
 * ==============================================================================
 * SHA INNOVATIVE TECHNOLOGIES - NAVBAR & NAVIGATION CONTROLLER
 * File: js/navbar.js
 * Description: Handles sticky header, mobile drawer, dropdowns & keyboard a11y.
 * ==============================================================================
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    initHeaderScroll();
    initMobileNav();
    initDropdownAccessibility();
    setActiveNavLink();
  });

  /**
   * 1. Header scroll effect (Subtle shadow on scroll)
   */
  function initHeaderScroll() {
    const header = document.querySelector('.site-header');
    if (!header) return;

    const handleScroll = () => {
      if (window.scrollY > 15) {
        header.classList.add('is-scrolled');
      } else {
        header.classList.remove('is-scrolled');
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  /**
   * 2. Mobile Navigation Toggle & Drawer Controller
   */
  function initMobileNav() {
    const toggleBtn = document.querySelector('.mobile-nav-toggle');
    const drawer = document.querySelector('.mobile-drawer');
    const overlay = document.querySelector('.mobile-overlay');

    if (!toggleBtn || !drawer) return;

    const openMenu = () => {
      toggleBtn.setAttribute('aria-expanded', 'true');
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      if (overlay) overlay.classList.add('is-visible');
      document.body.style.overflow = 'hidden';
    };

    const closeMenu = () => {
      toggleBtn.setAttribute('aria-expanded', 'false');
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      if (overlay) overlay.classList.remove('is-visible');
      document.body.style.overflow = '';
    };

    toggleBtn.addEventListener('click', () => {
      const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
      if (isExpanded) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    if (overlay) {
      overlay.addEventListener('click', closeMenu);
    }

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        closeMenu();
        toggleBtn.focus();
      }
    });

    // Close on mobile link click if navigating to anchor
    const mobileLinks = drawer.querySelectorAll('a');
    mobileLinks.forEach((link) => {
      link.addEventListener('click', () => {
        closeMenu();
      });
    });

    // Auto-close mobile drawer if resized to desktop width (>= 1024px)
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 1024 && drawer.classList.contains('is-open')) {
        closeMenu();
      }
    });
  }

  /**
   * 3. Accessible Dropdown Navigation & Keyboard Controller
   */
  function initDropdownAccessibility() {
    const dropdowns = document.querySelectorAll('.nav-dropdown');
    if (!dropdowns.length) return;

    dropdowns.forEach((dropdown) => {
      const toggle = dropdown.querySelector('.dropdown-toggle');
      const menu = dropdown.querySelector('.dropdown-menu');

      if (!toggle || !menu) return;

      // Click toggle for touch / mouse
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const isOpen = menu.classList.contains('is-open');
        
        // Close other dropdowns first
        closeAllDropdowns();

        if (!isOpen) {
          menu.classList.add('is-open');
          dropdown.classList.add('is-open');
          toggle.setAttribute('aria-expanded', 'true');
        }
      });

      // Keyboard navigation (ArrowDown, Enter, Space)
      toggle.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          menu.classList.add('is-open');
          dropdown.classList.add('is-open');
          toggle.setAttribute('aria-expanded', 'true');
          const firstItem = menu.querySelector('a');
          if (firstItem) firstItem.focus();
        }
      });

      dropdown.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          menu.classList.remove('is-open');
          dropdown.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
          toggle.focus();
        }
      });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-dropdown')) {
        closeAllDropdowns();
      }
    });

    function closeAllDropdowns() {
      dropdowns.forEach((d) => {
        const m = d.querySelector('.dropdown-menu');
        const t = d.querySelector('.dropdown-toggle');
        if (m) m.classList.remove('is-open');
        d.classList.remove('is-open');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  }

  /**
   * 4. Highlight Active Navigation Item
   */
  function setActiveNavLink() {
    const currentPath = window.location.pathname.toLowerCase();
    const navLinks = document.querySelectorAll('.nav-link, .dropdown-item');

    navLinks.forEach((link) => {
      const href = (link.getAttribute('href') || '').toLowerCase();
      if (!href || href === '#') return;

      const isRoot = (currentPath === '/' || currentPath === '') && (href === 'index.html' || href === '/');
      const isMatch = currentPath.endsWith(href);

      if (isRoot || isMatch) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });
  }
})();
