import json, io
from api.utils.test_base import BaseTestCase
from api.models.model import Product, ProductSchema, Category, CategorySchema
import unittest2 as unittest

def create_category():
	category = Category(name="meaat")
	return category

class TestCategories(BaseTestCase):
	def setUp(self):
		super(TestCategories, self).setUp()
	
	def test_create_category(self):
		category = {
			'name': 'meat'
		}
		response = self.app.post(
			'/api/categories/',
			data=json.dumps(category),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
	
	def test_update_category(self):
		category = Category(name="meaat").create()
		update_info = {
			'name': 'meat'
		}
		response = self.app.put(
			'/api/categories/' + str(category.id),
			data=json.dumps(update_info),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
		
	def test_create_duplicate_category(self):
		Category(name="meat").create()
		new_category = {
			'name': 'meat'
		}
		response = self.app.post(
			'/api/categories/',
			data=json.dumps(new_category),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(201, response.status_code)

	def test_delete_category(self):
		category = Category(name="meat").create()
		response = self.app.delete(
			'/api/categories/' + str(category.id),
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)

if __name__ == '__main__':
	unittest.main()

