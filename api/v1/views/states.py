#!/usr/bin/python3
"""
Create a new view for State objects that handles
all default RESTFul API actions
index from views
"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_states(state_id=None):
    """get method states"""

    list_states = []
    if state_id is None:
        for val_state in storage.all("State").values():
            list_states.append(val_state.to_dict())
        return jsonify(list_states), 200
    else:
        state = storage.get("State", state_id)
        if state is not None:
            return jsonify(state.to_dict())
        else:
            abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id=None):
    """delete method states"""

    state = storage.get("State", state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_states():
    """post method states"""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Not a JSON'}), 400
    if "name" not in json_data.keys():
        return jsonify({"Missing name"}), 400
    state = State(**json_data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_states(state_id=None):
    p_state = storage.get("State", state_id)
    if p_state is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_state, key, value)
    storage.save()
    return jsonify(p_state.to_dict()), 200
