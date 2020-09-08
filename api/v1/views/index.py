#!/usr/bin/python3
"""
index
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """return HTTP response"""
    return  jsonify({"status": "OK"})
