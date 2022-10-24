#!/usr/bin/python3
"""Users handers module"""

from logging import exception
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_or_post_users():
    """Retrieves or create users"""
    output = []
    users = storage.all(User).values()
    if request.method == "GET":
        for user in users:
            output.append(user.to_dict())
        return (jsonify(output))
    if request.method == "POST":
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'email' not in request.json:
            abort(400, description="Missing email")
        if 'password' not in request.json:
            abort(400, description="Missing password")
        user = User(**data)
        user.save()
        return (jsonify(user.to_dict()), 201)


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
        storage.delete(user)
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return (make_response(jsonify(user.to_dict())), 200)
