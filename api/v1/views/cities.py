#!/usr/bin/python3
"""City handers module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_or_post_cities(state_id):
    """Retrieves or create cities"""
    output = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        for city in state.cities:
            print(city)
            output.append(city.to_dict())
        return jsonify(output)
    if request.method == 'POST':
        if not request.is_json:
            abort(400, description="Not a JSON")
        data = request.get_json()
        if data.get('name') is None:
            abort(400, description='Missing name')
        data['state_id'] = state_id
        city = City(**data)
        city.save()
        return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_delete_put_city(city_id):
    """Retrieves, deletes or updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            setattr(city, key, value)
        city.save()
        return (make_response(jsonify(city.to_dict())), 200)
