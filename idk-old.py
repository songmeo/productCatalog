from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError, pre_load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

##### MODELS #####
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	#products = db.relationship("Product", backref="Category", cascade="all, delete-orphan")

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
	category = db.relationship("Category", backref=db.backref("products", lazy="dynamic"))

##### SCHEMAS #####
def must_not_be_blank(data):
	if not data:
		raise ValidationError("Data not provided.")

class CategorySchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str()

class ProductSchema(Schema):
	id = fields.Int(dump_only=True)
	category = fields.Nested(CategorySchema, validate=must_not_be_blank)
	name = fields.Str(required=True, validate=must_not_be_blank)
	@pre_load
	def process_category(self, data, **kwargs):
		category_name = data.get("category")
		if category_name:
			name = category_name
			category_dict = dict(name=name)
		else:
			category_dict = {}
		data["category"] = category_dict
		return data

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True, only=("id", "name"))

##### API #####
@app.route('/categories')
def get_categories():
	categories = Category.query.all()
	result = categories_schema.dump(categories)
	return jsonify({"categories": result})

@app.route("/categories/<int:pk>")
def get_category(pk):
	try:
		category = Category.query.get(pk)
	except IntegrityError:
		return {"message": "Category could not be found."}, 400
	category_result = category_schema.dump(category)
	products_result  = products_schema.dump(category.products.all())
	return {"category": category_result, "products": products_result}

@app.route("/products/<int:pk>")
def get_product(pk):
	try:
		product = Product.query.get(pk)
	except IntegrityError:
		return jsonify({"message": "Product could not be found."}), 400
	result = product_schema.dump(product)
	return jsonify({"product": result})
	
@app.route('/products')
def get_products():
	products = Product.query.all()
	result = product_schema.dump(products, many=True)
	return jsonify({"products": result})

@app.route("/products/", methods=['POST'])
def new_product():
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
	return {"message": "Created new product.", "product": result}

@app.route("/product/<int:id>", methods=["PUT"])
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

@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product_by_id(id):
	get_product = Product.query.get(id)
	db.session.delete(get_product)
	db.session.commit()
	return {"message": "Deleted product"}

@app.route("/categories/", methods=['POST'])
def new_category():
	json_data = request.get_json()
	if not json_data:
		return jsonify({"message": "No input data provided"}), 400
	try:
		data = category_schema.load(json_data)
	except ValidationError as err:
		return jsonify(err.messages), 422
	name = data["name"]
	category = Category.query.filter_by(name=name).first()
	if category is None:
		category = Category(name=name)
		db.session.add(category)
		db.session.commit()
		result = category_schema.dump(Category.query.get(category.id))
		return {"message": "Created new category.", "category": result}
	else:
		return {"message": "Category existed"}

@app.route("/category/<int:id>", methods=['PUT'])
def update_category_by_id(id):
	json_data = request.get_json()
	if not json_data:
		return jsonify({"message": "No input data provided"}), 400
	try:
		data = category_schema.load(json_data)
	except ValidationError as err:
		return jsonify(err.messages), 422
	get_category = Category.query.get(id)
	if data.get("name"):
		get_category.name = data["name"]
	db.session.add(get_category)
	db.session.commit()
	result = category_schema.dump(get_category)
	return {"message": "Updated category", "category": result}

@app.route("/category/<int:id>", methods = ['DELETE'])
def delete_category_by_id(id):
	get_category = Category.query.get(id)
	db.session.delete(get_category)
	db.session.commit()
	return {"message": "Deleted category"}
	
if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)

'''
Getting the list of all categories;
Getting the list of products of the concrete category;
Create/update/delete of category;
Create/update/delete of product;

Response results should have JSON encoding;
The assignment results should be published on github including a short ReadMe abouthow to deploy the application;

Evaluation criteria
Architectural organization of API;
Code readability;
Error handling;
Unit tests coverage
'''

