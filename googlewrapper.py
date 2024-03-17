from flask import Flask
from flask_cors import CORS
import json
import requests
app = Flask(__name__)
CORS(app)

google_URL="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=1.3068714444563487,103.9351283404665&radius=2000&types=parking&sensor=false&key=AIzaSyBNWtyHG53pXtomi6KJL9ZH4Erituy6FNE"



@app.route('/google_results')
def make_post_request(url=google_URL):
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses 
        response=response.json()
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return None



@app.route('/google_result', methods=['POST'])
def retrievecoordinates():
    try:
        data = request.get_json()
        print(data)

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the session. " + str(e)
            }
        ), 500








if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=False)
