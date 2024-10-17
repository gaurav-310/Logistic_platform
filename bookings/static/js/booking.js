let map, directionsService, directionsRenderer;

// Initialize the Google Map and directions service
function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();

    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 28.6139, lng: 77.209 },
        zoom: 8
    });

    directionsRenderer.setMap(map);

    // Initialize autocomplete for pickup and dropoff fields
    new google.maps.places.Autocomplete(document.getElementById('id_pickup_location'));
    new google.maps.places.Autocomplete(document.getElementById('id_dropoff_location'));
}

// Function to calculate the route and display results
async function calculateRoute() {
    const pickupPlace = document.getElementById('id_pickup_location').value;
    const dropoffPlace = document.getElementById('id_dropoff_location').value;

    if (!pickupPlace || !dropoffPlace) {
        alert('Please enter both pickup and dropoff locations');
        return;
    }

    try {
        const results = await directionsService.route({
            origin: pickupPlace,
            destination: dropoffPlace,
            travelMode: google.maps.TravelMode.DRIVING,
        });

        directionsRenderer.setDirections(results);
        const route = results.routes[0];
        const distanceInMeters = route.legs[0].distance.value;
        const distanceInKm = distanceInMeters / 1000;

        // Display the distance and cost
        document.getElementById('distance-display').value = distanceInKm.toFixed(2) + ' km';
        calculateEstimatedCost(distanceInKm);

        // Show the map and details
        document.getElementById('map').style.display = 'block';
        document.getElementById('details').style.display = 'block';
    } catch (error) {
        alert('An error occurred while calculating the route. Please try again.');
        console.error(error);
    }
}

// Function to calculate the estimated cost
function calculateEstimatedCost(distanceInKm) {
    const vehicleTypeSelect = document.getElementById('id_vehicle_type');
    const selectedOption = vehicleTypeSelect.options[vehicleTypeSelect.selectedIndex];
    const costPerKm = parseFloat(selectedOption.getAttribute('data-cost-per-km'));
    const baseFare = parseFloat(selectedOption.getAttribute('data-base-fare'));

    // Calculate estimated cost
    const estimatedCost = baseFare + distanceInKm * costPerKm;

    // Display the estimated cost
    document.getElementById('estimated-cost-display').value = '₹ ' + estimatedCost.toFixed(2);
}

// Prevent default form submission
document.getElementById('booking-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from being submitted and page from reloading
    calculateRoute();
});

// Initialize the map when the window loads
window.onload = function() {
    initMap();
};
