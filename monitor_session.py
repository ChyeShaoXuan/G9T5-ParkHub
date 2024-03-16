from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

# APScheduler runs in background to trigger jobs at regular intervals to monitor sessions and send notifications
from subprocess import call

import time
import os
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
# scheduler.configure(timezone=pytz.timezone('Asia/Singapore'))
scheduler.add_job(func='processMonitorSession',interval='target', seconds=300)
scheduler.start()
# print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

app = Flask(__name__)

import logging
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

CORS(app)

user_URL = "http://localhost:5000/user"
session_URL = "http://localhost:5001/session/trigger"
# shipping_record_URL = "http://localhost:5002/shipping_record"
# activity_log_URL = "http://localhost:5003/activity_log"
# error_URL = "http://localhost:5004/error"

exchangename = "notification_topic" # exchange name
exchangetype="topic"

connection = amqp_connection.create_connection() 
channel = connection.channel()

if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status


@app.route("/monitor_session")
def monitor_session():
    # Simple check of input format and data of the request are JSON
    try:
            # do the actual work
            # 1. Send order info {cart items}
        result = processMonitorSession()
        return jsonify(result), result["code"]

    except Exception as e:
            # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "monitor_session.py internal error: " + ex_str
        }), 500

    # if reached here, not a JSON request.
    
def processMonitorSession():
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    # print('\n-----Invoking user microservice-----')
    # user_result = invoke_http(user_URL, method='GET')
    # print('user_result:', user_result)

    # 4. Record new order
    # record the activity log anyway
    print('\n\n-----Invoking session_record microservice-----')
    sessions_results = invoke_http(session_URL)
    print("Sessions Results:", json.dumps(sessions_results, indent=4))  # This will print the structure of the sessions_results
    logging.info("Checking for sessions that are about to end...")
    print("\nExpiring Sessions retrieved\n", sessions_results)
    list_of_ending_session = [endingsession for endingsession in sessions_results['data']]

    for info in list_of_ending_session:
        print(info)
        userID = info['userID']
        sessionID = info['sessionID']
        endtime = info['endtime']
        print("hiiiiiiii")
        user_info = invoke_http(user_URL+'/'+str(userID))
        print(type(user_info))
        # user_info = json.loads(user_info)
        print(user_info)
        phoneNo = user_info['data']['phoneNo']
        print('\n\n-----Publishing the session message with routing_key=notification.send-----')        

        message = {
            'sessionID':sessionID, 
            'phoneNo':phoneNo, 
            'endtime':endtime
            } # need sessionID, phoneNo, endtime
        messagejson = json.dumps(message)
        channel.basic_publish(exchange=exchangename, routing_key="notification.send", 
            body=messagejson, properties=pika.BasicProperties(delivery_mode = 2))
        
    
    # 4. Record new order
    # record the activity log anyway
    #print('\n\n-----Invoking activity_log microservice-----')
    
    print("\nOrder published to RabbitMQ Exchange.\n")

    return {
        "code": 201,
        "data": {
            # "user_result": user_result,
            "sessions_results": sessions_results
        }
    }

@app.route('/scheduled-jobs')
def scheduled_jobs():
    jobs = scheduler.get_jobs()
    jobs_info = [{"id": job.id, "next_run": job.next_run_time} for job in jobs]
    return jsonify(jobs_info)

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
