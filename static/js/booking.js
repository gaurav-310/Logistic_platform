let map, directionsService, directionsRenderer;

function initMap() {
    // Initialize the map and services
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 28.6139, lng: 77.209 },
        zoom: 8
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    // Initialize Places Autocomplete for Pickup and Dropoff inputs
    new google.maps.places.Autocomplete(document.getElementById('id_pickup_location'));
    new google.maps.places.Autocomplete(document.getElementById('id_dropoff_location'));

    // Add event listener to the form submission
    document.getElementById('booking-form').addEventListener('submit', handleFormSubmit);
}

async function handleFormSubmit(event) {
    event.preventDefault(); // Prevent form from submitting immediately

    const pickupPlace = document.getElementById('id_pickup_location').value;
    const dropoffPlace = document.getElementById('id_dropoff_location').value;

    // Validate that a vehicle type is selected
    const vehicleTypeSelect = document.getElementById('id_vehicle_type');
    const vehicleType = vehicleTypeSelect.value;

    if (!vehicleType) {
        alert("Please select a vehicle type.");
        return;
    }

    // Call the API to calculate the route
    try {
        const results = await directionsService.route({
            origin: pickupPlace,
            destination: dropoffPlace,
            travelMode: google.maps.TravelMode.DRIVING,
        });

        // Render the directions on the map
        directionsRenderer.setDirections(results);
        const route = results.routes[0];
        const distanceInMeters = route.legs[0].distance.value;
        const distanceInKm = distanceInMeters / 1000;

        // Display the distance
        document.getElementById('distance-display').value = distanceInKm.toFixed(2) + ' km';

        // Update the hidden form input for distance
        document.getElementById('id_distance').value = distanceInKm.toFixed(2);

        // Calculate and display estimated cost
        calculateEstimatedCost(distanceInKm);

        // Optionally, you can submit the form here if needed
        // document.getElementById('booking-form').submit();

    } catch (error) {
        alert('An error occurred while calculating the route. Please try again.');
        console.error(error);
    }
}

function calculateEstimatedCost(distanceInKm) {
    const vehicleTypeSelect = document.getElementById('id_vehicle_type');
    const selectedOption = vehicleTypeSelect.options[vehicleTypeSelect.selectedIndex];

    // Fetch the base fare and cost per km from the selected vehicle option
    const baseFare = parseFloat(selectedOption.getAttribute('data-base-fare'));
    const costPerKm = parseFloat(selectedOption.getAttribute('data-cost-per-km'));

    // Check if the attributes are valid numbers
    if (isNaN(baseFare) || isNaN(costPerKm)) {
        alert("Invalid vehicle type data. Please try again.");
        return;
    }

    // Calculate estimated cost
    const estimatedCost = baseFare + (distanceInKm * costPerKm);

    // Display the estimated cost
    document.getElementById('estimated-cost-display').value = '$' + estimatedCost.toFixed(2);

    // Update the hidden form input for estimated cost
    document.getElementById('id_estimated_cost').value = estimatedCost.toFixed(2);
}

// Expose the initMap function to the global scope
window.initMap = initMap;
