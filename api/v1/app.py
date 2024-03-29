#!/usr/bin/python3
""" app """
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """removes current sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    # python3 -m api.v1.app
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
