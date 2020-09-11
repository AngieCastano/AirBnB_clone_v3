#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities/',
                 methods=['GET'], strict_slashes=False)
def cities_state(state_id=None):
    """ Return all citis of a state"""
    state = storage.get("State",  state_id)
    if state is None:
        abort(404)
    cities_list = state.cities
    cities_dict = [city.to_dict()for city in cities_list]
    return jsonify(cities_dict)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def ret_city_id(city_id=None):
    """Retrieves a City object"""
    city = storage.get('City',  city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>/',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):

    new_dict = storage.get('City', city_id)
    if new_dict is None:
        abort(404)
    storage.delete(new_dict)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/',
                 methods=['POST'], strict_slashes=False)
def create_city_with_state_id(state_id=None):
    """creates a city"""
    state = storage.get("State",  state_id)
    if state is None:
        abort(404)
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    if 'name' not in reqst:
        return 'Missing name', 400
    new_city = City(**reqst)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>/', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """update city"""
    new_dict = storage.get('City', city_id)
    if new_dict is None:
        abort(404)
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'created_at', 'updated_at', 'state_id'):
        reqst.pop(key, None)
    for key, value in reqst.items():
        setattr(new_dict, key, value)
    new_dict.save()
    return jsonify(new_dict.to_dict()), 200
