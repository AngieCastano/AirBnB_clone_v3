#!/usr/bin/python3
""" user module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def all_users():
    """ Return all Users"""
    user_dict = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(user_dict)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def ret_user_id(user_id=None):
    """Retrieves a User object"""
    user = storage.get('User',  user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):

    new_dict = storage.get('User', user_id)
    if new_dict is None:
        abort(404)
    storage.delete(new_dict)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_new_user():
    """creates an amenity"""
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    if 'email' not in reqst:
        return 'Missing email', 400
    if 'password' not in reqst:
        return 'Missing password', 400
    new_user = User(**reqst)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """update user"""
    new_dict = storage.get('User', user_id)
    if new_dict is None:
        abort(404)
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'created_at', 'updated_at', 'email'):
        reqst.pop(key, None)
    for key, value in reqst.items():
        setattr(new_dict, key, value)
    storage.save()
    return jsonify(new_dict.to_dict()), 200
