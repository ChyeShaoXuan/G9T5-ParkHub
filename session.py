from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/user"
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
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    

    def __init__(self, sessionID, starttime, endtime, ppCode, userID):
        self.sessionID = sessionID
        self.starttime = starttime
        self.endtime = endtime
        self.ppCode = ppCode
        self.userID = userID


    def json(self):
        return {"sessionID": self.sessionID, "starttime": self.starttime, "endtime": self.endtime, "ppCode": self.ppCode, "userID": self.userID}


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

# @app.route("/book/<string:isbn13>", methods=['POST'])
# def create_book(isbn13):
#     if (db.session.scalars(
#     	db.select(Book).filter_by(isbn13=isbn13).
#     	limit(1)
# ).first()
# ):
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "Book already exists."
#             }
#         ), 400


#     data = request.get_json()
#     book = Book(isbn13, **data)


#     try:
#         db.session.add(book)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "An error occurred creating the book."
#             }
#         ), 500


#     return jsonify(
#         {
#             "code": 201,
#             "data": book.json()
#         }
#     ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)