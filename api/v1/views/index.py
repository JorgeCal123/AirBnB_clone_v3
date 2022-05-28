#!/usr/bin/python3
"""index from views"""

from models import *
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def stats():
    dictt = {
            "amenities": storage.count(storage.classes['Amenities']),
            "cities": storage.count(storage.classes['City']),
            "places": storage.count(storage.classes['Place']),
            "revies": storage.count(storage.classes['Review']),
            "states": storage.count(storage.classes['State']),
            "users": storage.count(storage.classes['User'])
            }
    return jsonify(dictt)
