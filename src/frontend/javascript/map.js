let map = L.map("map", {
  maxZoom: 11,
  minZoom: 4,
  maxBounds: L.latLngBounds([-85, -180], [85, 180]),
  maxBoundsViscosity: 0.8,
}).setView([60.23, 24.74], 13);
L.tileLayer(
  "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png",
  {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attribution">CARTO</a>',
    noWrap: false,
  },
).addTo(map);

async function currentView() {
  let response = await fetch("http://127.0.0.1:3000/playerlocation");
  let airport = await response.json();
  map.setView([airport.latitude_deg, airport.longitude_deg], 5);
}

currentView();
const airportMarkers = L.featureGroup().addTo(map);

async function currentLocation() {
  let response = await fetch("http://127.0.0.1:3000/playerlocation");
  let airport = await response.json();

  airportMarkers.clearLayers();

  let response3 = await fetch("http://127.0.0.1:3000/currentAirport");
  let currentAirportName = await response3.json();

  console.log(currentAirportName);

  const marker = L.marker([airport.latitude_deg, airport.longitude_deg])
    .bindPopup(
      `Current Location 📍<br>ICAO: ${currentAirportName[0]}<br>Country: ${currentAirportName[1]}<br>Airport: ${currentAirportName[2]}`,
    )
    .openPopup();
  airportMarkers.addLayer(marker);
}
currentLocation();
