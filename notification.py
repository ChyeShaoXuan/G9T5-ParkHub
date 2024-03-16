#!/usr/bin/env python3
import amqp_connection
import json
import pika
import os
from twilio.rest import Client

#from os import environ
os.environ['TWILIO_ACCOUNT_SID'] = 'AC5cae419481fe61101479ed4e9e528ee4'
os.environ['TWILIO_AUTH_TOKEN'] = 'f42df443e2924a05c7ef7fa1aadb3472'

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

a_queue_name = 'notification' # queue to be subscribed by Activity_Log microservice

# Instead of hardcoding the values, we can also get them from the environ as shown below
# a_queue_name = environ.get('Activity_Log') #Activity_Log

def receiveEndingSession(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=a_queue_name, on_message_callback=callback, auto_ack=True)
        print('notification: Consuming from queue:', a_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"notification: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("notification: Program interrupted by user.") 


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nnotification: Received an ending session log by " + __file__)
    processEndingSession(json.loads(body))
    print()

def processEndingSession(endingsession):
    # userID = endingsession['userID']
    endtime = endingsession['endtime']
    phoneNo = '+65'+str(endingsession['phoneNo'])
    sessionID = endingsession['sessionID']
    message = client.messages.create(
                                from_='+13219780566',
                                body="Dear user, your parking session will be ending soon on " + endtime +". To extend your session, please follow this link",
                                to=phoneNo
                            )

    print(message.sid)
    print("notification: Recording an endingsession log:")
    print(endingsession)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("notification: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("notification: Connection established successfully")
    channel = connection.channel()
    receiveEndingSession(channel)
