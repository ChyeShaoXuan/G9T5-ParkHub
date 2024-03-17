from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root@localhost:3306/session"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Session(db.Model):
    __tablename__ = 'session'

    sessionID = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.DateTime, nullable=False)
    endtime = db.Column(db.DateTime, nullable=False)
    ppCode = db.Column(db.String(5))
    # foreign key to carpark locator?
    notifAllowed = db.Column(db.Boolean, nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    
    

    def __init__(self, starttime, endtime, ppCode, userID, notifAllowed):
        # self.sessionID = sessionID
        self.starttime = starttime
        self.endtime = endtime
        self.ppCode = ppCode
        self.userID = userID
        self.notifAllowed = notifAllowed


    def json(self):
        return {"sessionID": self.sessionID, "starttime": self.starttime, "endtime": self.endtime, "ppCode": self.ppCode, "userID": self.userID, "notifAllowed": self.notifAllowed}

# get all
@app.route("/session")
def get_all():
    sessionrecord = db.session.scalars(db.select(Session)).all()


    if len(sessionrecord):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "sessions": [session.json() for session in sessionrecord]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no session records."
        }
    ), 404

# find specific session
@app.route("/session/<string:sessionID>")
def find_by_sessionID(sessionID):
    session = db.session.scalars(
    	db.select(Session).filter_by(sessionID=sessionID).
    	limit(1)
).first()


    if session:
        return jsonify(
            {
                "code": 200,
                "data": session.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Session record not found."
        }
    ), 404

# update session endtime
@app.route("/session/<string:sessionID>", methods=['PUT'])
def update_session(sessionID):
    try:
        session = db.session.scalars(
        db.select(Session).filter_by(sessionID=sessionID).
        limit(1)).first()
        if not session:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "sessionID": sessionID
                    },
                    "message": "session not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['endtime']:
            session.endtime = data['endtime']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": session.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "session_id": sessionID
                },
                "message": "An error occurred while updating the session. " + str(e)
            }
        ), 500

# insert data format: "2024-03-15 05:00:31.000000"

# create new session record
@app.route("/session", methods=['POST'])
def create_session():
    # userID = request.json.get('userID')

    try:
        data = request.get_json()
    

        if data:
            session = Session(userID=data['userID'],starttime=data['starttime'],endtime=data['endtime'],ppCode=data['ppCode'],notifAllowed=data['notifAllowed'])
 
        db.session.add(session)
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": session.json()
            }
            ), 200
        
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the session. " + str(e)
            }
        ), 500

# sample input:
"""
{
    "endtime": "2024-03-15 05:00:31.000000",
    "starttime": "2024-03-13 05:00:31.000000",
    "userID": 1,
    "ppCode":15,
    "notifAllowed":0

}
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
