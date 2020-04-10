from flask import Blueprint
from flask import request, jsonify
from api.utils.responses import response_with 
from api.utils import responses as resp
from api.models.model import Product, ProductSchema, Category, CategorySchema
from api.utils.database import db
from marshmallow import ValidationError
product_routes = Blueprint("product_routes", __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True, only=("id", "name"))

@product_routes.route("/<int:pk>")
def get_product(pk):
	product = Product.query.get(pk)
	if not product:
		return response_with(resp.SERVER_ERROR_404)
	result = product_schema.dump(product)
	return jsonify({"product": result})
	
@product_routes.route('/')
def get_products():
	products = Product.query.all()
	result = products_schema.dump(products)
	return jsonify({"products": result})

@product_routes.route("/", methods=['POST'])
def new_product():
	data = request.get_json()
	if not data:
		return response_with(resp.INVALID_INPUT_422)
	try:
		data = product_schema.load(data)
	except ValidationError as err:
		return response_with(resp.INVALID_INPUT_422)	
	exists = Product.query.filter_by(name=data["name"]).first()
	if exists:
		return response_with(resp.SUCCESS_201, value={"message": "product existed"})
	product = Product(name=data["name"])
	categories = data.get("categories")
	if categories:
		for c in categories:
			category = Category.query.filter_by(name=c['name']).first()
			if category is None:
				category = Category(name=c['name'])
				db.session.add(category)
			product.categories.append(category)
	db.session.add(product)
	db.session.commit()
	result = product_schema.dump(Product.query.get(product.id))
	return response_with(resp.SUCCESS_200, value={"product": result})
	
@product_routes.route("/<int:id>", methods=["PUT"])
def update_products_by_id(id):	
	json_data = request.get_json()
	if not json_data:
		return response_with(resp.INVALID_INPUT_422)
	try:
		data = product_schema.load(json_data)
	except ValidationError as err:
		return response_with(resp.INVALID_INPUT_422)
	product = Product.query.get(id)
	product.name = data["name"]
	product.categories = []
	try:
		categories = data["categories"]
	except:
		return repsonse_with(resp.MISSING_PARAMETERS_422)
	for c in categories:
		category = Category(name=c["name"])
		db.session.add(category)
		category.products.append(product)
	try:
		db.session.add(product)
	except:
		return response_with(resp.BAD_REQUEST_400, value={"message": "Product existed"})
	db.session.commit()
	result = product_schema.dump(product)
	return response_with(resp.SUCCESS_200, value={"product": result})

@product_routes.route("/", methods=["DELETE"])
def delete_all_products():
	Product.query.delete()
	db.session.commit()
	return response_with(resp.SUCCESS_200)

@product_routes.route("/<int:id>", methods=["DELETE"])
def delete_product_by_id(id):
	get_product = Product.query.get(id)
	db.session.delete(get_product)
	db.session.commit()
	return response_with(resp.SUCCESS_200, value={"message": "Deleted product"})
