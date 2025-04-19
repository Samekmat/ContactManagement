# JavaScript Tests

This directory contains tests for the JavaScript files in the `contacts/static/contacts/js` directory.

## Setup

The tests use [Jest](https://jestjs.io/) as the testing framework and [jsdom](https://github.com/jsdom/jsdom) to simulate a DOM environment.

To set up the testing environment:

1. Navigate to this directory:
   ```
   cd contacts/tests/js
   ```

2. Install the dependencies:
   ```
   npm install
   ```

## Running Tests

To run all tests:
```
npm test
```

To run a specific test file:
```
npm test -- contact_form_validation.test.js
```
or
```
npm test -- get_weather.test.js
```

## Test Files

- `contact_form_validation.test.js`: Tests for the form validation logic in `contact_form_validation.js`
- `get_weather.test.js`: Tests for the weather data fetching and display logic in `get_weather.js`

## Test Coverage

The tests cover the following functionality:

### Contact Form Validation
- Validation of phone number format (must be exactly 9 digits)
- Validation of email format
- Checking that required fields are not empty
- Successful form submission with valid data

### Weather Data Fetching
- Fetching and displaying weather data for multiple cities
- Handling the case when a city is not found
- Handling API fetch errors