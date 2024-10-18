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
function initAutocomplete() {
    const input = document.getElementById('current_location');
    const autocomplete = new google.maps.places.Autocomplete(input);
}

google.maps.event.addDomListener(window, 'load', initAutocomplete);
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

        // Show the confirm booking button
        document.getElementById('confirm-button').style.display = 'inline-block';
        
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
function confirmBooking() {
    const pickupLocation = document.getElementById('id_pickup_location').value;
    const dropoffLocation = document.getElementById('id_dropoff_location').value;
    const vehicleType = document.getElementById('id_vehicle_type').value;
    const date = document.getElementById('id_date').value;
    const estimatedCost = document.getElementById('estimated-cost-display').value.replace('₹ ', '');

    // Prepare the data to send
    const bookingData = {
        pickup_location: pickupLocation,
        dropoff_location: dropoffLocation,
        vehicle_type: vehicleType,
        date: date,
        estimated_cost: estimatedCost,
    };

    // Get CSRF token
    const csrftoken = getCookie('csrftoken');

    // Send the POST request to the server
    fetch('/bookings/confirm/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(bookingData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);  // Show success message
            window.location.href = "/accounts/user_dashboard/";  // Redirect to the user dashboard
        } else if (data.error) {
            alert(data.error);  // Show error message from server
        } else {
            alert('An unknown error occurred.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const cookieTrimmed = cookie.trim();
            if (cookieTrimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookieTrimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Confirm Booking and send details to the server (called on 'Confirm Booking')
// function confirmBooking() {
//     const pickupLocation = document.getElementById('id_pickup_location').value;
//     const dropoffLocation = document.getElementById('id_dropoff_location').value;
//     const vehicleType = document.getElementById('id_vehicle_type').value;
//     const date = document.getElementById('id_date').value;
//     const estimatedCost = document.getElementById('estimated-cost-display').value;

//     const bookingData = {
//         pickup_location: pickupLocation,
//         dropoff_location: dropoffLocation,
//         vehicle_type: vehicleType,
//         date: date,
//         estimated_cost: estimatedCost,
//     };

//     // AJAX request to send booking data to the server
//     fetch('/bookings/confirm/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//         },
//         body: JSON.stringify(bookingData),
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.message) {
//             alert(data.message);  // Show success message
//             window.location.href = "/accounts/user_dashboard/";  // Redirect to the user dashboard
//         } else {
//             alert('An error occurred while confirming the booking.');
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }

// Prevent default form submission
document.getElementById('booking-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from being submitted and page from reloading
    calculateRoute();
});

// Initialize the map when the window loads
window.onload = function() {
    initMap();
};
