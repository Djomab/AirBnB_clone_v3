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
        if request.method == 'DELETE':
            if amenity not in place.aminities:
                abort(404)
            place.amenities.remove(amenity)
            res_obj = (jsonify({}), 200)
        if request.method == 'POST':
            if amenity not in place.amenities:
                place.amenities.append(amenity)
                place.save()
                status_code = 201
            else:
                status_code = 200
            res_obj = (jsonify(amenity.to_dict()), status_code)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        if request.method == 'DELETE':
            if amenity not in place.aminity_ids:
                abort(404)
            place.amenity_ids.remove(amenity.id)
            res_obj = (jsonify({}), 200)
        if request.method == 'POST':
            if amenity.id not in place.amenity_ids:
                place.amenity_ids.append(amenity.id)
                place.save()
                status_code = 201
            else:
                status_code = 200
            res_obj = (jsonify(amenity.to_dict()), status_code)
    return res_obj
