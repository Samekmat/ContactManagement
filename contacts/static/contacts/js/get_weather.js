document.addEventListener("DOMContentLoaded", async () => {
  const weatherCells = document.querySelectorAll(".weather-data");

  for (const cell of weatherCells) {
    const city = cell.dataset.city;

    try {
      // 1. Fetch geolocation(latitude, longitude) data from OpenStreetMap Nominatim API
      const geoRes = await fetch(`https://nominatim.openstreetmap.org/search?q=${city}&format=json&limit=1`);
      const geoData = await geoRes.json();

      if (!geoData.length) {
        cell.innerHTML = `<span class="text-red-500">City not found</span>`;
        continue;
      }

      const { lat, lon } = geoData[0];

      // 2. Fetch weather data from Open Meteo API
      const weatherRes = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=relative_humidity_2m&timezone=auto`
      );
      const weatherData = await weatherRes.json();

      const temperature = weatherData.current_weather.temperature;
      const windspeed = weatherData.current_weather.windspeed;

      // Humidity for this hour, rounded down to the full hour
      const currentTime = weatherData.current_weather.time;
      const hourOnlyTime = currentTime.slice(0, 13) + ':00';

      const timeIndex = weatherData.hourly.time.findIndex(t => t === hourOnlyTime);
      const humidity = timeIndex !== -1 ? weatherData.hourly.relative_humidity_2m[timeIndex] : "–";

      cell.innerHTML = `
        🌡️ ${temperature}°C<br>
        💧 ${humidity}% RH(Relative Humidity)<br>
        💨 ${windspeed} km/h
      `;
    } catch (err) {
      console.error("Weather fetch failed:", err);
      cell.innerHTML = `<span class="text-red-500">Error</span>`;
    }
  }
});
