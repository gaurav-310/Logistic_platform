
    function initAutocomplete() {
        var input = document.getElementById('id_location');
        var autocomplete = new google.maps.places.Autocomplete(input);

        // Bias the autocomplete object to the user's geographical location, as supplied by the browser's 'navigator.geolocation' object.
        autocomplete.setFields(['address_components', 'geometry', 'name']);

        autocomplete.addListener('place_changed', function() {
            var place = autocomplete.getPlace();
            if (!place.geometry) {
                // User entered the name of a place that was not suggested and pressed the Enter key
                window.alert("No details available for input: '" + place.name + "'");
                return;
            }

            // If you want to use the place details, do so here.
            var lat = place.geometry.location.lat();
            var lng = place.geometry.location.lng();
            console.log("Latitude: " + lat + ", Longitude: " + lng);
        });
    }

    // Initialize autocomplete when the window loads
    window.onload = function() {
        initAutocomplete();
    };
