#!/usr/bin/python3
"""
"""

from flask import Blueprint


app_views = Blueprint('simple_page', __name__,template_folder='templates')


@app_views.route('/api/v1')
def import_everything():
    """imports everything"""
    from api.v1.views.index import *
