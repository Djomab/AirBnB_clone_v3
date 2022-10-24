#!/usr/bin/python3
"""Places reviews handers module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_or_post_places(place_id):
    """Retrieves or create reviews"""
    output = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        for review in place.places:
            print(review)
            output.append(review.to_dict())
        return jsonify(output)
    if request.method == 'POST':
        if not request.is_json:
            abort(400, description="Not a JSON")
        data = request.get_json()
        if data.get('user_id') is None:
            abort(400, description='Missing user_id')
        if data.get('text') is None:
            abort(400, description='Missing text')
        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_delete_put_city(review_id):
    """Retrieves, deletes or updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, value)
        review.save()
        return (make_response(jsonify(review.to_dict())), 200)
