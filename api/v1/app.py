#!/usr/bin/python3
"""
Return HTTP response
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage():
    """close storage every time something is excecuted"""
    storage.close()

if __name__ == "__main__":
    host_flask = getenv("HBNB_API_HOST") or '0.0.0.0'
    port_flask = getenv("HBNB_API_PORT") or '5000'
    app.run(host=host_flask, port=port_flask, threaded=True)
