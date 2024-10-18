// You can add any interactive JS functionalities for the dashboard here.
document.addEventListener('DOMContentLoaded', function () {
    console.log("Driver dashboard JS loaded");
    // Example JS functionality: auto-focus on location input
    const locationInput = document.getElementById('current_location');
    if (locationInput) {
        locationInput.focus();
    }
});
