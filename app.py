from flask import Flask
from views import views
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env into the environment


app = Flask(__name__)
app.register_blueprint(views, url_prefix = "/views")
  
if __name__ == "__main__":
    app.run(debug=True, port=8001)


