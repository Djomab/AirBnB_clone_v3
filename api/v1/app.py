#!/usr/bin/python3
"""App module"""

from models import storage
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from os import environ

host = environ.get('HBNB_API_HOST', '0.0.0.0')
port = environ.get('HBNB_API_PORT', 5000)
app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """Teardown database"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Not found route handler"""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
