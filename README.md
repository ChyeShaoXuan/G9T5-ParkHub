# G9T5-ParkHub
An app that lets users find and compare parking options based on real-time lot availability, rates and location, view nearby amenities, and notifies users nearing their end time.


# Scenario 1
To run the search:
1. Import ura_rates.sql into phpmyadmin.
2. Run the ura_rates.py script in terminal. Change the token if you are inserting the database as it needs to be retrieved daily
   - call url https://www.ura.gov.sg/uraDataService/insertNewToken.action, with
     AccessKey Header in Postman : e61ff773-ba6b-4e89-aeda-759e0bc55604.
    - result of api call will be token.
    - Enter api_url = 'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details'
access_key = '04560d6a-1e36-4e14-80bf-85616c85510f'
token = ******your token here
user_agent = 'PostmanRuntime/7.36.3'
cookie = '__nxquid=HOIH8mjcscbjbYyu/M4fhlrXabqh+A==0014'

4. Run views.py
5. Run googlewrapper.py
6. Run ltawrapperlots.py
7. Run urawrapper_rates.py
8. Run searchinfo.py
