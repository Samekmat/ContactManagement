document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('contact-form');
  const phoneInput = document.querySelector('input[name="phone_number"]');
  const emailInput = document.querySelector('input[name="email"]');
  const firstNameInput = document.querySelector('input[name="first_name"]');
  const lastNameInput = document.querySelector('input[name="last_name"]');
  const cityInput = document.querySelector('input[name="city"]');
  const statusSelect = document.querySelector('select[name="status"]');

  const phoneError = document.createElement('p');
  phoneError.classList.add('text-sm', 'text-red-600', 'mt-1');
  const emailError = document.createElement('p');
  emailError.classList.add('text-sm', 'text-red-600', 'mt-1');
  const firstNameError = document.createElement('p');
  firstNameError.classList.add('text-sm', 'text-red-600', 'mt-1');
  const lastNameError = document.createElement('p');
  lastNameError.classList.add('text-sm', 'text-red-600', 'mt-1');
  const cityError = document.createElement('p');
  cityError.classList.add('text-sm', 'text-red-600', 'mt-1');
  const statusError = document.createElement('p');
  statusError.classList.add('text-sm', 'text-red-600', 'mt-1');

  form.addEventListener('submit', function (e) {
    let isValid = true;

    if (phoneInput && !/^\d{9}$/.test(phoneInput.value.trim())) {
      phoneInput.classList.add('border-red-500');
      phoneError.textContent = 'Phone number must consist of exactly 9 digits.';
      phoneInput.parentNode.appendChild(phoneError);
      isValid = false;
    } else {
      phoneInput.classList.remove('border-red-500');
      if (phoneError.parentNode) {
        phoneError.parentNode.removeChild(phoneError);
      }
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailInput && !emailPattern.test(emailInput.value.trim())) {
      emailInput.classList.add('border-red-500');
      emailError.textContent = 'Please provide a valid email address.';
      emailInput.parentNode.appendChild(emailError);
      isValid = false;
    } else {
      emailInput.classList.remove('border-red-500');
      if (emailError.parentNode) {
        emailError.parentNode.removeChild(emailError);
      }
    }

    if (firstNameInput && firstNameInput.value.trim() === "") {
      firstNameInput.classList.add('border-red-500');
      firstNameError.textContent = 'First name is required.';
      firstNameInput.parentNode.appendChild(firstNameError);
      isValid = false;
    } else {
      firstNameInput.classList.remove('border-red-500');
      if (firstNameError.parentNode) {
        firstNameError.parentNode.removeChild(firstNameError);
      }
    }

    if (lastNameInput && lastNameInput.value.trim() === "") {
      lastNameInput.classList.add('border-red-500');
      lastNameError.textContent = 'Last name is required.';
      lastNameInput.parentNode.appendChild(lastNameError);
      isValid = false;
    } else {
      lastNameInput.classList.remove('border-red-500');
      if (lastNameError.parentNode) {
        lastNameError.parentNode.removeChild(lastNameError);
      }
    }

    if (cityInput && cityInput.value.trim() === "") {
      cityInput.classList.add('border-red-500');
      cityError.textContent = 'City is required.';
      cityInput.parentNode.appendChild(cityError);
      isValid = false;
    } else {
      cityInput.classList.remove('border-red-500');
      if (cityError.parentNode) {
        cityError.parentNode.removeChild(cityError);
      }
    }

    if (statusSelect && statusSelect.value === "") {
      statusSelect.classList.add('border-red-500');
      statusError.textContent = 'Status is required.';
      statusSelect.parentNode.appendChild(statusError);
      isValid = false;
    } else {
      statusSelect.classList.remove('border-red-500');
      if (statusError.parentNode) {
        statusError.parentNode.removeChild(statusError);
      }
    }

    if (!isValid) {
      e.preventDefault();
    }
  });
});
