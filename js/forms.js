/**
 * ==============================================================================
 * SHA INNOVATIVE TECHNOLOGIES - FORMS & GOOGLE SHEETS INTEGRATION
 * File: js/forms.js
 * Description: Client-side validation, error feedback, and verified
 * Google Sheets dispatch via Google Apps Script Web App.
 * ==============================================================================
 */

(function () {
  'use strict';

  // Verified Google Apps Script Web App Endpoint
  const FORM_CONFIG = {
    endpointUrl: 'https://script.google.com/macros/s/AKfycbxjQnFW5kRkosKcmHiybNkFmllvlM9s1a-17sBmcut6AF19c1wBWP4UZ06BmFMDmQ-xMA/exec',
    isConfigured: true
  };

  document.addEventListener('DOMContentLoaded', () => {
    initFormValidation();
  });

  /**
   * Initializes client-side validation and submission listeners on forms marked with [data-validate-form]
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

      // Clear field error state dynamically on input
      const inputs = form.querySelectorAll('input, select, textarea');
      inputs.forEach((input) => {
        input.addEventListener('input', () => {
          clearFieldError(input);
        });
        input.addEventListener('change', () => {
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
      const val = (input.value || '').trim();

      if (!val) {
        setFieldError(input, 'This field is required');
        isValid = false;
        return;
      }

      // Email validation
      if (input.type === 'email' || input.name === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(val)) {
          setFieldError(input, 'Please enter a valid email address');
          isValid = false;
          return;
        }
      }

      // Phone validation (accepts standard 10-digit formats & international prefixes)
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
   * Maps form fields to the appropriate Google Apps Script enquiry payload
   */
  function buildPayload(form) {
    const nameEl = form.querySelector('[name="name"]');
    const emailEl = form.querySelector('[name="email"]');
    const phoneEl = form.querySelector('[name="phone"]');
    const orgEl = form.querySelector('[name="organization"]');
    const reqEl = form.querySelector('[name="requirement_type"], [name="requirement"]');
    const msgEl = form.querySelector('[name="message"]');

    const name = nameEl ? nameEl.value.trim() : '';
    const email = emailEl ? emailEl.value.trim() : '';
    const phone = phoneEl ? phoneEl.value.trim() : '';
    const organization = orgEl ? orgEl.value.trim() : '';
    const requirement = reqEl ? reqEl.value.trim() : '';
    const message = msgEl ? msgEl.value.trim() : '';

    // 1. Training Enquiry
    if (requirement === 'Training') {
      return {
        type: 'training',
        name: name,
        email: email,
        phone: phone,
        course: organization ? `Training Program (Org: ${organization})` : 'Technology Training Program',
        learning_mode: 'Standard / Classroom',
        message: message
      };
    }

    // 2. Internship Enquiry
    if (requirement === 'Internship') {
      return {
        type: 'internship',
        name: name,
        email: email,
        phone: phone,
        college: organization || 'Not Specified',
        department: '',
        domain: 'Practical Project Internship',
        duration: 'Standard',
        message: message
      };
    }

    // 3. Project / Solution Enquiry
    const projectTypes = [
      'Project Requirement',
      'Technology Solution',
      'Project Guidance',
      'Web Development',
      'Software Solutions',
      'IT Solutions',
      'Digital Marketing',
      'Business Requirement'
    ];

    if (projectTypes.includes(requirement)) {
      return {
        type: 'project',
        name: name,
        email: email,
        phone: phone,
        project_title: organization ? `${requirement} (${organization})` : requirement,
        technology: '',
        project_type: requirement,
        budget: '',
        deadline: '',
        requirements: message
      };
    }

    // 4. General / Institutional / Contact Enquiry (Default)
    return {
      type: 'contact',
      name: name,
      email: email,
      phone: phone,
      subject: organization ? `${requirement || 'General Enquiry'} - ${organization}` : (requirement || 'General Enquiry'),
      message: message
    };
  }

  /**
   * Safe HTML Escaping for User-Provided Strings
   */
  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, (tag) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag));
  }

  /**
   * Reusable Form Submission Pipeline with Google Apps Script
   */
  async function handleFormSubmit(form) {
    const submitBtn = form.querySelector('[type="submit"]');
    const feedbackEl = form.querySelector('.form-feedback');
    const originalBtnText = submitBtn ? (submitBtn.getAttribute('data-original-text') || submitBtn.textContent) : 'Send an Enquiry';

    if (!FORM_CONFIG.isConfigured || !FORM_CONFIG.endpointUrl) {
      if (feedbackEl) {
        feedbackEl.innerHTML = `
          <div class="alert alert-info">
            <strong>Notice:</strong> Endpoint URL is currently not configured.
          </div>
        `;
      }
      return;
    }

    // Set loading state & disable button to prevent duplicate submissions
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.setAttribute('data-original-text', originalBtnText);
      submitBtn.innerHTML = '<span class="spinner" aria-hidden="true"></span> Submitting...';
    }

    if (feedbackEl) {
      feedbackEl.innerHTML = `
        <div class="alert alert-info">
          <span>Sending your enquiry, please wait...</span>
        </div>
      `;
    }

    const payload = buildPayload(form);

    try {
      const response = await fetch(FORM_CONFIG.endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain;charset=utf-8'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP network error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data && data.success) {
        const refId = data.enquiry_id ? ` (Ref: ${escapeHTML(data.enquiry_id)})` : '';
        if (feedbackEl) {
          feedbackEl.innerHTML = `
            <div class="alert alert-success">
              <strong>Thank you, ${escapeHTML(payload.name)}!</strong> Your enquiry has been received successfully${refId}. Our team will contact you shortly.
            </div>
          `;
        }
        form.reset();

        // Clear any residual validation classes on form inputs
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach((input) => clearFieldError(input));
      } else {
        throw new Error(data && data.message ? data.message : 'Server returned unsuccessful response.');
      }
    } catch (err) {
      if (feedbackEl) {
        feedbackEl.innerHTML = `
          <div class="alert alert-danger">
            There was an issue submitting your enquiry. Please call us directly at <a href="tel:+919344440310" style="color: inherit; font-weight: bold; text-decoration: underline;">+91 93444 40310</a> or email <a href="mailto:shainnovativetechnologieshr01@gmail.com" style="color: inherit; font-weight: bold; text-decoration: underline;">shainnovativetechnologieshr01@gmail.com</a>.
          </div>
        `;
      }
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
      }
    }
  }

  // Export to window for modular access
  window.SHAFormHandler = {
    validateForm,
    handleFormSubmit,
    buildPayload,
    config: FORM_CONFIG
  };
})();
