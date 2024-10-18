// booking_detail.js

function initMap() {
    var mapOptions = {
        zoom: 10,
        center: { lat: -34.397, lng: 150.644 } // Default center, will be reset later
    };
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    var bounds = new google.maps.LatLngBounds();

    if (typeof driverCurrentLocation !== 'undefined' && typeof bookingDropoffLocation !== 'undefined') {
        var geocoder = new google.maps.Geocoder();

        // Geocode the driver's current location
        geocoder.geocode({ 'address': driverCurrentLocation }, function (results, status) {
            if (status === 'OK') {
                var driverLocation = results[0].geometry.location;
                var driverMarker = new google.maps.Marker({
                    map: map,
                    position: driverLocation,
                    label: 'Driver'
                });
                bounds.extend(driverLocation);
                map.fitBounds(bounds);
            } else {
                console.error('Geocode was not successful for the following reason: ' + status);
            }
        });

        // Geocode the drop-off location
        geocoder.geocode({ 'address': bookingDropoffLocation }, function (results, status) {
            if (status === 'OK') {
                var dropoffLocation = results[0].geometry.location;
                var dropoffMarker = new google.maps.Marker({
                    map: map,
                    position: dropoffLocation,
                    label: 'Drop-off'
                });
                bounds.extend(dropoffLocation);
                map.fitBounds(bounds);
            } else {
                console.error('Geocode was not successful for the following reason: ' + status);
            }
        });
    } else {
        console.error('Driver current location or booking drop-off location is not defined.');
    }
}

google.maps.event.addDomListener(window, 'load', initMap);
