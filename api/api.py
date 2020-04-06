from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError, pre_load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kat/adcash/database/products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
	category = db.relationship("Category", backref=db.backref("products", lazy="dynamic"))
	'''
	def create(self):
		db.session.add(self)
		db.session.commit()
		return self
	def __init__(self, name, category):
		self.name = name
		self.category = category
	def __repr__(self):
		return '<Product %d>' % self.id
	'''

db.create_all()

class CategorySchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str()

def must_not_be_blank(data):
	if not data:
		raise ValidationError("Data not provided.")
		
class ProductSchema(Schema):
	id = fields.Int(dump_only=True)
	category = fields.Nested(CategorySchema, validate=must_not_be_blank)
	name = fields.Str(required=True, validate=must_not_be_blank)
'''
	class Meta(ModelSchema.Meta):
		model = Product
		sqla_session = db.session
'''


@app.route('/products', methods=['GET'])
def index():
	get_products = Product.query.all()
	product_schema = ProductSchema(many=True)
	products = product_schema.dump(get_products)
	return {"products": products}
	
if __name__ == '__main__':
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

