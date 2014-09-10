"""Foodtruck backend defines the Blueprint the application will use, the model Foodtruck, and the potential errors that can be thrown
"""
from .views import api as api_blueprint
from .models import Foodtruck
from .errors import InvalidUsage, ResourceNotFound, MissingParameter
from .ujson_encoder import UltraJSONEncoder
