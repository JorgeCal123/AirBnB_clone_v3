#!/usr/bin/python3
"""index from views"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews_place(place_id=None):
    """get method Place"""
    list_reviews = []
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for value in place.reviews:
        list_reviews.append(value.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id=None):
    """Method GET for review"""
    review = storage.get("Review", review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Method DELETE for review"""
    review = storage.get("Review", review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """Method POST review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in json_data.keys():
        return jsonify({'error': "Missing user_id"}), 400
    user = storage.get("User", json_data['user_id'])
    if user is None:
        abort(404)
    if "text" not in json_data.keys():
        return jsonify({'error': "Missing text"}), 400
    json_data['place_id'] = place_id
    review = Review(**json_data)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id=None):
    """Method PUT for review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
