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

@app_views.route('/places_search/', methods=['POST'],
                 strict_slashes=False)
def retreive_places_depending_on_a_foreign_id():
    """Retreive a place depending on State or City or Amenity id"""
    reqst = request.get_json()
    if reqst is None:
        return 'Not a JSON', 400
    print("LENGHT OF REQUEST DICTINARY", len(reqst))
    if len(reqst) == 0:
        new_dict = [place.to_dict() for place in storage.all('Place').values()]
        return jsonify(new_dict)
    reqst = request.get_json()
    amenities = reqst.get("amenities")
    if amenities:
        list_of_places_with_same_amenity = []
        list_of_dictionaries_places_with_same_amenity = []
        if len(amenities) == 1:
            places_with_same_amenity =  storage.places_amenities(amenities[0])    
            for place_ in places_with_same_amenity:
                place_id = place_[0]
                place = storage.get('Place', place_id)
                if place is None:
                    abort(404)
                list_of_dictionaries_places_with_same_amenity.append(place.to_dict())
        else:
            
            set_of_unique_places_id = [item[0] for item in storage.places_amenities(amenities[0])]
            for amenity in amenities:
                places_with_same_amenity =  storage.places_amenities(amenity)
                list_of_places_with_same_amenity = [item[0] for item in storage.places_amenities(amenity)]
                for item1 in set_of_unique_places_id:
                        if item1 not in list_of_places_with_same_amenity:
                            set_of_unique_places_id.remove(item1)
            for place_id in set_of_unique_places_id:
                place = storage.get('Place', place_id)
                if place:
                    list_of_dictionaries_places_with_same_amenity.append(place.to_dict())
        return jsonify(list_of_dictionaries_places_with_same_amenity)
    states = reqst.get("states")
    cities = reqst.get("cities")
    list_of_cities_id = []
    if states and cities:
        state = storage.get('State', states[0])
        city_ids_of_first_state = [city.id for city in state.cities]
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                list_of_cities_id = [city.id for city in state.cities]
            for item1 in list_of_cities_id:
                if item1 not in city_ids_of_first_state:
                    city_ids_of_first_state.append(item1)
        last_city_ids = city_ids_of_first_state
    elif states:
        last_city_ids = []
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                list_of_cities_id = [city.id for city in state.cities]
                last_city_ids += list_of_cities_id
    elif cities:
        last_city_ids = cities
    list_of_dictionaries_places_of_cities = []
    for city_id in last_city_ids:
        city = storage.get('City', city_id)
        places_of_cities = [place.id for place in city.places]
        for place_id in places_of_cities:
            place = storage.get('Place', place_id)
            list_of_dictionaries_places_of_cities.append(place.to_dict())
    return jsonify(list_of_dictionaries_places_of_cities)