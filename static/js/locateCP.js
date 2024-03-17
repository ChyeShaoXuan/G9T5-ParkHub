
const apiKey = "AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY"

function autocompleteInputFunction() {
    var input = document.getElementById("autocompleteInput")
    
    let autocomplete = new google.maps.places.Autocomplete(input)
}

autocompleteInputFunction()

// window.addEventListener('load', autocompleteInput);

// Add event listener to the button
document.getElementById('searchButton').addEventListener('click', async function(event) {
    event.preventDefault();

    try {
        // Get the input value
        const address = document.getElementById('autocompleteInput').value;
        
        console.log(address)

        // Call the getCoordsForAddress function with the input value
        const coordinates = await getCoordsForAddress(address) //returns the converted coordinates 
        console.log('Coordinates:', coordinates);

        // Convert the result object to JSON format
        const COORDINATES_JSON = JSON.stringify(coordinates);

        console.log(COORDINATES_JSON)

        // Send the JSON data to the Flask microservice
        const response = await sendJsonToFlask(COORDINATES_JSON);
        console.log('Response from Flask route:', response);
        
    } 
    catch (error) {
        console.error('Error:', error.message);
        // Handle the error
    }
});

async function getCoordsForAddress(address) {
    try {
        const response = await axios.get(
            `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${apiKey}`
        );

        const data = response.data;
        console.log(data)

        if (!data || data.status === 'ZERO_RESULTS') {
            throw new Error('Could not find location for the specified address.');
        }

        const coordinates = data.results[0].geometry.location;

        return coordinates;
    } 
    catch (error) {
        console.error('Error:', error.message);
        throw error;
    }
}

async function sendJsonToFlask(COORDINATES_JSON) {
    try {
        const response = await axios.post('/locate-CP', {
            coordinates_json : COORDINATES_JSON
        });
        return response.data;
    } catch (error) {
        console.error('Error sending data to Flask route:', error.message);
        throw error;
    }
}
