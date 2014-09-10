"""
This module contains all of the routes for the backend API.
"""
from decimal import Decimal
from flask import Blueprint, request, jsonify

from foodtruck.data import db
from .models import Foodtruck
from .errors import InvalidUsage, ResourceNotFound, MissingParameter

api = Blueprint('api', __name__)

@api.route('/foodtrucks', methods=['GET'])
def list():
  """
  A simple view, returning all of the known trucks via a GET method.

  Returns:
    ``JSONObject('foodtrucks', JSONArray(Foodtruck))``
  """
  trucks = Foodtruck.query.all()
  return jsonify(foodtrucks=[truck.to_dict() for truck in trucks])

@api.route('/foodtrucks/nearby', methods=['GET'])
def nearby():
  """
  The real meat of the application: provides a list of trucks sorted by distance from a point provided as a query parameter.  This API call also supports pagination.  Pagination is especially useful when dealing with larger data sets.

  Args:
    lat[itude] (double precision, signed, float, SRID=4326): The latitude of the center Geo point.
    lon[gitude] (double precision, signed, float, SRID=4326): The longitude of the center Geo point.
    per_page | limit (int, optional): How many results to return per request. Must be greater than zero.  ``per_page`` takes precedence over ``limit`` if both are specified.  Don't do that.
    page_num (int, optional, default=1): Which page (effectively, results are offset to (per_page * page_num)) to return.  This value is only used if per_page is specified. That makes sense.

  Returns:
    ``JSONObject('foodtrucks', JSONArray(Foodtruck))`` sorted by distance, ascending.
  """

  # Pull up all the query parameters to see what we're dealing with
  # We'll be flexible with the naming, typing all those letters is hard
  # Generate some API errors if our conditions are not satisfied.
  lat = request.args.get('latitude') or request.args.get('lat')
  if lat:
    lat = Decimal(lat)
  else:
    raise MissingParameter('latitude')

  lon = request.args.get('longitude') or request.args.get('lon')
  if lon:
    lon = Decimal(lon)
  else:
    raise MissingParameter('longitude')


  limit = request.args.get('limit')
  if limit: limit = int(limit)

  per_page = request.args.get('per_page') or limit
  if per_page:
    per_page = int(per_page)
  # If limit is not specified (None), and per_page is not specified (None) we won't paginate a thing.

  page_num = int(request.args.get('page_num') or 1)
  # Offset math requires this value to be zero-indexed. But humans don't really do that.

  trucks_query = Foodtruck.query
  trucks_query = trucks_query.order_by(Foodtruck.location.distance_box('POINT({lat} {lon})'.format(lat=lat, lon=lon)))
  # The Truck query is set up before pagination is applied because A) we can (A.K.A. we have to according to geoalchemy2, it makes sense) and B) we don't know if we should paginate.
  # Also, to note, this logic could be abstracted to provide a Model level pagination feature, cleaning this area up and reducing reproduction of code. Time constraints!
  if per_page:
    # Oh, ok, we're paginating
    trucks_query = trucks_query.limit(per_page)
    trucks_query = trucks_query.offset(per_page * (page_num-1))

  # Send it home
  return jsonify(foodtrucks=[truck.to_dict() for truck in trucks_query])


@api.route('/foodtrucks/<int:foodtruck_id>', methods=['GET'])
def show(foodtruck_id):
  """A standard single resource endpoint. Provide an ID, get a truck.

  In order to reduce bandwidth, we could reduce the amount of information we send during the ``list`` or ``nearby`` methods (in extreme cases, just IDs could do), and let the client use this endpoint to resolve more detailed information about the Truck.  In reality, the information we have right now is not exorbitant and this is provided as a courtesy.

  Args:
    foodtruck_id (int): The ID of the Truck resource as provided in any other Truck resource endpoint.
  """
  truck = Foodtruck.query.get(foodtruck_id)
  if not truck:
    raise ResourceNotFound('Foodtruck with {{id:{}}} does not exist.'.format(foodtruck_id))
  return jsonify(truck.to_dict())

@api.errorhandler(ResourceNotFound)
@api.errorhandler(MissingParameter)
@api.errorhandler(InvalidUsage)
def handle_error(error):
  """The API error handler processes each error the API can throw and responds accordingly, automatically setting the status_code provided by the error class.  This method is not invoked directly, but a hook into Flask's error handling.  Nothing to do here.
  """
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response
