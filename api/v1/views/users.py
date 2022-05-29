#!/usr/bin/python3
"""
Create a new view for User objects that handles
all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.amenities import Amenity


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """get method users"""

    list_user = []
    if user_id is None:
        for val_user in storage.all("User").values():
            list_user.append(val_user.to_dict())
        return jsonify(list_user), 200
    else:
        user = storage.get("User", user_id)
        if user is not None:
            return jsonify(user.to_dict())
        else:
            abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id=None):
    """delete method user"""

    user = storage.get("Amenity", amenity_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_users():
    """post method users"""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in json_data.keys():
        return jsonify({'error': "Missing name"}), 400
    user = User(**json_data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_users(user_id=None):
    """Methos PUT in user"""
    p_user = storage.get("User", user_id)
    if p_user is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_user, key, value)
    storage.save()
    return jsonify(p_user.to_dict()), 200
