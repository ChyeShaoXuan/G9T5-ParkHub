<<<<<<< Updated upstream
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys, requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

session_record_url='http://localhost:5006/session'
nearby_amenities_url = 'http://localhost:5005/nearby_amenities'

# 1. Send request to view nearby amenities around selected car park
@app.route("/request_na", methods=['POST'])
def request_na():
    # Simple check of input format and data of the request are JSON
    # input is selected filters, selected carpark, userID, package all into json
    
    if request.is_json:
        try:
            # request_json = request.get_json()
            request_json = 
            print("\nReceived an order in JSON:", request_json)

            # do the actual work
            # 1. Send order info {cart items}
            result = processSearchAmenities(request_json)
            return jsonify(result), result["code"]
        
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "searchAmenities.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processSearchAmenities(json_details):
    #2. Request location of selected carpark
    # Invoke the session_record microservice
    print('\n-----Invoking session_record microservice-----')
    session_record_result = invoke_http(session_record_url, method='POST', json=json_details)
    print('order_result:', session_record_result)

    #3. 


request_na()

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
    app.run(host='0.0.0.0', port=5010, debug=False)
=======
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys, requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

userID = 9 #hardcoded later retrieve from stored value

session_getlocation_url=f'http://localhost:5006/session/location/{userID}'
nearby_amenities_wrapper_url = 'http://localhost:5011/nearby_amenities_request'

#example:
# sendto_nearbyAmenities = { userID : 6, 
#                            selectedFilters: ['carwash', 'restaurant'],
#                            latitude: 1.387,
#                           longitude: 130.555               
#                           }



@app.route("/search_amenities", methods=['POST', 'GET'])
def search_amenities():
    data = request.json
    selectedFilters = data.get('selectedFilters', [])

    #location
    location_result = invoke_http(session_getlocation_url, method='GET')
    print(location_result)
    latitude = location_result['data']['latitude']
    longitude = location_result['data']['longitude']

    # Package the data into JSON
    payload = {
        'userID': userID,
        'selectedFilters': selectedFilters,
        'latitude': latitude,
        'longitude': longitude
    }
    
    print(payload)
    response = invoke_http(nearby_amenities_wrapper_url, method='POST', json=payload)

    print(response)

    return jsonify(response)



# 1. Send request to view nearby amenities around selected car park
# @app.route("/receive_details", methods=['POST'])
# def receive_details():
#     #receive details from nearbyAmenities.js (filters, userID) as JSON
    
#     data = request.json
#     selectedFilters = data.get('selectedFilters', [])

#     print(30, selectedFilters)
#     return selectedFilters


# def get_location_from_session_record():

#     #2. Request location of selected carpark (sends userid, get back location)
#     # Invoke the session_record microservice
#     print('\n-----Invoking session_record microservice-----')
#     # session_getlocation_url=f'http://localhost:5001/session/{userID}'

#     #3. Returns location of selected car park
#     result = invoke_http(session_getlocation_url, method='GET')
#     latitude = result['data']['latitude']
#     longitude = result['data']['longitude']
#     print('Latitude: ', latitude)
#     print('Longitude: ', longitude)

#     return latitude, longitude
    
# @app.route("/send_to_nearby_amenities_wrapper", methods=['POST'])
# def send_details():

#     selectedFilters = receive_details()
#     latitude, longitude = get_location_from_session_record()

#     print(selectedFilters, latitude, longitude)

#     # Package the data into JSON
#     payload = {
#         'userID': userID,
#         'selectedFilters': selectedFilters,
#         'latitude': latitude,
#         'longitude': longitude
#     }

#     print(payload)
#     # Now you can send this payload to other functions or microservices

#     return jsonify({'message': 'Data received successfully', 'data': payload})

#     # invoke_http(nearby_amenities_wrapper_url, methods=['POST'], json=payload)


#     #4. Sends location of selected car park (coordinates) and #selected filters (carwash = 1, restaurants = 1, gas station = 1)


#     #5. Requests for nearby amenities  with location and selected filters

#     #6. Returns nearby amenities

#     #7. Returns nearby amenities details


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
    app.run(host='0.0.0.0', port=5010, debug=True)
>>>>>>> Stashed changes
