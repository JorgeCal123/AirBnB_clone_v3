#!/usr/bin/python3
"""index from views"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places_city(city_id=None):
    """get method states"""
    list_places = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for value in city.places:
        list_places.append(value.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id=None):
    place = storage.get("Place", place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):

    place = storage.get("Place", place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in json_data.keys():
        return jsonify({'error': "Missing user_id"}), 400
    if "name" not in json_data.keys():
        return jsonify({'error': "Missing name"}), 400
    user = storage.get("User", json_data['user_id'])
    if user is None:
        abort(404)
    json_data['city_id'] = city_id
    place = Place(**json_data)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id=None):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
