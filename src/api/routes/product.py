from flask import Blueprint
from flask import request, jsonify
from api.utils.responses import response_with 
from api.utils import responses as resp
from api.models.model import Product, ProductSchema, Category, CategorySchema
from api.utils.database import db

product_routes = Blueprint("product_routes", __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True, only=("id", "name"))

@product_routes.route("/<int:pk>")
def get_product(pk):
	product = Product.query.get(pk)
	if not product:
		return response_with(resp.BAD_REQUEST_400, {"message": "Product could not be found."})
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
		return response_with(resp.BAD_REQUEST_400, value={"message": "No input data provided"})
	product = Product.query.filter_by(name=data["name"]).first()
	if product is None:
		product = Product(name=data["name"])
		category = Category.query.filter_by(name=data["category"]).first()
		if category is None:
			category = Category(name=data["category"],products=[])
			db.session.add(category)
		category.products.append(product)
		db.session.add(product)
		db.session.commit()
		result = product_schema.dump(Product.query.get(product.id))
		return response_with(resp.SUCCESS_200, value={"product": result})
	return response_with(resp.SUCCESS_201, value={"message": "product existed"})

@product_routes.route("/<int:id>", methods=["PUT"])
def change_product_name_by_id(id):
	data = request.get_json()
	if not data:
		return response_with(resp.BAD_REQUEST_400, value={"message": "No input data provided"})
	get_product = Product.query.get(id)
	if not get_product:
		return response_with(resp.BAD_REQUEST_400, value={"message": "no product found"})
	get_product.name = data["name"]
	db.session.add(get_product)
	db.session.commit()
	result = product_schema.dump(get_product)
	return response_with(resp.SUCCESS_201, value={"product": result})

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
	return response_with(resp.SUCCESS_204, value={"message": "Deleted product"})
