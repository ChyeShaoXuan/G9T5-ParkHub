from flask import Blueprint, render_template, request, jsonify, redirect, url_for  
#request (for query parameters)

views = Blueprint(__name__, "views")

name = "Chye Shao Xuan"
location = "Sengkang"

@views.route("/")
def home():
    return render_template("homepage.html", username = name, location = location)

# #access parameters in url
# @views.route("/profile/<username>")
# def profile(username):
#     return render_template("homepage.html", name=username)

@views.route("/locate-CP")
def locate_CP():
    return render_template("locateCP.html", username = name, location = location)

@views.route("/map")
def map():
    api_key = 'AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY'
    return render_template("map.html", gm_api_key = api_key)

@views.route("/get-location")
def get_location():
    api_key = 'AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY'
    return render_template("getlocation.html", gm_api_key = api_key)


#------------------------------------------------------------------------------------------

#query parameters (profile?name=bill)
@views.route("/profile")
def profile():
    # args = request.args
    # name1 = args.get('name') #name variable in profile.html

    # Access query parameters using request.args
    name_param = request.args.get('name')  # Get the value of the 'name' parameter
    location_param = request.args.get('location')  # Get the value of the 'location' parameter

    # Use the default values if the parameters are not provided
    name_to_display = name_param if name_param else name
    location_to_display = location_param if location_param else location

    return render_template("profile.html", name=name_to_display, location=location_to_display) 


#convert to json dictionary and view it
@views.route("/json")
def get_json():
    return jsonify(
        {'name': 'tim', 
         "coolness": 10}
        )

#getting json data
@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

#redirecting
# @views.route("/go-to-home")
# def go_to_home():
#     return redirect(url_for("views.get_json"))