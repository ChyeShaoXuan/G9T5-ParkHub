
async function request_nearby_amenities() {
    // Event listener for the submit button click
    document.getElementById('search_amenities_btn').addEventListener('click', function() {
        // Array to store the selected checkboxes values
        let selectedFilters = [];

        // Check if the checkbox is checked, if yes, add its value to the array
        if (document.getElementById('carwash-checkbox').checked) {
            selectedFilters.push(document.getElementById('carwash-checkbox').value);
        }
        if (document.getElementById('restaurant-checkbox').checked) {
            selectedFilters.push(document.getElementById('restaurant-checkbox').value);
        }
        if (document.getElementById('gas-station-checkbox').checked) {
            selectedFilters.push(document.getElementById('gas-station-checkbox').value);
        }

    //     // Log the selected filters for demonstration purposes
    //     console.log(selectedFilters);

    //     fetch('http://localhost:5010/search_amenities', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify(
    //         { selectedFilters: selectedFilters }
    //     )
    // })

        try {
            
            $.ajax({ 
                url: 'http://localhost:5010/search_amenities', //  searchInfo/handle_coords
                type: 'POST', 
                contentType: 'application/json', 
                data: JSON.stringify(
                    { selectedFilters: selectedFilters }
                ), 
                success: function(response) { 
                    // axios.get('http://localhost:5010/search_amenities')
                    //     .then(response => { 
                    //             console.log(response)
                    //         }
                    //     )
                    //     .catch(error => {
                    //         console.error('Error fetching search results:', error);
                    //         // Handle error
                    //     });
                    console.log(response)
                    index = 0
                    result_string = ''
                    nearby_amenities_container = document.getElementById("nearby_amenities_results")

                    let location_array_of_dicts = response
                    console.log(selectedFilters)
                    location_array_of_dicts.forEach(function(each_result) {
                        // console.log(each_result)
                        // console.log(each_result.types, types[index])

                        // Split the string at commas and trim whitespace
                        let typesArray = each_result.type.split(',').map(type => type.trim());
                        console.log(typesArray)
                        
                        for(each_type of typesArray) {
                            if (each_type === selectedFilters[index]) {
                                // name of place, address, photo
                                // console.log(222222222222, each_result.type)
                                place_name = each_result.name
                                place_type = each_type
                                place_address = each_result.address
                                place_photo = each_result.photo

                                    result_string += `<div class="max-w-xs w-full sm:w-1/2 md:w-1/3 lg:w-1/4 mr-5">
                                                        <div class="flex flex-col justify-center items-center outline outline-1 rounded bg-white overflow-hidden shadow-lg pt-5">
                                                            <div class="items-start px-6 py-4">
                                                                <img src="${place_photo}" class="rounded w-64 h-64 " >
                                                                <div class="text-left px-6 py-4">
                                                                    <p class="mb-2">Type: ${place_type}</p>
                                                                    <p class="mb-2">Name: ${place_name}</p>
                                                                    <p class="mb-2">Address: ${place_address}</p>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>`;
                                console.log(place_type)
                                index += 1
                            }
                        }
                        
                    })
                    nearby_amenities_container.innerHTML = result_string


                }, 
                error: function(error) { 
                    console.log(error); 
                } 
            });
        } 
        catch (error) {
            console.error('Error:', error.message);
            throw error;
        }
        
    });
}

request_nearby_amenities()





// Define a function to fetch nearby amenities based on selected filters and user location
// async function fetchNearbyAmenities() {
//     try {
//         // Fetch the data from the receive_details endpoint
//         // const response = await fetch('http://localhost:5011/receive_details', {
//         //     method: 'POST', // Change the method to POST
//         //     headers: {
//         //         'Content-Type': 'application/json'
//         //     },
//         //     body: JSON.stringify({}) // Send an empty JSON object as the payload
//         // });
        
//         $.ajax({ 
//             url: 'http://localhost:5010/search_amenities', //  searchInfo/handle_coords
//             type: 'POST', 
//             contentType: 'application/json', 
//             data: JSON.stringify( { selectedFilters: selectedFilters }), 
//             success: function(response) { 
//                 // axios.get('http://localhost:5010/return_to_UI')
//                 //     .then(response => { 
//                 //         console.log('Search results:', response);
//                 //         })
//                 //     .catch(error => {
//                 //         console.error('Error fetching search results:', error);
//                 //         // Handle error
//                 //     })
//                 }
            
//         })
            
//         // Extract the JSON data from the response
//         const data = await response.json();

//         // Return the received data
//         return data;

//     } catch (error) {
//         console.error('Error:', error);
//         return null; // Return null if an error occurs
//     }
// }


// async function getNearbyAmenities() {

//     const responseData = await fetchNearbyAmenities();

//         // Check if data is received successfully
//         if (responseData) {
//             console.log(responseData, 11111111111);
    
//             // Your existing logic to fetch nearby amenities can go here
//             // You can use the responseData as needed
    
//             // Example:
//             // const types = responseData.types;
//             // const userLocation = responseData.userLocation;
//             // const selectedFilters = responseData.selectedFilters;
//             // Perform actions based on the received data
    
//         } else {
//             console.error('Failed to fetch nearby amenities data.');
//         }
//     let types;

//     if ('geolocation' in navigator) {
//         // console.log(navigator)

//         navigator.geolocation.getCurrentPosition(async function (position) {
//             userLocation = {
//                 lat: position.coords.latitude,
//                 lng: position.coords.longitude
//             } 
//             const service = new google.maps.places.PlacesService(document.createElement('div'));
//             types = ['car_wash', 'gas_station', 'point_of_interest']

//             const request = {
//                 location: userLocation, 
//                 radius: 3000, // You can adjust the radius as needed
//                 types: types, // types: selectedFilters
//             };
            
//             service.nearbySearch(request, function (results, status) {
//                 if (status === google.maps.places.PlacesServiceStatus.OK) {
//                     // console.log(results)
//                     console.log(types)
//                     index = 0
//                     result_string = ''
//                     nearby_amenities_container = document.getElementById("nearby_amenities_results")

//                     let location_array_of_dicts = results
//                     console.log(results)

//                     location_array_of_dicts.forEach(function(each_result) {
//                         // console.log(each_result)
//                         // console.log(each_result.types, types[index])
//                         if (each_result.types.includes(types[index])) {
//                             // name of place, address, photo
//                             place_name = each_result.name
//                             place_type = types[index]
//                             place_address = each_result.vicinity
//                             place_photo = each_result.photos[0].getUrl(  {maxWidth: 400, maxHeight: 400} )

//                                 result_string += `<div class="max-w-xs w-full sm:w-1/2 md:w-1/3 lg:w-1/4 mr-5">
//                                                     <div class="flex flex-col justify-center items-center outline outline-1 rounded bg-white overflow-hidden shadow-lg pt-5">
//                                                         <div class="items-start px-6 py-4">
//                                                             <img src="${place_photo}" class="rounded w-64 h-64 " >
//                                                             <div class="text-left px-6 py-4">
//                                                                 <p class="mb-2">Type: ${place_type}</p>
//                                                                 <p class="mb-2">Name: ${place_name}</p>
//                                                                 <p class="mb-2">Address: ${place_address}</p>
//                                                             </div>
//                                                         </div>
//                                                     </div>
//                                                 </div>`;
//                             console.log(place_type)
//                             index += 1
                            
//                         }
//                     })
//                     nearby_amenities_container.innerHTML = result_string

//                 }
//             })
//         })
//     }
// }

// getNearbyAmenities()