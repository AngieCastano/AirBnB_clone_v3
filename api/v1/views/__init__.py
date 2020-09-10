#!/usr/bin/python3
""" init file of module views """
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *