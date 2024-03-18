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
