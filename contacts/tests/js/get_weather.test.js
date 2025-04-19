/**
 * Tests for get_weather.js
 */

describe('Weather Data Fetching', () => {
  // Setup DOM elements before each test
  beforeEach(() => {
    // Create a mock DOM structure with weather-data cells
    document.body.innerHTML = `
      <div class="weather-data" data-city="New York"></div>
      <div class="weather-data" data-city="London"></div>
    `;

    // Mock the global fetch function
    global.fetch = jest.fn();

    // Mock successful geolocation response for New York
    const mockGeoResponseNY = Promise.resolve({
      json: () => Promise.resolve([
        { lat: 40.7128, lon: -74.0060 }
      ])
    });

    // Mock successful weather response for New York
    const mockWeatherResponseNY = Promise.resolve({
      json: () => Promise.resolve({
        current_weather: {
          temperature: 22.5,
          windspeed: 10.2,
          time: '2025-04-19T15:00:00'
        },
        hourly: {
          time: ['2025-04-19T15:00:00'],
          relative_humidity_2m: [65]
        }
      })
    });

    // Mock successful geolocation response for London
    const mockGeoResponseLondon = Promise.resolve({
      json: () => Promise.resolve([
        { lat: 51.5074, lon: -0.1278 }
      ])
    });

    // Mock successful weather response for London
    const mockWeatherResponseLondon = Promise.resolve({
      json: () => Promise.resolve({
        current_weather: {
          temperature: 18.3,
          windspeed: 8.7,
          time: '2025-04-19T15:00:00'
        },
        hourly: {
          time: ['2025-04-19T15:00:00'],
          relative_humidity_2m: [70]
        }
      })
    });

    // Set up fetch mock to return different responses based on URL
    global.fetch.mockImplementation((url) => {
      if (url.includes('nominatim.openstreetmap.org')) {
        if (url.includes('New%20York')) {
          return mockGeoResponseNY;
        } else if (url.includes('London')) {
          return mockGeoResponseLondon;
        }
      } else if (url.includes('api.open-meteo.com')) {
        if (url.includes('latitude=40.7128')) {
          return mockWeatherResponseNY;
        } else if (url.includes('latitude=51.5074')) {
          return mockWeatherResponseLondon;
        }
      }
      return Promise.reject(new Error('Unhandled URL in mock'));
    });
  });

  // Clean up after each test
  afterEach(() => {
    document.body.innerHTML = '';
    jest.restoreAllMocks();
    global.fetch.mockClear();
    delete global.fetch;
  });

  test('should fetch and display weather data for cities', async () => {
    // Clear previous mock implementation
    global.fetch.mockReset();

    // Set up a more specific mock for this test
    global.fetch.mockImplementation((url) => {
      // Handle New York geolocation request
      if (url.includes('nominatim.openstreetmap.org') && url.includes('New York')) {
        return Promise.resolve({
          json: () => Promise.resolve([
            { lat: 40.7128, lon: -74.0060 }
          ])
        });
      }
      // Handle London geolocation request
      else if (url.includes('nominatim.openstreetmap.org') && url.includes('London')) {
        return Promise.resolve({
          json: () => Promise.resolve([
            { lat: 51.5074, lon: -0.1278 }
          ])
        });
      }
      // Handle New York weather request
      else if (url.includes('api.open-meteo.com') && url.includes('latitude=40.7128')) {
        return Promise.resolve({
          json: () => Promise.resolve({
            current_weather: {
              temperature: 22.5,
              windspeed: 10.2,
              time: '2025-04-19T15:00:00'
            },
            hourly: {
              time: ['2025-04-19T15:00'],
              relative_humidity_2m: [65]
            }
          })
        });
      }
      // Handle London weather request
      else if (url.includes('api.open-meteo.com') && url.includes('latitude=51.5074')) {
        return Promise.resolve({
          json: () => Promise.resolve({
            current_weather: {
              temperature: 18.3,
              windspeed: 8.7,
              time: '2025-04-19T15:00:00'
            },
            hourly: {
              time: ['2025-04-19T15:00'],
              relative_humidity_2m: [70]
            }
          })
        });
      }
      return Promise.reject(new Error('Unhandled URL in mock'));
    });

    // Load the script
    require('../../../contacts/static/contacts/js/get_weather.js');

    // Trigger DOMContentLoaded event to initialize the script
    document.dispatchEvent(new Event('DOMContentLoaded'));

    // Wait for all promises to resolve
    await new Promise(process.nextTick);

    // Get the weather cells
    const nyWeatherCell = document.querySelector('.weather-data[data-city="New York"]');
    const londonWeatherCell = document.querySelector('.weather-data[data-city="London"]');

    // Assert that fetch was called
    expect(global.fetch).toHaveBeenCalled();

    // Check that the weather data was displayed correctly based on our mock responses

    // Assert that the weather data was displayed correctly
    expect(nyWeatherCell.innerHTML).toContain('22.5°C');
    expect(nyWeatherCell.innerHTML).toContain('65% RH');
    expect(nyWeatherCell.innerHTML).toContain('10.2 km/h');

    expect(londonWeatherCell.innerHTML).toContain('18.3°C');
    expect(londonWeatherCell.innerHTML).toContain('70% RH');
    expect(londonWeatherCell.innerHTML).toContain('8.7 km/h');
  });

  test('should handle city not found error', async () => {
    // Clear previous mock implementation
    global.fetch.mockReset();

    // Mock fetch to return empty array for geolocation of NonExistentCity
    global.fetch.mockImplementation((url) => {
      if (url.includes('nominatim.openstreetmap.org') && url.includes('NonExistentCity')) {
        return Promise.resolve({
          json: () => Promise.resolve([])
        });
      }
      return Promise.reject(new Error('Unhandled URL in mock'));
    });

    // Update DOM to include a non-existent city
    document.body.innerHTML += `<div class="weather-data" data-city="NonExistentCity"></div>`;

    // Load the script
    require('../../../contacts/static/contacts/js/get_weather.js');

    // Trigger DOMContentLoaded event to initialize the script
    document.dispatchEvent(new Event('DOMContentLoaded'));

    // Wait for all promises to resolve
    await new Promise(process.nextTick);

    // Get the weather cell for the non-existent city
    const nonExistentCityCell = document.querySelector('.weather-data[data-city="NonExistentCity"]');

    // Assert that the error message was displayed
    expect(nonExistentCityCell.innerHTML).toContain('City not found');
  });

  test('should handle API fetch error', async () => {
    // Clear previous mock implementation
    global.fetch.mockReset();

    // Mock fetch to throw an error for ErrorCity
    global.fetch.mockImplementation((url) => {
      if (url.includes('nominatim.openstreetmap.org') && url.includes('ErrorCity')) {
        return Promise.reject(new Error('Network error'));
      }
      return Promise.reject(new Error('Unhandled URL in mock'));
    });

    // Update DOM to include a city that will trigger an error
    document.body.innerHTML += `<div class="weather-data" data-city="ErrorCity"></div>`;

    // Mock console.error to prevent test output pollution
    const originalConsoleError = console.error;
    console.error = jest.fn();

    // Load the script
    require('../../../contacts/static/contacts/js/get_weather.js');

    // Trigger DOMContentLoaded event to initialize the script
    document.dispatchEvent(new Event('DOMContentLoaded'));

    // Wait for all promises to resolve
    await new Promise(process.nextTick);

    // Get the weather cell for the error city
    const errorCityCell = document.querySelector('.weather-data[data-city="ErrorCity"]');

    // Assert that the error message was displayed
    expect(errorCityCell.innerHTML).toContain('Error');

    // Assert that console.error was called
    expect(console.error).toHaveBeenCalled();

    // Restore console.error
    console.error = originalConsoleError;
  });
});
