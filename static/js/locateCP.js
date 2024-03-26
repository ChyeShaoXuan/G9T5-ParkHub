const apiKey = "AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY"

function autocompleteInputFunction() {
    var input = document.getElementById("autocompleteInput")
    
    let autocomplete = new google.maps.places.Autocomplete(input)
}

autocompleteInputFunction()

// window.addEventListener('load', autocompleteInput);

// Add event listener to the button
// document.getElementById('searchButton').addEventListener('click', async function(event) {
//     event.preventDefault();

//     try {
//         // Get the input value
//         const address = document.getElementById('autocompleteInput').value;
        
//         console.log(address)

//         // Call the getCoordsForAddress function with the input value
//         const coordinates = await getCoordsForAddress(address) //returns the converted coordinates 
//         console.log('Coordinates:', coordinates);

//         // Convert the result object to JSON format
//         const COORDINATES_JSON = JSON.stringify(coordinates);

//         console.log(COORDINATES_JSON)

//         // Send the JSON data to the Flask microservice
//         // const response = await sendJsonToFlask(COORDINATES_JSON);
//         // console.log('Response from Flask route:', response);
        
//     } 
//     catch (error) {
//         console.error('Error:', error.message);
//         // Handle the error
//     }
// });

// When form is submitted
document.getElementById('infoform').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission
    console.log(sessionStorage.getItem('userID'))
    // Get form data
    try{
    const location = document.getElementById('autocompleteInput').value;
    // const starttime = document.getElementById('starttime').value;
    // const endtime = document.getElementById('endtime').value;

    console.log(location)
    // Send data to microservice
    const coordinates = await getCoordsForAddress(location);
    console.log('Coordinates:', coordinates);

    const COORDINATES_JSON = JSON.stringify(coordinates);
    console.log(COORDINATES_JSON)
    
    } 
    catch (error) {
        console.error('Error:', error.message);
        // Handle the error
    }
});

    // const response = await axios.post('http://localhost:5002/handle_coords', { value: coordinates });
    // console.log('Response from Flask route:', response.data);

    // // Call the Flask microservice to fetch search results
    // const searchResponse = await axios.get('http://localhost:5002/search_results');
    // console.log('Search results:', searchResponse.data);

    // // Update the HTML with the search results
    // const carparkResults = searchResponse.data;
    // let newHTML = '';

    // for (const carpark of carparkResults) {
    //     newHTML += `
    //         <div class="max-w-sm rounded overflow-hidden shadow-lg">
    //             <div class="px-6 py-4">
    //                 Carpark Name:<div class="text-xl mb-2">${carpark['carpark_name']}</div>
    //             </div>
    //             <div class="px-6 pt-4 pb-2">
    //                 <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">lots available: ${carpark['lotsavailable']}</span>
    //                 <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekday rate: ${carpark['rates']['weekdayrate']}</span>
    //                 <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekend rate: ${carpark['rates']['weekendrate']}</span>
    //             </div>
    //             <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mb-5 border border-2 rounded-full">
    //                 Select Carpark
    //             </button>
    //         </div>`;
// }


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
            url: 'http://localhost:5002/handle_coords', //  sent to handle coords in search info
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify({ 'value': coordinates }), 
            success: function(response) { 
                axios.get('http://localhost:5002/search_results')
                    .then(response => { 
                        console.log('Search results:', response);

                        // Check if response data is an empty array
                        console.log('Response data:', response.data);
                        if (response.data.length === 0) {
                            console.log('No search results found');
                            document.getElementById('carparktopresults').innerHTML = "<p>No results found</p>";
                        } else {
                            // Process response data
                            let new_html = '';
                            for (carpark of response.data) {
                                new_html += `
                                <div class="flex justify-center"> <!-- Added flex and justify-center to center horizontally -->
                                    <div class="max-w-sm rounded overflow-hidden shadow-lg">
                                        <div class="px-6 py-4">
                                            Carpark Name:<div class="text-xl mb-2">${carpark['carpark_name']}</div>
                                        </div>
                                        <div class="px-6 pt-4 pb-2">
                                            <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">lots available: ${carpark['lotsavailable']}</span>
                                            <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekday rate: ${carpark['rates']['weekdayrate']}</span>
                                            <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekend rate: ${carpark['rates']['weekendrate']}</span>
                                        </div>
                                        <button onclick="confirmSelection('${carpark['carpark_name']}', '${carpark['google_lat']}', '${carpark['google_lon']}', '${carpark['carparkid']}')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mb-5 border border-2 rounded-full">
                                            Select Carpark
                                        </button>
                                    </div>
                                </div>`;
                            }
                            console.log('Generated HTML:', new_html);
                            document.getElementById('carparktopresults').innerHTML = new_html;
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching search results:', error);
                        // Handle error
                    });
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

function askForNotificationPreference(lat, lng, carparkID) {
    var isConfirmed = confirm("Do you want to receive notifications about your parking session?");
    if (isConfirmed) {
        // User wants to receive notifications
        sendSelectedCP(lat, lng, true, carparkID); 
    } else {
        // User does not want to receive notifications
        sendSelectedCP(lat, lng, false, carparkID); 
    }
}

function confirmSelection(carparkName, lat, lng, carparkID) {
    var isConfirmed = confirm("Confirm selection of " + carparkName + "?");
    if (isConfirmed) {
        askForNotificationPreference(lat, lng, carparkID);
    }
}

// This sends details of the carpark and parking session to session database
async function sendSelectedCP(lat,lng, notifAllowed, carparkID) {
    const data = {
        starttime: document.getElementById('starttime').value,
        endtime: document.getElementById('endtime').value,
        // userID: '007',  
        userID: sessionStorage.getItem('userID'),
        latitude: lat,
        longitude: lng,
        notifAllowed: notifAllowed,
        ppCode: carparkID
    };
    console.log(data);

        $.ajax({ 
            url: 'http://localhost:5006/session',
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify(data), 
            success: function(e) { 
                console.log(e)
                alert('Selection successful!');
            }, 
            error: function(xhr, status, error) { 
                console.log("Error: " + xhr.responseText);
            }
        });

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
