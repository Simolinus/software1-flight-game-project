let map = L.map("map", {
  maxZoom: 13,
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
const playerMarker = L.featureGroup().addTo(map);

async function currentLocation() {
  let response = await fetch("http://127.0.0.1:3000/playerlocation");
  let airport = await response.json();

  playerMarker.clearLayers();

  let response3 = await fetch("http://127.0.0.1:3000/currentAirport");
  let currentAirportName = await response3.json();

  console.log(currentAirportName);

  let marker = L.marker([airport.latitude_deg, airport.longitude_deg])
    .bindPopup(
      `Current Location 📍<br>ICAO: ${currentAirportName[0]}<br>Country: ${currentAirportName[1]}<br>Airport: ${currentAirportName[2]}`,
    )
    .openPopup();
  playerMarker.addLayer(marker);
}

async function airport_markers() {
  let response = await fetch("http://127.0.0.1:3000/airportLocations");
  let airports_locations = await response.json();
  console.log(airports_locations);

  for (let i = 0; i < airports_locations.length; i++) {
    let marker = L.marker([
      airports_locations[i][3],
      airports_locations[i][4],
    ]).bindPopup(
      `ICAO: ${airports_locations[i][2]}<br>Country: ${airports_locations[i][0]}<br>Airport: ${airports_locations[i][1]}`,
    );
    airportMarkers.addLayer(marker);
  }
}

async function main() {
  airport_markers();
  currentView();
}

main();
currentLocation();
