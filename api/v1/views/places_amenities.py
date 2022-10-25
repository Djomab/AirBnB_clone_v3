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
    place_obj = storage.get('Place', place_id)
    amenity_obj = storage.get('Amenity', amenity_id)
    if place_obj is None:
        abort(404, 'Not found')
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if (amenity_obj not in place_obj.amenities and
                amenity_obj.id not in place_obj.amenities):
            abort(404, 'Not found')
        if STORAGE_TYPE == 'db':
            place_obj.amenities.remove(amenity_obj)
        else:
            place_obj.amenity_ids.pop(amenity_obj.id, None)
        place_obj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (amenity_obj in place_obj.amenities or
                amenity_obj.id in place_obj.amenities):
            return jsonify(amenity_obj.to_json()), 200
        if STORAGE_TYPE == 'db':
            place_obj.amenities.append(amenity_obj)
        else:
            place_obj.amenities = amenity_obj
        return jsonify(amenity_obj.to_json()), 201
