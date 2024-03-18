from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
app = Flask(__name__)
CORS(app)


@app.route('/results_coords', methods=['POST','GET'])
def retrievecoordinates():
    try:
        
        data = request.get_json()
        print(data['value'])
        global coords_object
        coords_object=data['value']
        return data['value']

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the session. " + str(e)
            }
        ), 500

@app.route('/google_results')
def make_google_request():
    
    
    coords_lat=coords_object['lat']
    
    coords_lon=coords_object['lng']
    coords_str=str(coords_lat)+","+str(coords_lon)
    
    
    try:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius=2000&types=parking&sensor=false&key=AIzaSyBNWtyHG53pXtomi6KJL9ZH4Erituy6FNE".format(coords_str)
        response = requests.get(url)
        response.raise_for_status()
        response=response.json()
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return None












if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
