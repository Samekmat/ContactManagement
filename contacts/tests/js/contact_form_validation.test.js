/**
 * Tests for contact_form_validation.js
 */

// Import the file to test
// Note: The actual import happens through Jest's moduleDirectories configuration
// which maps to the static/contacts/js directory

describe('Contact Form Validation', () => {
  // Setup DOM elements before each test
  beforeEach(() => {
    // Create a mock DOM structure
    document.body.innerHTML = `
      <form id="contact-form">
        <div>
          <input name="phone_number" value="" />
        </div>
        <div>
          <input name="email" value="" />
        </div>
        <div>
          <input name="first_name" value="" />
        </div>
        <div>
          <input name="last_name" value="" />
        </div>
        <div>
          <input name="city" value="" />
        </div>
        <div>
          <select name="status">
            <option value="">Select status</option>
            <option value="1">Active</option>
          </select>
        </div>
      </form>
    `;

    // Load the script
    require('../../../contacts/static/contacts/js/contact_form_validation.js');

    // Trigger DOMContentLoaded event to initialize the script
    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  // Clean up after each test
  afterEach(() => {
    document.body.innerHTML = '';
    // Clean up any event listeners
    jest.restoreAllMocks();
  });

  test('should prevent form submission when phone number is invalid', () => {
    // Arrange
    const form = document.getElementById('contact-form');
    const phoneInput = document.querySelector('input[name="phone_number"]');
    const preventDefault = jest.fn();

    // Set invalid phone number (not 9 digits)
    phoneInput.value = '12345';

    // Act
    form.dispatchEvent(new Event('submit', { preventDefault }));

    // Assert
    expect(phoneInput.classList.contains('border-red-500')).toBe(true);
    const errorMessage = phoneInput.parentNode.querySelector('p');
    expect(errorMessage).not.toBeNull();
    expect(errorMessage.textContent).toContain('Phone number must consist of exactly 9 digits');
  });

  test('should prevent form submission when email is invalid', () => {
    // Arrange
    const form = document.getElementById('contact-form');
    const emailInput = document.querySelector('input[name="email"]');
    const preventDefault = jest.fn();

    // Set invalid email
    emailInput.value = 'invalid-email';

    // Act
    form.dispatchEvent(new Event('submit', { preventDefault }));

    // Assert
    expect(emailInput.classList.contains('border-red-500')).toBe(true);
    const errorMessage = emailInput.parentNode.querySelector('p');
    expect(errorMessage).not.toBeNull();
    expect(errorMessage.textContent).toContain('Please provide a valid email address');
  });

  test('should prevent form submission when required fields are empty', () => {
    // Arrange
    const form = document.getElementById('contact-form');
    const firstNameInput = document.querySelector('input[name="first_name"]');
    const lastNameInput = document.querySelector('input[name="last_name"]');
    const cityInput = document.querySelector('input[name="city"]');
    const preventDefault = jest.fn();

    // Leave required fields empty
    firstNameInput.value = '';
    lastNameInput.value = '';
    cityInput.value = '';

    // Act
    form.dispatchEvent(new Event('submit', { preventDefault }));

    // Assert
    expect(firstNameInput.classList.contains('border-red-500')).toBe(true);
    expect(lastNameInput.classList.contains('border-red-500')).toBe(true);
    expect(cityInput.classList.contains('border-red-500')).toBe(true);

    const firstNameError = firstNameInput.parentNode.querySelector('p');
    const lastNameError = lastNameInput.parentNode.querySelector('p');
    const cityError = cityInput.parentNode.querySelector('p');

    expect(firstNameError).not.toBeNull();
    expect(lastNameError).not.toBeNull();
    expect(cityError).not.toBeNull();

    expect(firstNameError.textContent).toContain('First name is required');
    expect(lastNameError.textContent).toContain('Last name is required');
    expect(cityError.textContent).toContain('City is required');
  });

  test('should allow form submission when all fields are valid', () => {
    // Arrange
    const form = document.getElementById('contact-form');
    const phoneInput = document.querySelector('input[name="phone_number"]');
    const emailInput = document.querySelector('input[name="email"]');
    const firstNameInput = document.querySelector('input[name="first_name"]');
    const lastNameInput = document.querySelector('input[name="last_name"]');
    const cityInput = document.querySelector('input[name="city"]');
    const statusSelect = document.querySelector('select[name="status"]');

    // Mock preventDefault
    const mockEvent = { preventDefault: jest.fn() };

    // Set valid values
    phoneInput.value = '123456789';
    emailInput.value = 'test@example.com';
    firstNameInput.value = 'John';
    lastNameInput.value = 'Doe';
    cityInput.value = 'New York';
    statusSelect.value = '1';

    // Act
    form.dispatchEvent(Object.assign(new Event('submit'), mockEvent));

    // Assert
    // No error classes should be added
    expect(phoneInput.classList.contains('border-red-500')).toBe(false);
    expect(emailInput.classList.contains('border-red-500')).toBe(false);
    expect(firstNameInput.classList.contains('border-red-500')).toBe(false);
    expect(lastNameInput.classList.contains('border-red-500')).toBe(false);
    expect(cityInput.classList.contains('border-red-500')).toBe(false);
    expect(statusSelect.classList.contains('border-red-500')).toBe(false);

    // No error messages should be present
    expect(phoneInput.parentNode.querySelector('p')).toBeNull();
    expect(emailInput.parentNode.querySelector('p')).toBeNull();
    expect(firstNameInput.parentNode.querySelector('p')).toBeNull();
    expect(lastNameInput.parentNode.querySelector('p')).toBeNull();
    expect(cityInput.parentNode.querySelector('p')).toBeNull();
    expect(statusSelect.parentNode.querySelector('p')).toBeNull();
  });
});
