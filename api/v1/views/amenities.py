#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/',
                 methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Return all amenities"""
    amenity_dict = [amenity.to_dict() for amenity in storage.
                    all("Amenity").values()]
    return jsonify(amenity_dict)


@app_views.route('/amenities/<amenity_id>/',
                 methods=['GET'], strict_slashes=False)
def ret_amenity_id(amenity_id=None):
    """Retrieves a Amenity object"""
    amenity = storage.get('Amenity',  amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>/',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):

    new_dict = storage.get('Amenity', amenity_id)
    if new_dict is None:
        abort(404)
    storage.delete(new_dict)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """creates an amenity"""
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    if 'name' not in reqst:
        return 'Missing name', 400
    new_amenity = Amenity(**reqst)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>/',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id=None):
    """update amenity"""
    new_dict = storage.get('Amenity', amenity_id)
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
