#!/usr/bin/python3
"""__init__ from views"""
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
