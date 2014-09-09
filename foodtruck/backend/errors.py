"""
.. module:: errors
    :synopsis:  This module contains all of the errors the :mod:`foodtruck.backend` sub-module will use.

"""

class InvalidUsage(Exception):
  """Base class for the internally raised API errors used throughout :mod:`foodtruck.backend`

  Args:
    message (str): An informative message that will be available in the response
    status_code (int, optional): An HTTP response code
    payload (dict, optional): A payload dictionary for any custom attributes to add to the error response.  Attributes in payload will overwrite any default attributes, including a sub-class's.
  """
  status_code = 400
  error = True
  """ To let a client know they really did do something wrong"""
  payload = {}
  message = 'You did it wrong'
  """ Hopefully the subclasses will be more informative...(they will)"""

  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.message = message
    self.status_code = status_code or self.status_code
    self.payload = payload or self.payload

  def to_json(self):
    """A serialization function to standardize the responses of subclasses

    This method is part of an artificial interface, allowing to rendering of it through Flask's ``jsonify``
    """
    rv = {
      'message': self.message,
      'status_code': self.status_code,
      'error': self.error,
    }
    rv = dict(rv.items() + self.payload.items())
    return rv

class ResourceNotFound(InvalidUsage):
  """An implementation of :class:`InvalidUsage` acting as a 404 response

  This class overrides the ``status_code`` with a value of 404, and a snarky message that could be replaced.
  """
  status_code = 404
  message = 'The resource you are looking for is not here'

class MissingParameter(InvalidUsage):
  """An implementation of :class:`InvalidUsage` informing our client that they have not included the necessaries

  Args:
    parameter (str, optional): The name of the parameter that was forgotten.  If just this parameter is passed, then the default message will be formatted to take care of everything.  Easy peasy.
    message (str, optional): A message that will replace the default_message.  If this parameter is passed along with the ``parameter`` parameter (ugh) then this class will attempt to format that message with the parameter name passed as a convenience.
  """
  status_code = 400
  default_message = 'Missing some parameters, apparently'
  """A useless message by itself"""

  def __init__(self, parameter=None, message=None,):
    if message:
      self.default_message = message
      if parameter:
        self.default_message.format(parameter)
    elif parameter:
      self.default_message = 'This endpoint requires the parameter: "{}"'.format(parameter)

    self.message = self.default_message

