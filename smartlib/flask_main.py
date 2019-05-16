# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy requests flask_wtf mysqlclient
# python3 flask_main.py
from flask import Flask
from flask_api import api, db
from flask_site import site

app = Flask(__name__)

# Update HOST and PASSWORD appropriately.
HOST = "35.197.173.114"
USER = "root"
PASSWORD = "suwat513"
DATABASE = "Assignment2"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == "__main__":
    #app.debug = True
    app.run(host = "0.0.0.0")
