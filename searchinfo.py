from flask import Flask

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
@app.route('/search_results')
def processreturntopcarparks():
    #invoke googlewrapper function and return results
    google_response=invoke_http(googlewrapper_url,method='GET')
    google_result=google_response['results']
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
        google_lon=google_car_park['geometry']['location']['lng']   # not sure why the google_result only returns the 1st 2 sets of lat long
        # print(google_lat,google_lon)
        for lta_carpark in lta_carparks:    
        
          lta_coordinates=lta_carpark['Location']
          
          split_str=lta_coordinates.split()
          
          if len(split_str)>0:
             lta_lat=float(split_str[0])
             lta_lon=float(split_str[1])
          
             if(haversine_distance(google_lat,google_lon,lta_lat,lta_lon)<20) and lta_carpark['CarParkID'] not in results_list:
       
                results_list.append({'carparkid':lta_carpark['CarParkID'],'lotsavailable':lta_carpark['AvailableLots']})

    for result in results_list:
       ura_response=invoke_http(urawrapper_url+result['carparkid'],method='GET')
       result['rates']=ura_response
    print(results_list)
processreturntopcarparks()


    





if __name__=='__main__':
    app.run(host='0.0.0.0', port=5002,debug=False)