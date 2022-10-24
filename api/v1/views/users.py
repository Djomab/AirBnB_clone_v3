#!/usr/bin/python3
"""Users handers module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_or_post_users():
    """Retrieves or create users"""
    if request.method == 'GET':
        users = storage.all('User').values()
        output = []
        for user in users:
            output.append(user.to_dict())
        return jsonify(output)
    if request.method == 'POST':
        if not request.is_json:
            abort(400, description='Not a JSON')
        data = request.get_json()
        if data.get('email') is None:
            abort(400, description='Missing email')
        if data.get('password') is None:
            abort(400, description='Missing password')
        user = User(**data)
        user.save()
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_delete_put_user(user_id):
    """Retrieves, deletes or updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(User, user_id)
        storage.save()
        return make_response(jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.get_items():
            setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
