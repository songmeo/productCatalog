from flask import Blueprint
from flask import request, jsonify
from api.utils.responses import response_with 
from api.utils import responses as resp
from api.models.model import Product, ProductSchema, Category, CategorySchema
from api.utils.database import db
from marshmallow import ValidationError

category_routes = Blueprint("category_routes", __name__)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True, only=("id", "name"))
product_schema = ProductSchema()
products_schema = ProductSchema(many=True, only=("id", "name"))

@category_routes.route('/')
def get_categories():
	categories = Category.query.all()
	result = categories_schema.dump(categories)
	return {"categories": result}

@category_routes.route("/<int:pk>")
def get_category(pk):
	category = Category.query.get(pk)
	if not category:
		return response_with(resp.BAD_REQUEST_400, value={"message": "Category could not be found."})
	category_result = category_schema.dump(category)
	return {"category": category_result}
	
@category_routes.route("/", methods=['POST'])
def new_category():
	json_data = request.get_json()
	if not json_data:
		return response_with(resp.BAD_REQUEST_400, value={"message": "No input data provided"})
	try:
		data = category_schema.load(json_data)
	except ValidationError as err:
		return response_with(resp.INVALID_INPUT_422)
	name = data["name"]
	category = Category.query.filter_by(name=name).first()
	if category is not None:
		return response_with(resp.SUCCESS_201, value={"message": "Category existed"})
	category = Category(name=name, products=[])
	products = data["products"]
	for p in products:
		product = Product.query.filter_by(name=p["name"]).first()
		if product is None:
			product = Product(name=p["name"])
			db.session.add(product)
		category.products.append(product)
	db.session.add(category)
	db.session.commit()
	result = category_schema.dump(category)
	return {"message": "Created new category.", "category": result}

@category_routes.route("/<int:id>", methods=['PATCH'])
def modify_category_by_id(id):
	category = Category.query.get(id)
	if category is None:
		return response_with(resp.BAD_REQUEST_400, value={"message": "No such category"})
	data = request.get_json()
	if not data:
		return response_with(resp.BAD_REQUEST_400, value={"message": "No input data provided"})
	if data.get('name'):
		category.name = data['name']
	if data.get('products'):
		products = data['products']
		for p in products:
			product = Product.query.filter_by(name=p).first()
			if product is None:
				product = Product(name=p)
				db.session.add(product)
			category.products.append(product)
	db.session.add(category)
	db.session.commit()
	result = category_schema.dump(category)
	return response_with(resp.SUCCESS_200, value={"category": result})
	
@category_routes.route("/<int:id>", methods=['PUT'])
def update_category_by_id(id):
	json_data = request.get_json()
	if not json_data:
		return response_with(resp.BAD_REQUEST_400, value={"message": "No input data provided"})
	try:
		data = category_schema.load(json_data)
	except ValidationError as err:
		return response_with(resp.INVALID_INPUT_422)
	category = Category.query.get(id)
	category_exist = Category.query.filter_by(name=data["name"]).first()
	if category_exist:
		return response_with(resp.BAD_REQUEST_400, value={"message": "Category existed"})
	category.name = data["name"]
	category.products = []
	products = data["products"]
	for p in products:
		product = Product(name=p["name"])
		db.session.add(product)
		category.products.append(product)
	db.session.add(category)
	db.session.commit()
	result = category_schema.dump(category)
	return response_with(resp.SUCCESS_200, value={"category": result})

@category_routes.route("/", methods = ['DELETE'])
def delete_all():
	Category.query.delete()
	db.session.commit()
	return response_with(resp.SUCCESS_200)

@category_routes.route("/<int:id>/products", methods = ['DELETE'])
def delete_products_from_category(id):
	category = Category.query.get(id)
	if not category:
		return response_with(resp.BAD_REQUEST_400, value={"message": "no category found"})
	data = request.get_json()
	if not data:
		return response_with(resp.BAD_REQUEST_400, value={"message": "No input data provided"})
	products = data['products']
	if products is None:
		return response_with(resp.INVALID_FIELD_NAME_SENT_422)
	for p in products:
		product = Product.query.filter_by(name=p).first()
		if product and (product in category.products):
			category.products.remove(product)
	db.session.add(category)
	db.session.commit()
	result = category_schema.dump(category)
	return response_with(resp.SUCCESS_200, value={"category": result})
	
	
@category_routes.route("/<int:id>", methods = ['DELETE'])
def delete_category_by_id(id):
	category = Category.query.get(id)
	if not category:
		return response_with(resp.BAD_REQUEST_400, value={"message": "no category found"})
	db.session.delete(category)
	db.session.commit()
	return {"message": "Deleted category"}
