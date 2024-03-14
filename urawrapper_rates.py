from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
app = Flask(__name__)
import json
CORS(app)




@app.route("/ura_rates/<string:carpark_no>")
def find_by_cp_no(carpark_no):
    connection=mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='ura_rates',
    ssl_disabled=True
)
    cursor=connection.cursor()
    query=""" 
    SELECT weekdayRate,satdayRate from ura_rates
    WHERE ppCode = %s
    LIMIT 1
""" 
    
    val=(carpark_no,)

    cursor.execute(query,val)

    # response=cursor.fetchall()
    results=[]
    for i, data in enumerate(cursor):
        results.append(data)
    
    
    formatted={}
    formatted['weekdayrate']="%0.2f" % (float(results[0][0]))
    
    formatted['weekendrate']="%0.2f" % (float(results[0][1]))
    cursor.close()
    connection.close()
    return formatted
    
# find_by_cp_no('E0027')
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5003,debug=False)
