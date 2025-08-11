// Leaflet-Karte initialisieren
const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap-Mitwirkende',
  maxZoom: 18
}).addTo(map);

// Daten laden
fetch('../leaflet_routes.json')
  .then(response => response.json())
  .then(dataArray => {
    // === Filter Dropdown befüllen ===
    const personSet = new Set();
    dataArray.forEach(entry => personSet.add(entry.person));
    personSet.forEach(name => {
      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      document.getElementById('personFilter').appendChild(option);
    });

    // === Funktion zum Zeichnen basierend auf Filter ===
    function drawMap(filteredData) {
      // Vorherige Marker und Linien entfernen
      map.eachLayer(layer => {
        if (layer instanceof L.CircleMarker || layer instanceof L.Polyline) {
          map.removeLayer(layer);
        }
      });

      const allCoords = [];
      const locationMap = new Map();

      // Orte gruppieren
      filteredData.forEach(entry => {
        entry.route.forEach(point => {
          const id = point.location_id;
          if (!locationMap.has(id)) {
            locationMap.set(id, {
              ...point,
              persons: new Map([[entry.person, entry.person_id || null]])
            });
          } else {
            locationMap.get(id).persons.set(entry.person, entry.person_id || null);
          }
        });
      });

      // Marker zeichnen
      locationMap.forEach(loc => {
        const coord = [loc.lat, loc.lng];
        allCoords.push(coord);
        const count = loc.persons.size;

        const marker = L.circleMarker(coord, {
          radius: 3 + count * 1.5,
          color: '#497f7f',
          fillColor: '#497f7f',
          fillOpacity: 0.8,
          weight: 1
        }).addTo(map);

        let personList = '';
        loc.persons.forEach((id, name) => {
          if (id) {
            personList += `👤 <a href="${id}" target="_blank">${name}</a><br>`;
          } else {
            personList += `👤 ${name}<br>`;
          }
        });

        marker.bindPopup(`
          <b><a href="${loc.location_id}" target="_blank">${loc.location}</a></b><br>
          👥 Personen: ${count}<br>
          ${personList}
        `);
      });

      // Linien zeichnen
      filteredData.forEach(entry => {
        const coords = entry.route.map(p => [p.lat, p.lng]);
        for (let i = 0; i < coords.length - 1; i++) {
          L.polyline([coords[i], coords[i + 1]], {
            color: '#4f4849',
            weight: 2,
            opacity: 0.5,
            dashArray: '4,6'
          })
          .bindPopup(`<b>${entry.person}</b><br>Reiseabschnitt ${i + 1}`)
          .addTo(map);
        }
      });

      if (allCoords.length > 0) {
        map.fitBounds(allCoords, { padding: [30, 30] });
      }
    }

    // === Filter anwenden ===
    function applyFilters() {
      const selectedPerson = document.getElementById('personFilter').value;

      const filtered = dataArray.filter(entry => {
        return !selectedPerson || entry.person === selectedPerson;
      });

      drawMap(filtered);
    }

    // === Event Listener für Personenfilter ===
    document.getElementById('personFilter').addEventListener('change', applyFilters);

    // === Erste Anzeige aller Daten ===
    drawMap(dataArray);
  })
  .catch(err => {
    console.error('Fehler beim Laden:', err);
    alert('Daten konnten nicht geladen werden.');
  });
