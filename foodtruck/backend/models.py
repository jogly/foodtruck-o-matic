"""This module contains all of the Flask-SQLAlchemy models the backend uses.

Actually it's just the one, but if there *were* more this is where they would be.
"""

from geoalchemy2 import Geometry

from foodtruck.data import db

class Foodtruck(db.Model):
  """
  The fabled Foodtruck model.  This model simultaneously defines our table in the database, is a source of our migration logic (not the same), and is an object to use and abuse in processing requests.  Each field is derived from the SF Foodtruck data source and manipulated a little bit to fit in syntactically, except for the unique ID which is auto-incremented.  The SF Foodtruck data does not have a single unique key and this is simpler than creating a multi-field key.
  """
  id = db.Column(db.Integer, primary_key=True)
  """Generated by the database, this will be our unique resource identifier"""
  location_id = db.Column(db.Integer)
  applicant = db.Column(db.String())
  facility_type = db.Column(db.String())
  cnn = db.Column(db.Integer)
  location_description = db.Column(db.String())
  address = db.Column(db.String())
  blocklot = db.Column(db.String())
  block = db.Column(db.Integer)
  lot = db.Column(db.String())
  permit = db.Column(db.String())
  status = db.Column(db.String()) #Could be enumerated
  food_items = db.Column(db.String())
  """This is a good candidate for full-text indexing and searching"""
  x = db.Column(db.Float())
  y = db.Column(db.Float())
  latitude = db.Column(db.Numeric())
  """This field along with the longitude field generate the PostGIS GEOM Point field ``location``

  This is not automated now, though can be through a script that would process the SF datasource API and generate the ``WKTElement(GEOM_From_Text('POINT(lat long)'))`` expression
  """
  longitude = db.Column(db.Numeric())
  """This field along with the latitude field generate the PostGIS GEOM Point field ``location``

  This is not automated now, though can be through a script that would process the SF datasource API and generate the ``WKTElement(GEOM_From_Text('POINT(lat long)'))`` expression
  """
  schedule_url = db.Column(db.String())
  """We could provide this url to users interested in a particular foodtruck!"""
  noi_sent_on = db.Column(db.Date())
  approved_at = db.Column(db.DateTime())
  received_at = db.Column(db.DateTime())
  prior_permit = db.Column(db.Boolean())
  expires_on = db.Column(db.Date())
  location = db.Column(Geometry('POINT'))
  """The *magic* that allows us to perform quick geo expressions on the foodtrucks through the ORM.

  P.S. It's not magic, its the good work of the extension geoalchemy2
  """

  def to_json(self):
    """
    This is the synthetic interface that this application's models use to aid JSON serialization.  This method will create a `dict` that can be used by Flask's jsonify.  Importantly, it will not create keys for values the model considers null, maintaining the JSON spec.

    Returns:
      ``dict``
    """
    truck = {}
    if self.id:	truck['id'] = self.id
    if self.location_id:	truck['location_id'] = self.location_id
    if self.applicant:	truck['applicant'] = self.applicant
    if self.facility_type:	truck['facility_type'] = self.facility_type
    if self.cnn:	truck['cnn'] = self.cnn
    if self.location_description:	truck['location_description'] = self.location_description
    if self.address:	truck['address'] = self.address
    if self.blocklot:	truck['blocklot'] = self.blocklot
    if self.block:	truck['block'] = self.block
    if self.lot:	truck['lot'] = self.lot
    if self.permit:	truck['permit'] = self.permit
    if self.status:	truck['status'] = self.status
    if self.food_items:	truck['food_items'] = self.food_items
    if self.x:	truck['x'] = self.x
    if self.y:	truck['y'] = self.y
    if self.latitude:	truck['latitude'] = str(self.latitude)
    if self.longitude:	truck['longitude'] = str(self.longitude)
    if self.schedule_url:	truck['schedule_url'] = self.schedule_url
    if self.approved_at:	truck['approved_at'] = self.approved_at.isoformat()
    if self.received_at:	truck['received_at'] = self.received_at.isoformat()
    if self.prior_permit:	truck['prior_permit'] = self.prior_permit
    if self.expires_on:	truck['expires_on'] = self.expires_on.isoformat()
    return truck;
