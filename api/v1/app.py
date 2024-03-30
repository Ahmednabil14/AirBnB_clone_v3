#!/usr/bin/python3
""" app """
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """removes current sqlalchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handeling not found page (error 404)"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    # python3 -m api.v1.app
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', 5000)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
