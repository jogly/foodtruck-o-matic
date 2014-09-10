import ujson
from flask.json import JSONEncoder

class UltraJSONEncoder(JSONEncoder):
  """
  This is a proxy class for the ultraJSON module, so that we can replace Flask's built-in JSONEncoder.  This will let us have access to high-precision float fields, seamless Datetime integration, and all faster than before.
  """
  def default(self, obj):
    """
    Override JSONEncoder's method.
    Args:
      obj (object): Any ol py object that ultraJSON can encode
    Returns:
      ``str``: The JSON string, of course.
    """
    return ujson.dumps(obj, double_precision=14)
