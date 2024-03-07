from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)

ura_URL="https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details"
ura_headers={'AccessKey':'e61ff773-ba6b-4e89-aeda-759e0bc55604',
             'Token':'acedbp@khNkfP+wHJnk-U3475Prg9@MJ7fyET2e3-e5-YRe45E+H5HbTePceU@JebS2zvbFUZbAe95@C52FYfF+kffaTQ5yeaDD-'}

@app.route('/locate', methods=['POST'])
# def handle_location_request():
#     data = request.json
#     location = data.get('location')
    
#     # Perform your Geocoding and Nearby Search API calls here using the location

#     # Dummy response for illustration
#     response_data = {"message": "Results found", "results": []}
#     return jsonify(response_data)




#token
#api_key



def make_get_request(url, headers=ura_headers):
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
url = "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details"
custom_headers = {
    "AccessKey": "e61ff773-ba6b-4e89-aeda-759e0bc55604",  # Example custom header
    "Token": "acedbp@khNkfP+wHJnk-U3475Prg9@MJ7fyET2e3-e5-YRe45E+H5HbTePceU@JebS2zvbFUZbAe95@C52FYfF+kffaTQ5yeaDD-",
    'User-Agent': 'PostmanRuntime/7.28.4',
    'Cookie': 'BIGipServerIAPP-HTTPS_A83-WWW.URA.GOV.SG_V4.app~IAPP-HTTPS_A83-WWW.URA.GOV.SG_V4_pool=!z0XVV5FkuQdCmN1CNQC8y2lWE3egLN/KKai61thY7Ni7WgSTHDm7rFYdZdydhkW3TPT1pit5ATmlEMU=; TS019d87de=01c9d36efc676e7a8a518d67985c9a128171baa74a24b4b25dee67ed071f25d6751f393ca9327f547898e23ec6d7702e73738d0b42'  # Example authorization header
}

response = make_get_request(url, headers=custom_headers)

if response:
    print(f"Status Code: {response.status_code}")
    print("Response Content:")
    print(response.text)
else:
    print("Failed to make the GET request.")







if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)