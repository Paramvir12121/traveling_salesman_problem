document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([43.704604, -79.398569], 13);  // Set initial map view

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Function to add a route to the map
    function drawRoute(coordinates) {
        var latlngs = coordinates.map(coord => [coord[1], coord[0]]); // Convert [lon, lat] to [lat, lon]
        var polyline = L.polyline(latlngs, {color: 'blue'}).addTo(map);
        map.fitBounds(polyline.getBounds()); // Fit map to the polyline's bounds
    }

    // Capture form submission with htmx
    document.body.addEventListener('htmx:afterRequest', function (event) {
        if (event.detail.xhr.status === 200) {
            var response = event.detail.xhr.response;
            var data = JSON.parse(response);
            if (data.routes && data.routes.length > 0) {
                drawRoute(data.routes[0].geometry.coordinates);
            }
        }
    });
});