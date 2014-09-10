"""
This module encapsulates a function for the creation of, and attaching of endpoints to, an application.
"""


from flask import Flask
import logging
import os

from .data import db
from .backend import api_blueprint, UltraJSONEncoder
from .frontend import frontend_blueprint
from .config import setup_log

def create_app(config_from_object=None, config_from_env=None):
  """A factory function to produce a Flask application instance

  This will create the one true application, in a flexible and extensible way.  The app is being created via a factory function in order to facilitate custom or manual configurations.  In this fashion, the app could be configured automatically by the Flask-Script file ``manage.py`` during development using an environment variable on a local workstation prescribing a ``DevelopmentConfig``, while on the production machine, it will resolve to a ``ProductionConfig``, or manually specified in the tests directory during set-up as ``TestingConfig`` as defined in the :mod:`foodtruck.config` module.

  The app will register the :mod:`foodtruck.backend` module at the endpoint specified by``API_ENDPOINT`` using a Flask blueprint in a self-contained backend sub-package, demonstrating the flexibility Flask provides.

  Args:
    config_from_object (str, optional): A string representing the name of an object to import
    config_from_env  (str, optional): A string representing the name of the environment variable to pull the name of the object to import

  Note:
    While both arguments are optional, at least **one** is mandatory.  Otherwise, where will we get our configs??
  """
  setup_log()
  log = logging.getLogger(__name__)

  app = Flask(__name__)

  if config_from_env:
    app.config.from_object(os.environ[config_from_env])
  # While the ENVIRONMENT configures first, the config object can be used to merge and overwrite settings, providing additional flexibility
  if config_from_object:
    app.config.from_object(config_from_object)

  # We'll be mounting our API right on this endpoint here:
  app.register_blueprint(api_blueprint, url_prefix='/'+app.config['API_ENDPOINT'])
  app.register_blueprint(frontend_blueprint)

  # Register our JSON encoder too
  app.json_encoder = UltraJSONEncoder

  db.init_app(app)

  return app
