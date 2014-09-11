import flask
import unittest
import logging
import ujson as json
from decimal import Decimal
from foodtruck import create_app, db, setup_log
from foodtruck.backend import Foodtruck
from foodtruck.backend.models import columns

class FoodtruckTestCase(unittest.TestCase):

  def setUp(self):
    self.app = create_app(config_from_object='foodtruck.config.TestingConfig')
    db.init_app(self.app)
    self.client = self.app.test_client()
    self.setup_data()

  def tearDown(self):
    pass

  def setup_data(self):
    with self.app.app_context():
      self.truck = Foodtruck.query.limit(1).one()
      self.num_locations = Foodtruck.query.count()

      self.loc = {
        'lat':self.truck.latitude,
        'lon':self.truck.longitude,
      }

      self.paginate_1 = dict(self.loc.items() + {
                              'per_page': 1
                            }.items())

      self.paginate_2 = dict(self.paginate_1.items() + {
                              'page_num': 2
                            }.items())

  def test_list(self):
    rv = self.client.get('/api/foodtrucks')
    data = json.loads(rv.data)

    self.assertIn('foodtrucks', data)
    self.assertEqual(len(data['foodtrucks']), self.num_locations)

  def test_single(self):
    rv = self.client.get('/api/foodtrucks/{}'.format(self.truck.id))
    data = json.loads(rv.data)

    self.assertIsInstance(data, dict)
    self.assertIn('id', data)
    self.assertEqual(data['id'], self.truck.id)

  def test_single_contents(self):
    rv = self.client.get('/api/foodtrucks/{}'.format(self.truck.id))
    data = json.loads(rv.data)
    for column in columns(Foodtruck):
      self.assertIn(column, data)

  def test_nearest_basic(self):
    rv = self.client.get('/api/foodtrucks/nearby?lat={lat}&lon={lon}'
                         .format(**self.loc))
    data = json.loads(rv.data)

    self.assertIn('foodtrucks', data)
    self.assertEqual(len(data['foodtrucks']), self.num_locations)
    self.assertEqual(data['foodtrucks'][0]['id'], self.truck.id)

  def test_nearest_aliases(self):
    rv = self.client.get('/api/foodtrucks/nearby?latitude={lat}&longitude={lon}'
                         .format(**self.loc))
    data = json.loads(rv.data)

    self.assertIn('foodtrucks', data)
    self.assertEqual(len(data['foodtrucks']), self.num_locations)
    self.assertEqual(data['foodtrucks'][0]['id'], self.truck.id)

  def test_nearest_pagination(self):
    rv = self.client.get('/api/foodtrucks/nearby?'\
                         'lat={lat}&'\
                         'lon={lon}&'\
                         'per_page={per_page}'.format(**self.paginate_1))
    data = json.loads(rv.data)

    self.assertIn('foodtrucks', data)
    self.assertEqual(len(data['foodtrucks']), self.paginate_1['per_page'])
    self.assertEqual(data['foodtrucks'][0]['id'], self.truck.id)

  def test_nearest_pagination_next_page(self):
    rv = self.client.get('/api/foodtrucks/nearby?'\
                         'lat={lat}&'\
                         'lon={lon}&'\
                         'per_page={per_page}&'\
                         'page_num={page_num}'.format(**self.paginate_2))
    data = json.loads(rv.data)

    self.assertIn('foodtrucks', data)
    self.assertEqual(len(data['foodtrucks']), self.paginate_2['per_page'])
    self.assertNotEqual(data['foodtrucks'][0]['id'], self.truck.id)
