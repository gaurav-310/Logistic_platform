// static/js/booking_detail.js

let map, directionsService, directionsRenderer;

// Initialize the Google Map and directions service

function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();

    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 28.6139, lng: 77.209 }, // Default center, can be adjusted
        zoom: 8
    });

    directionsRenderer.setMap(map);

    // Now, calculate and display the route
    calculateRoute();
}

// Function to calculate the route and display results
async function calculateRoute() {
    const driverLocation = driverCurrentLocation;
    const dropoffLocation = bookingDropoffLocation;

    if (!driverLocation || !dropoffLocation) {
        alert('Driver or dropoff location not available.');
        return;
    }

    try {
        const results = await directionsService.route({
            origin: driverLocation,
            destination: dropoffLocation,
            travelMode: google.maps.TravelMode.DRIVING,
        });

        directionsRenderer.setDirections(results);
        const route = results.routes[0];
        const distanceInMeters = route.legs[0].distance.value;
        const distanceInKm = distanceInMeters / 1000;
        const duration = route.legs[0].duration.text;

        // Display the distance and estimated time
        document.getElementById('distance-display').value = distanceInKm.toFixed(2) + ' km';
        document.getElementById('duration-display').value = duration;

    } catch (error) {
        alert('An error occurred while calculating the route. Please try again.');
        console.error(error);
    }
}

// Initialize the map when the window loads
window.onload = function() {
    initMap();
};
