
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
        $.ajax({ 
            url: 'http://localhost:5002/handle_coords', 
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify({ 'value': coordinates }), 
            success: function(response) { 
                axios.get('http://localhost:5002/search_results')
                .then(response => { 
                    console.log(response.data);
                    new_html=''
                    
                    for(carpark of response.data){
                       new_html+=`<div class="max-w-sm rounded overflow-hidden shadow-lg">
                       
                       <div class="px-6 py-4">
                         <div class="font-bold text-xl mb-2">${carpark['carpark_name']}</div>
                         
                       </div>
                       <div class="px-6 pt-4 pb-2">
                         <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">lots available:${carpark['lotsavailable']}</span>
                         <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekday rate:${carpark['rates']['weekdayrate']}</span>
                         <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekend rate:${carpark['rates']['weekendrate']}</span>
                       </div>
                     </div>`
                    // new_html+=`${carpark['carpark_name']}`;
                    }
                    document.getElementById('carparktopresults').innerHTML=new_html
                  
                  
                    
              
                  })
                  .catch(error => {
              
                      // ERROR
                      // Something went wrong
                      console.log(error.message)
                  })
            }, 
            error: function(error) { 
                console.log(error); 
            } 
        });
        return coordinates;
    } 
    catch (error) {
        console.error('Error:', error.message);
        throw error;
    }
}

// async function sendJsonToFlask(COORDINATES_JSON) {
//     try {
//         const response = await axios.post('/locate-CP', {
//             coordinates_json : COORDINATES_JSON
//         });
//         return response.data;
//     } catch (error) {
//         console.error('Error sending data to Flask route:', error.message);
//         throw error;
//     }
// }
