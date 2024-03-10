// Replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual Google Maps API key
const apiKey = 'AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY';

function initMap() {
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            console.log(navigator)

            console.log(userLocation)
            
            const latElement = document.getElementById("lat");
            latElement.textContent = "lat: " + userLocation.lat;

            const lngElement = document.getElementById("lng");
            lngElement.textContent = "lng: " + userLocation.lng;

            const service = new google.maps.places.PlacesService(document.createElement('div'));

            const request = {
                location: userLocation,
                radius: 500, // You can adjust the radius as needed
                type: ['parking'], // Include multiple types of places you want to display
            };

            service.nearbySearch(request, function (results, status) {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                        // results.slice(0, 9).forEach(function (place, index) 

                    console.log(results)
                    let container = document.getElementById("top10")

                    let print_str = '<ol>'

                    for (let i = 0; i < 10; i++) {
                        const place = results[i];
                        print_str += `<li>${place.name}</li>`;
                    }
            
                    print_str += '</ol>';
                    container.innerHTML += print_str;

                }
            });
        });
    } else {
        alert('Geolocation is not supported in your browser');
    }
}

initMap()