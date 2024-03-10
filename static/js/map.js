let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

// initMap();

// const loader = new Loader({
//   apiKey: "AIzaSyDll2EpYsFOl5O8zKy0CmZucV59DPtXV7Q",
//   version: "weekly",
// });

// loader.load().then(async () => {
//   const { Map } = await google.maps.importLibrary("maps");

//   map = new Map(document.getElementById("map"), {
//     center: { lat: -34.397, lng: 150.644 },
//     zoom: 8,
//   });
// });

// Initialize map variable
// let map;

// // Function to initialize the map
// function initMap() {
//   // Create a new map instance
//   map = new google.maps.Map(document.getElementById("map"), {
//     center: { lat: -34.397, lng: 150.644 },
//     zoom: 8,
//   });
// }

// // Use Google Maps API loader to asynchronously load the Maps library
// const loader = new google.maps.plugins.loader.Loader({
//   apiKey: "AIzaSyDll2EpYsFOl5O8zKy0CmZucV59DPtXV7Q",
//   version: "weekly",
// });

// // Load the Maps library and initialize the map
// loader.load().then(() => {
//   // Call initMap function once the Maps library is loaded
//   initMap();
// });
