#!/usr/bin/python3
""" palce module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.place import Place


@app_views.route('/cities/<city_id>/places/', methods=['GET'],
                 strict_slashes=False)
def get_places_city(city_id=None):
    """ Retrieves the list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_dict = [place.to_dict() for place in city.places]
    return jsonify(places_dict)


@app_views.route('/places/<place_id>/', methods=['GET'],
                 strict_slashes=False)
def ret_palce_id(place_id=None):
    """Retrieves a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Delete place / id"""
    new_dict = storage.get('Place', place_id)
    if new_dict is None:
        abort(404)
    storage.delete(new_dict)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def create_place_with_city_id(city_id=None):
    """creates a place"""
    if request.method == 'POST':
        city = storage.get("City", city_id)
        if city is None:
            abort(404)
        reqst = request.get_json()
        if reqst is None:
            return 'Not a JSON', 400
        if 'user_id' not in reqst:
            return 'Missing user_id', 400
        user = storage.get("User", reqst.get("user_id"))
        if user is None:
            abort(404)
        if 'name' not in reqst:
            return 'Missing name', 400
        reqst['city_id'] = city_id
        new_place = Place(**reqst)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>/', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """update place"""
    new_dict = storage.get('Place', place_id)
    if new_dict is None:
        abort(404)
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
        reqst.pop(key, None)
    for key, value in reqst.items():
        setattr(new_dict, key, value)
    new_dict.save()
    return jsonify(new_dict.to_dict()), 200
