import json, io
from api.utils.test_base import BaseTestCase
from api.models.category import Category
from api.models.product import Product
import unittest2 as unittest

class TestCategories(BaseTestCase):
	def setUp(self):
		super(TestCategories, self).setUp()
	
	def test_create_categories(self):
		category = {
			'name': 'vegetables'
		}
		response = self.app.post(
			'/api/categories/',
			data=json.dumps(category),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)

if __name__ == '__main__':
	unittest.main()

