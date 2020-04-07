import json, io
from api.utils.test_base import BaseTestCase
from api.models.model import Product, ProductSchema, Category, CategorySchema
import unittest2 as unittest

class TestProducts(BaseTestCase):
	def setUp(self):
		super(TestProducts, self).setUp()
	
	def test_create_product(self):
		product = {
			'name': 'banana',
			'category': 'fruit'
		}
		response = self.app.post(
			'/api/products/',
			data=json.dumps(product),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
	
'''
	def test_create_duplicate_product(self):
		product = 
'''
