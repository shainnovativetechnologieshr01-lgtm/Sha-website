/**
 * ==============================================================================
 * SHA INNOVATIVE TECHNOLOGIES - FORMS & ENQUIRY ARCHITECTURE
 * File: js/forms.js
 * Description: Client-side validation, error handling & preparation for
 * Google Apps Script / Google Sheets endpoint integration in Step 2.
 * ==============================================================================
 */

(function () {
  'use strict';

  // Config placeholder for future Google Apps Script Web App Endpoint
  const FORM_CONFIG = {
    // In future phases, set to the live Google Apps Script Exec URL:
    // endpointUrl: 'https://script.google.com/macros/s/.../exec',
    endpointUrl: '',
    isConfigured: false
  };

  document.addEventListener('DOMContentLoaded', () => {
    initFormValidation();
  });

  /**
   * Initializes client-side validation on forms marked with [data-validate-form]
   */
  function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate-form]');

    forms.forEach((form) => {
      form.addEventListener('submit', (e) => {
        e.preventDefault();

        if (validateForm(form)) {
          handleFormSubmit(form);
        }
      });

      // Clear error on input change
      const inputs = form.querySelectorAll('input, select, textarea');
      inputs.forEach((input) => {
        input.addEventListener('input', () => {
          clearFieldError(input);
        });
      });
    });
  }

  /**
   * Validates form fields (Email, Phone, Required fields)
   */
  function validateForm(form) {
    let isValid = true;
    const requiredInputs = form.querySelectorAll('[required]');

    requiredInputs.forEach((input) => {
      const val = input.value.trim();
      const group = input.closest('.form-group');

      if (!val) {
        setFieldError(input, 'This field is required');
        isValid = false;
        return;
      }

      // Email validation
      if (input.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(val)) {
          setFieldError(input, 'Please enter a valid email address');
          isValid = false;
          return;
        }
      }

      // Phone validation (accepts standard Indian 10-digit formats / international prefixes)
      if (input.type === 'tel' || input.name === 'phone') {
        const phoneClean = val.replace(/[\s\-\+\(\)]/g, '');
        if (phoneClean.length < 10) {
          setFieldError(input, 'Please enter a valid 10-digit phone number');
          isValid = false;
          return;
        }
      }

      clearFieldError(input);
    });

    return isValid;
  }

  function setFieldError(input, message) {
    const group = input.closest('.form-group') || input.closest('.contact-field-wrap');
    if (!group) return;

    group.classList.add('has-error');
    let errorEl = group.querySelector('.form-error-msg');
    if (!errorEl) {
      errorEl = document.createElement('span');
      errorEl.className = 'form-error-msg';
      group.appendChild(errorEl);
    }
    errorEl.textContent = message;
  }

  function clearFieldError(input) {
    const group = input.closest('.form-group') || input.closest('.contact-field-wrap');
    if (!group) return;
    group.classList.remove('has-error');
    const errorEl = group.querySelector('.form-error-msg');
    if (errorEl) {
      errorEl.remove();
    }
  }

  /**
   * Reusable Form Submission Pipeline
   */
  function handleFormSubmit(form) {
    const submitBtn = form.querySelector('[type="submit"]');
    const feedbackEl = form.querySelector('.form-feedback');

    // If backend isn't configured yet (Step 1 phase)
    if (!FORM_CONFIG.isConfigured || !FORM_CONFIG.endpointUrl) {
      if (feedbackEl) {
        feedbackEl.innerHTML = `
          <div class="alert alert-info">
            <strong>Enquiry Received (Preview Mode):</strong> Form submission pipeline is structured and ready for Google Apps Script integration in Step 2.
          </div>
        `;
      }
      return;
    }

    // When configured in Step 2:
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner"></span> Submitting...';
    }

    const formData = new FormData(form);

    fetch(FORM_CONFIG.endpointUrl, {
      method: 'POST',
      body: formData,
      mode: 'cors'
    })
      .then((res) => res.json())
      .then((data) => {
        if (feedbackEl) {
          feedbackEl.innerHTML = `
            <div class="alert alert-success">
              Thank you! Your enquiry has been received. Our team will contact you shortly.
            </div>
          `;
        }
        form.reset();
      })
      .catch((err) => {
        console.error('Form submission error:', err);
        if (feedbackEl) {
          feedbackEl.innerHTML = `
            <div class="alert alert-danger">
              There was an error sending your enquiry. Please call us directly at +91 93444 40310.
            </div>
          `;
        }
      })
      .finally(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = submitBtn.getAttribute('data-original-text') || 'Submit Enquiry';
        }
      });
  }

  // Export to window for modular use
  window.SHAFormHandler = {
    validateForm,
    handleFormSubmit,
    config: FORM_CONFIG
  };
})();
