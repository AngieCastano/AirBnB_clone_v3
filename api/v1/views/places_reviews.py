#!/usr/bin/python3
""" review model """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id=None):
    """ show all reviews """
    new_place = storage.get('Place', place_id)
    if new_place is None:
        abort(404)
    new_reviews = [review.to_dict() for review in new_place.reviews]
    return jsonify(new_reviews)


@app_views.route('/reviews/<review_id>/',  methods=['GET'],
                 strict_slashes=False)
def show_one_review(review_id):
    """ show one review """
    new_review = storage.get('Review', review_id)
    if new_review is None:
        abort(404)
    return jsonify(new_review.to_dict())


@app_views.route('/reviews/<review_id>/',  methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    new_review = storage.get('Review', review_id)
    if new_review is None:
        abort(404)
    storage.delete(new_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews/',  methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create a new review """
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    if 'user_id' not in reqst.keys():
        return 'Missing user_id', 400
    if 'text' not in reqst.keys():
        return 'Missing text', 400
    new_place = storage.get('Place', place_id)
    if new_place is None:
        abort(404)
    new_user = storage.get('User', reqst['user_id'])
    if new_user is None:
        abort(404)
    reviews = Review(**reqst)
    reviews.place_id = place_id
    reviews.save()
    return jsonify(reviews.to_dict()), 201


@app_views.route('/reviews/<review_id>/',  methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ update one review """
    new_review = storage.get('Review', review_id)
    if new_review is None:
        abort(404)
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'user_id', 'place_id', 'created_at', 'update_at'):
        reqst.pop(key, None)
    for key, value in reqst.items():
        setattr(new_review, key, value)
    new_review.save()
    return jsonify(new_review.to_dict()), 200
