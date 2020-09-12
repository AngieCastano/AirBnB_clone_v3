#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_s(state_id=None):
    """ Return all states or one state """
    if state_id is None:
        new_dict = [state.to_dict() for state in storage.all('State').values()]
        return jsonify(new_dict)
    else:
        new_dict = storage.get('State',  state_id)
        if new_dict is None:
            abort(404)
        return jsonify(new_dict.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """ Delete state whith id """
    new_dict = storage.get('State', state_id)
    if new_dict is None:
        abort(404)
    storage.delete(new_dict)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create state """
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    if 'name' not in reqst:
        return 'Missing name', 400
    new_state = State(**reqst)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """ update state """
    new_dict = storage.get('State', state_id)
    if new_dict is None:
        abort(404)
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'created_at', 'updated_at'):
        reqst.pop(key, None)
    for key, value in reqst.items():
        setattr(new_dict, key, value)
    new_dict.save()
    return jsonify(new_dict.to_dict()), 200
