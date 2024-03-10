from pyproj import Proj, transform

def convert_svy21_to_wgs84(easting, northing):
    # Define the SVY21 and WGS84 projections
    svy21 = Proj(init='epsg:3414')  # SVY21 projection
    wgs84 = Proj(init='epsg:4326')  # WGS84 projection

    # Convert SVY21 coordinates to WGS84
    longitude, latitude = transform(svy21, wgs84, easting, northing)

    return latitude, longitude

# Example coordinates in SVY21 format (replace with your own)
easting = 30873.0177
northing = 32533.6617

# Convert SVY21 to WGS84
latitude, longitude = convert_svy21_to_wgs84(easting, northing)

print(f"Latitude: {latitude}, Longitude: {longitude}")


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

print(f"Easting: {easting}, Northing: {northing}")