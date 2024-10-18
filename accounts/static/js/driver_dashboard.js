function initAutocomplete() {
    const input = document.getElementById('current_location');
    const autocomplete = new google.maps.places.Autocomplete(input);
}

google.maps.event.addDomListener(window, 'load', initAutocomplete);