import { refreshPlayerUI } from "./api.js";
let map = L.map("map", {
  maxZoom: 15,
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

let playerIcon = L.icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

async function currentView() {
  let response = await fetch("http://127.0.0.1:3000/playerlocation");
  let airport = await response.json();
  map.flyTo([airport.latitude_deg, airport.longitude_deg], 15, {
    duration: 2,
  });
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

  let marker = L.marker([airport.latitude_deg, airport.longitude_deg], {
    icon: playerIcon,
  })
    .bindPopup(
      `Current Location 📍<br>ICAO: ${currentAirportName[0]}<br>Country: ${currentAirportName[1]}<br>Airport: ${currentAirportName[2]}`,
    )
    .openPopup();

  playerMarker.addLayer(marker);
}

async function airport_markers() {
  let response = await fetch("http://127.0.0.1:3000/airportLocations");
  let airports_locations = await response.json();

  for (let i = 0; i < airports_locations.length; i++) {
    const airport = airports_locations[i];
    let marker = L.marker([airport[3], airport[4]]).bindPopup(
      `ICAO: ${airport[2]}<br>Country: ${airport[0]}<br>Airport: ${airport[1]}<br>Travel:<br><button id="commercial-${airport[2]}">Commercial Flight(300€)</button><button id="private-${airport[2]}">Private Flight(800€)</button>`,
    );
    marker.on("popupopen", () => {
      document
        .getElementById(`commercial-${airport[2]}`)
        ?.addEventListener("click", () => commercialTravel(airport));

      document
        .getElementById(`private-${airport[2]}`)
        ?.addEventListener("click", () => privateTravel(airport));
    });
    airportMarkers.addLayer(marker);
  }
}

async function commercialTravel(airport) {
  const response = await fetch("http://127.0.0.1:3000/travel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      destination: airport[2],
      type: "commercial",
    }),
  });
  const data = await response.json();
  if (data.status === "success") {
    currentLocation();
    currentView();
    addToHistory(`Traveled to ${airport[1]}, ${airport[0]}`, "travel");
    check_puzzle_piece(airport);
    await refreshPlayerUI();
    const event = new Event("playerUpdated");
    window.dispatchEvent(event);
  }
  if (data.error) {
    addToHistory(data.error, "error");
  }
}
async function privateTravel(airport) {
  const response = await fetch("http://127.0.0.1:3000/travel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      destination: airport[2],
      type: "private",
    }),
  });
  const data = await response.json();
  if (data.status === "success") {
    currentLocation();
    currentView();
    addToHistory(`Traveled to ${airport[1]}, ${airport[0]}`, "travel");
    check_puzzle_piece(airport);
    await refreshPlayerUI();
    const event = new Event("playerUpdated");
    window.dispatchEvent(event);
  }
  if (data.error) {
    addToHistory(data.error, "error");
  }
}

async function check_puzzle_piece(airport) {
  if (airport[5] != null) {
    const response = await fetch("http://127.0.0.1:3000/acquire-puzzle-piece");
    const data = await response.json();
    if (data.piece) {
      addToHistory(data.piece, "puzzle");
    } else {
      addToHistory(data.error, "error");
    }
  }
}
function addToHistory(message, type = "info") {
  const box = document.getElementById("game-history");
  const entry = document.createElement("div");
  entry.className = "log-entry";
  if (type === "travel") {
    entry.style.borderLeftColor = "#4fc3f7";
  } else if (type === "puzzle") {
    entry.style.borderLeftColor = "#fa0000";
  } else if (type === "error") {
    entry.style.borderLeftColor = "#e57373";
  }
  entry.textContent = message;
  box.appendChild(entry);
  box.scrollTop = box.scrollHeight;
}
currentLocation();
airport_markers();
