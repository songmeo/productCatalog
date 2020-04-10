import json, io
from api.utils.test_base import BaseTestCase
from api.models.model import Product, ProductSchema, Category, CategorySchema
import unittest2 as unittest

def create_category():
	category = Category(name="meaat").create()
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
		category = create_category()
		update_info = {
			'name': 'meat',
			'products': ['pork']
		}
		response = self.app.put(
			'/api/categories/' + str(category.id),
			data=json.dumps(update_info),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
		
	def test_create_duplicate_category(self):
		create_category()
		new_category = {
			'name': 'meaat'
		}
		response = self.app.post(
			'/api/categories/',
			data=json.dumps(new_category),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(201, response.status_code)

	def test_delete_category(self):
		category = create_category()
		response = self.app.delete(
			'/api/categories/' + str(category.id),
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)

	def test_update_category(self):
		category = create_category()
		update_info = {
			'name': 'meat',
			'products': ["cat","dog"]
		}
		response = self.app.put(
			'/api/categories/' + str(category.id),
			data=json.dumps(update_info),
			content_type='application/json',
		)
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
		
	def test_adding_same_product_to_many_categories(self):
		product = {
			'products': ['beef']
		}
		category1 = Category(name="meat").create()
		category2 = Category(name="others").create()
		response1 = self.app.patch(
			'/api/categories/' + str(category1.id) + '/add',
			data=json.dumps(product),
			content_type='application/json',
		)
		response2 = self.app.patch(
			'/api/categories/' + str(category2.id) + '/add',
			data=json.dumps(product),
			content_type='application/json',
		)
		self.assertEqual(200, response1.status_code)
		self.assertEqual(200, response2.status_code)
	
	def test_removing_products_from_category(self):
		category = Category(name='meat', products=['beef']).create()
		product = {
			'products': ['beef']
		}
		response = self.app.patch(
			'/api/categories/' + str(category.id) + '/remove',
			data=json.dumps(product),
			content_type='application/json',
		)
		self.assertEqual(200, response.status_code)

		
if __name__ == '__main__':
	unittest.main()
