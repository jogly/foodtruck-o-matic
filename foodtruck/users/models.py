from flask.ext.sqlalchemy import SQLAlchemy
from foodtruck.data import db, login_manager

@login_manager.request_loader
def load_user(request):
  return User.query.get(int(userid))

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String())
  first_name = db.Column(db.String())
  last_name = db.Column(db.String())
  password = db.Column(db.String())

  def is_authenticated(self):
        return True

  def is_active(self):
      return True

  def is_anonymous(self):
      return False

  def get_id(self):
      return unicode(self.id)

  def __repr__(self):
      return '<User %r>' % (self.nickname)

  def __init__(self, email, first_name, last_name, password):
    self.email = email
    self.first_name = first_name
    self.last_name = last_name
    self.password = password

  def __repr__(self):
    return '<email {}>'.format(self.email)
