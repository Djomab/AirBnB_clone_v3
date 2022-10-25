#!/usr/bin/python3
"""Places amenities handers module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User
from os import getenv
STORAGE_IS_DB = (getenv('HBNB_TYPE_STORAGE') == 'db')
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_places_amenities(place_id):
    """Retrives a place's amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    output = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(output)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def delete_or_post_amenities(place_id, amenity_id):
    """Deletes or creates amenities"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        if amenity not in place.aminities:
            abort(404)
        if request.method == 'DELETE':
            place.amenities.remove(amenity)
            res_obj = (jsonify({}), 200)
        if request.method == 'POST':
            place.amenities.append(amenity)
            place.save()
            res_obj = (jsonify(amenity.to_dict()), 201)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        if request.method == 'DELETE':
            place.amenity_ids.remove(amenity.id)
            res_obj = (jsonify({}), 200)
        if request.method == 'POST':
            place.amenity_ids.append(amenity.id)
            place.save()
            res_obj = (jsonify(amenity.to_dict()), 201)
    return res_obj
