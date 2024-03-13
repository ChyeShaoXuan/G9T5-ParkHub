import requests
import pymysql.cursors
from datetime import datetime
import re

# Function to fetch data from API
    
def fetch_data_from_api(api_url, access_key, token,user_agent, cookie):
    headers = {
        'AccessKey': access_key,
        'Token': token,
        'User-Agent': user_agent,
        'Cookie': cookie,
        'Connection': "keep-alive"
    }
    response = requests.get(api_url, headers=headers,allow_redirects=True)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: HTTP status code {response.status_code}")
            return None
    except ValueError as e:
        # The response body does not contain valid JSON
        print(f"Error decoding JSON: {e}")
        return None
    
def remove_geometries(carpark):
    # Create a copy of the carpark dictionary without the 'geometries' key
    carpark_copy = {key: value for key, value in carpark.items() if key != 'geometries'}
    return carpark_copy

def preprocess_data(carpark):
    def parse_minutes(min_string):
        return int(min_string.split(' ')[0])

    def parse_rate(rate_string):
        return float(rate_string.replace('$', ''))

    def convert_time(time_string):
        return datetime.strptime(time_string, "%I.%M %p").strftime("%H:%M")

    preprocessed = {}

    preprocessed = {
        'ppCode': carpark['ppCode'],
        'ppName': carpark['ppName'],
        'weekdayMin': parse_minutes(carpark['weekdayMin']) if 'weekdayMin' in carpark and carpark['weekdayMin'] is not None else 'Default_WeekdayMin',
        'weekdayRate': parse_rate(carpark['weekdayRate']) if 'weekdayRate' in carpark and carpark['weekdayRate'] is not None else 0.0,
        'satdayMin': parse_minutes(carpark['satdayMin']) if 'satdayMin' in carpark and carpark['satdayMin'] is not None else 'Default_SatdayMin',
        'satdayRate': parse_rate(carpark['satdayRate']) if 'satdayRate' in carpark and carpark['satdayRate'] is not None else 0.0,
        'sunPHMin': parse_minutes(carpark['sunPHMin']) if 'sunPHMin' in carpark and carpark['sunPHMin'] is not None else 'Default_SunPHMin',
        'sunPHRate': parse_rate(carpark['sunPHRate']) if 'sunPHRate' in carpark and carpark['sunPHRate'] is not None else 0.0,
        'startTime': convert_time(carpark['startTime']) if 'startTime' in carpark and carpark['startTime'] is not None else 'Default_StartTime',
        'endTime': convert_time(carpark['endTime']) if 'endTime' in carpark and carpark['endTime'] is not None else 'Default_EndTime'
    }

    return preprocessed


# Function to insert data into MySQL
def insert_data_to_mysql(data, db_config):
    try:
        connection = pymysql.connect(host=db_config['host'],
                                     user=db_config['user'],
                                     password=db_config['password'],
                                     database=db_config['database'],
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `ura_rates` (`ppCode`, `ppName`, `weekdayMin`, `weekdayRate`, `satdayMin`, `satdayRate`, `sunPHMin`, `sunPHRate`, `startTime`, `endTime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                for carpark in data:
                    cursor.execute(sql, (carpark['ppCode'], carpark['ppName'], carpark['weekdayMin'], carpark['weekdayRate'], carpark['satdayMin'], carpark['satdayRate'], carpark['sunPHMin'], carpark['sunPHRate'], carpark['startTime'], carpark['endTime']))
            connection.commit()
        finally:
            connection.close()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")


# API URL
api_url = 'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details'
access_key = '04560d6a-1e36-4e14-80bf-85616c85510f'
token = '26au+nfJfdRV76Mc2w85Fd436PCerF181xd+pc6DrF8e+55u-pC4vbzvWfb@54MtBke0fbkCcPA8QRr04jzYfcK58UXF8JTerc4p'
user_agent = 'PostmanRuntime/7.36.3'
cookie = '__nxquid=HOIH8mjcscbjbYyu/M4fhlrXabqh+A==0014'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ura_rates'
}

# Main flow
raw_data = fetch_data_from_api(api_url, access_key, token, user_agent, cookie)
if raw_data and 'Result' in raw_data:
    cleaned_data = [remove_geometries(carpark) for carpark in raw_data['Result']]
    preprocessed_data = []
    for carpark in cleaned_data:
        processed = preprocess_data(carpark)
        if processed:
            preprocessed_data.append(processed)
    insert_data_to_mysql(preprocessed_data, db_config)
