#!/usr/bin/python3
"""index from views"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_states(state_id=None):
    """get method states"""
    list_city = []
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for value in state.cities:
        list_city.append(value.to_dict())
    return jsonify(list_city)


@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):

    cities = storage.get("City", city_id)
    if cities is not None:
        storage.delete(cities)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in json_data.keys():
        return jsonify({'error': "Missing name"}), 400
    json_data['state_id'] = state_id
    city = City(**json_data)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id=None):
    p_city = storage.get("City", city_id)
    if p_city is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_city, key, value)
    storage.save()
    return jsonify(p_city.to_dict()), 200
