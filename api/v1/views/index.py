#!/usr/bin/python3
"""
index
"""

from api.v1.views import *
from flask import jsonify

@app_views.route('/status', method = ['GET'])
def status():
    """return HTTP response"""
    return  jsonify({"status": "OK"})
