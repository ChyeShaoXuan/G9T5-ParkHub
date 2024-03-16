from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

app = Flask(__name__)
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
    print("\nExpiring Sessions retrieved\n", sessions_results)
    list_of_ending_session = [endingsession for endingsession in sessions_results['data']]

    for info in list_of_ending_session:
        userID = info['userID']
        sessionID = info['sessionID']
        endtime = info['endtime']
        print("hiiiiiiii")
        user_info = invoke_http(user_URL+'/'+str(userID))
        print(type(user_info))
        # user_info = json.loads(user_info)
        print(user_info)
        phoneNo = user_info['data']['phoneNo']
        print('\n\n-----Publishing the (order info) message with routing_key=notification.send-----')        

        message = {
            'sessionID':sessionID, 
            'phoneNo':phoneNo, 
            'endtime':endtime
            } # need sessionID, phoneNo, endtime
        messagejson = json.dumps(message)
        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        channel.basic_publish(exchange=exchangename, routing_key="notification.send", 
            body=messagejson, properties=pika.BasicProperties(delivery_mode = 2))
        

    
    # 4. Record new order
    # record the activity log anyway
    #print('\n\n-----Invoking activity_log microservice-----')
        
    
    print("\nOrder published to RabbitMQ Exchange.\n")
        


    # - reply from the invocation is not used;
    # continue even if this invocation fails

    # Check the order result; if a failure, send it to the error microservice.
    # code = user_result["code"]
    # if code not in range(200, 300):

    #     # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as order fails-----')
    #     invoke_http(error_URL, method="POST", json=order_result)
    #     # - reply from the invocation is not used; 
    #     # continue even if this invocation fails
    #     print("Order status ({:d}) sent to the error microservice:".format(
    #         code), order_result)

    #     # 7. Return error
    #     return {
    #         "code": 500,
    #         "data": {"order_result": order_result},
    #         "message": "Order creation failure sent for error handling."
    #     }

    # 5. Send new order to shipping
    # Invoke the shipping record microservice
    # print('\n\n-----Invoking shipping_record microservice-----')
    # shipping_result = invoke_http(
    #     shipping_record_URL, method="POST", json=order_result['data'])
    # print("shipping_result:", shipping_result, '\n')

    # # Check the shipping result; 
    # # if a failure, send it to the error microservice.
    # code = shipping_result["code"]
    # if code not in range(200, 300):

    #     # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as shipping fails-----')
    #     invoke_http(error_URL, method="POST", json=shipping_result)
    #     print("Shipping status ({:d}) sent to the error microservice:".format(
    #         code), shipping_result)

    #     # 7. Return error
    #     return {
    #         "code": 400,
    #         "data": {
    #             "order_result": order_result,
    #             "shipping_result": shipping_result
    #         },
    #         "message": "Simulated shipping record error sent for error handling."
    #     }

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            # "user_result": user_result,
            "sessions_results": sessions_results
        }
    }



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
