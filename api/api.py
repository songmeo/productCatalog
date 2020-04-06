from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError, pre_load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kat/adcash/database/products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

##### MODELS #####
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	
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

@app.route('/categories')
def get_categories():
	categories = Category.query.all()
	result = categories_schema.dump(categories)
	return {"categories": result}

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
	
@app.route('/products/', methods=['GET'])
def get_products():
	products = Product.query.all()
	result = product_schema.dump(products)
	return {"products": result}
	

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
'''
@app.route('/categories', methods=['GET'])
def listAllCategories():
	 

@app.route('/products', methods=['POST'])
def create_product():
	data = request.get_json()
	if not data:
		return {"message": "no input provided"}, 400
	product_schema = ProductSchema()
	product = product_schema.load(data)
	result = product_schema.dump(product.create())
	return {"message": "new product added", "product": result}
	

'''
'''
Getting the list of all categories;
Getting the list of products of the concrete category;
Create/update/delete of category;
Create/update/delete of product;

The application should be written in one of the following languages (Golang, Python,PHP, JavaScript);
Response results should have JSON encoding;
The assignment results should be published on github including a short ReadMe abouthow to deploy the application;

Evaluation criteria
Architectural organization of API;
Code readability;
Error handling;
Unit tests coverage
'''

