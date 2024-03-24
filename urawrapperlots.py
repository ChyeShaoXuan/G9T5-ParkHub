from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from math import radians, sin, cos, sqrt, atan2
import requests
app = Flask(__name__)
CORS(app)

ura_URL="https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details"
custom_headers = {
    "AccessKey": "e61ff773-ba6b-4e89-aeda-759e0bc55604",  # Example custom header
    # token needs to be changed every day.
    "Token": "h@Va9r4Zb6-6RC3W96aP4b8V-SDw4jFYs-97QQWS51qyewgZ8b8wBemNnDfceux3Pf75@mk6Gmh5DgHqzfVYky7Gbdee74-2Q7wC",
    'User-Agent': 'PostmanRuntime/7.28.4',
    'Cookie': 'BIGipServerIAPP-HTTPS_A83-WWW.URA.GOV.SG_V4.app~IAPP-HTTPS_A83-WWW.URA.GOV.SG_V4_pool=!z0XVV5FkuQdCmN1CNQC8y2lWE3egLN/KKai61thY7Ni7WgSTHDm7rFYdZdydhkW3TPT1pit5ATmlEMU=; TS019d87de=01c9d36efc676e7a8a518d67985c9a128171baa74a24b4b25dee67ed071f25d6751f393ca9327f547898e23ec6d7702e73738d0b42'  # Example authorization header
}
# call postman via the url https://www.ura.gov.sg/uraDataService/insertNewToken.action with GET request, 
# enter header which is the accesskey. The response will give the token to be used for the day.
def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in meters (mean value)
    earth_radius = 6371000

    # Calculate the distance
    distance = earth_radius * c

    return distance


@app.route('/ura_results')
def make_get_request(url, headers=custom_headers):
    """
    Make a GET request with optional headers.

    Parameters:
    - url (str): The URL to make the GET request to.
    - headers (dict, optional): A dictionary of headers to include in the request.

    Returns:
    - requests.Response: The response object containing the server's response.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return None

# Example usage:
url = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"
custom_headers = {
    'AccountKey': 'kkFPEYubRJqbnVDK5CmanA==',
    'User-Agent': 'PostmanRuntime/7.28.4',
    'accept':'application/json'
    }

response = make_get_request(url, headers=custom_headers)
sample_coords_lat=1.3072638
sample_coords_long=103.9356894
if response:
    print(f"Status Code: {response.status_code}")
    print("Response Content:")
    response=response.json()
    for carpark in response["value"]:
        
        
          carpark_coordinates=carpark['Location']
        #   print(carpark_coordinates)
          split_str=carpark_coordinates.split()
          
          if len(split_str)>0:
            lta_lat=float(split_str[0])
            lta_lon=float(split_str[1])
          
            if(haversine_distance(sample_coords_lat,sample_coords_long,lta_lat,lta_lon)<20):
        #[0]['coordinates']=="37372.641,42214.218":
              print(carpark['CarParkID'])
        # else:
        #     print("no")
    
    

else:
    print("Failed to make the GET request.")






if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001,debug=False)