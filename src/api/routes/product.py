from flask import Blueprint
from flask import request, jsonify
from api.utils.responses import response_with 
from api.utils import responses as resp
from api.models.product import Product, ProductSchema
from api.models.category import Category
from api.utils.database import db

product_routes = Blueprint("product_routes", __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True, only=("id", "name"))

@product_routes.route("/<int:pk>")
def get_product(pk):
	try:
		product = Product.query.get(pk)
	except IntegrityError:
		return jsonify({"message": "Product could not be found."}), 400
	result = product_schema.dump(product)
	return jsonify({"product": result})
	
@product_routes.route('/')
def get_products():
	products = Product.query.all()
	result = product_schema.dump(products, many=True)
	return jsonify({"products": result})

@product_routes.route("/", methods=['POST'])
def new_product():
	try:
		json_data = request.get_json()
		if not json_data:
			return jsonify({"message": "No input data provided"}), 400
		try:
			data = product_schema.load(json_data)
		except ValidationError as err:
			return jsonify(err.messages), 422
		name = data["category"]["name"]
		category = Category.query.filter_by(name=name).first()
		if category is None:
			category = Category(name=name)
			db.session.add(category)
		product = Product(
				name=data["name"], category = category
				)
		db.session.add(product)
		db.session.commit()
		result = product_schema.dump(Product.query.get(product.id))
		return response_with(resp.SUCCESS_200, value={"product": result})
	except Exception as e:
		print(e)
		return response_with(resp.INVALID_INPUT_422)

@product_routes.route("/product/<int:id>", methods=["PUT"])
def update_product_by_id(id):
	data = request.get_json()
	if not data:
		return jsonify({"message": "No input data provided"}), 400
	get_product = Product.query.get(id)
	if data.get("name"):
		get_product.name = data["name"]
	if data.get("category"):
		get_product.category = Category.query.filter_by(name=data["category"]).first()
	db.session.add(get_product)
	db.session.commit()
	result = product_schema.dump(get_product)
	return {"message": "Updated product", "product": result}

@product_routes.route("/product/<int:id>", methods=["DELETE"])
def delete_product_by_id(id):
	get_product = Product.query.get(id)
	db.session.delete(get_product)
	db.session.commit()
	return {"message": "Deleted product"}
