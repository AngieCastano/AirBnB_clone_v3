#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states/', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_s(state_id=None):
    """ Return all states """
    if state_id is None:
        new_dict = [state.to_dict() for state in storage.all('State').values()]
        return jsonify(new_dict)
    else:
        new_dict = storage.get('State', state_id)
        if new_dict is None:
            abort(404)
        return jsonify(new_dict.to_dict())
