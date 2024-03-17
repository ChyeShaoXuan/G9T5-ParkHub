from pyproj import Proj, transform

def convert_wgs84_to_svy21(latitude, longitude):
    # Define the WGS84 and SVY21 projections
    wgs84 = Proj(init='epsg:4326')  # WGS84 projection
    svy21 = Proj(init='epsg:3414')  # SVY21 projection

    # Convert WGS84 coordinates to SVY21
    easting, northing = transform(wgs84, svy21, longitude, latitude)

    return easting, northing

# Example coordinates in WGS84 format (replace with your own)
latitude = 1.3104972637937204 
longitude = 103.85913404261208

# Convert WGS84 to SVY21
easting, northing = convert_wgs84_to_svy21(latitude, longitude)

print(easting,northing)

#convert from the google coordinates to easting northing