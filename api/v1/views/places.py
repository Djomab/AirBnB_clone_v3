#!/usr/bin/python3
"""Handles all default RESTFul API actions for Place objects"""


from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from os import getenv
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places/',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        return abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort(400, "Missing name")

    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    instance = Place(**data)
    instance.city_id = city_id
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Handles the route for searching a place"""
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    places = []
    state_ids = data.get('states')
    city_ids = data.get('cities')
    amenity_ids = data.get('amenities')
    if (not state_ids and not city_ids and not amenity_ids):
        places = storage.all(Place).values()
    if amenity_ids:
        for place in storage.all(Place).values():
            place_amenities_ids = [amenity.id for amenity in place.amenities]
            if are_equal(amenity_ids, place_amenities_ids):
                places.append(place)
    if city_ids:
        cities = [storage.get(City, city_id) for city_id in city_ids]
        for city in cities:
            [places.append(p) for p in city.places if city and p not in places]
    if state_ids:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    [places.append(p) for p in city.places if p not in places]
    output = [place.to_dict() for place in places]
    return make_response(jsonify(output))


def are_equal(list1, list2):
    """Compare two lists"""
    list_tmp = list1.copy()
    for item in list2:
        if item in list_tmp:
            list_tmp.remove(item)
    return (len(list_tmp) == 0)
