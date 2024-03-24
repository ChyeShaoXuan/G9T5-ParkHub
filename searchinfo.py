# 5002 is the port of searchinfo.py complex microservice
from flask import Flask, request,jsonify

from flask_cors import CORS
from math import radians, sin, cos, sqrt, atan2
from invokes import invoke_http
app = Flask(__name__)
CORS(app)

googlewrapper_url='http://localhost:5000/google_results'
ltawrapper_url='http://localhost:5001/lta_results'
urawrapper_url='http://localhost:5003//ura_rates/'

#helper function to calculate distance between 2 points
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

@app.route('/handle_coords',methods=['POST'])
def handle_data():
   data=request.get_json()
   print(data)
   invoke_http('http://localhost:5000/results_coords',method='POST', json=data)

   return data
    
@app.route('/search_results')
def processreturntopcarparks():
    #invoke googlewrapper function and return results
    google_response=invoke_http(googlewrapper_url,method='GET')
    google_result=google_response['results']
    print(222222)
    print()
    # print(google_result[0])
    #invoke ltawrapperlots and return results
    lta_response=invoke_http(ltawrapper_url,method='GET')
    lta_carparks=lta_response['value']
    # print(lta_carparks)
    #invoke urawrapper_rates and return results
    
    #nested loop to match google and lta results. 
    
    #Some offset is needed here as both APIs return results around 20m away from each other. We use the helper function to match the results.
    results_list=[]
    for google_car_park in google_result:
        google_lat=google_car_park['geometry']['location']['lat']
        google_lon=google_car_park['geometry']['location']['lng'] 
        carpark_name=google_car_park['name']
        print(google_lat,google_lon, carpark_name)
        for lta_carpark in lta_carparks:    
        
          lta_coordinates=lta_carpark['Location']
          
          split_str=lta_coordinates.split()
          
          if len(split_str)>0:
             lta_lat=float(split_str[0])
             lta_lon=float(split_str[1])
          
            #something wrong with the condition
             if(haversine_distance(google_lat,google_lon,lta_lat,lta_lon)<20) and lta_carpark['CarParkID'] not in results_list:
                print(3333333)
                results_list.append({'google_lat':google_lat,'carparkid':lta_carpark['CarParkID'],'google_lon':google_lon,'carpark_name':carpark_name,'lotsavailable':lta_carpark['AvailableLots']})

    print(results_list)
    for result in results_list:
       ura_response=invoke_http(urawrapper_url+result['carparkid'],method='GET')
       result['rates']=ura_response
    print(results_list)
    return results_list

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5002,debug=True)
