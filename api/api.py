from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kat/adcash/database/products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	category = db.Column(db.String(20))
	
	def __init__(self, name, category):
		self.name = name
		self.category = category
	def __repr__(self):
		return '<Product %d>' % self.id
db.create_all()

class ProductSchema(ModelSchema):
	class Meta(ModelSchema.Meta):
		model = Products
		sqla_session = db.session
	
	id = fields.Number(dump_only=True)
	name = fields.String(required=True)
	category = fields.String(required=True)
	
@app.route('/products', methods=['GET'])
def index():
	get_products = Products.query.all()
	product_schema = ProductSchema(many=True)
	products = product_schema.dump(get_products)
	return {"products": products}
	
if __name__ == '__main__':
	app.run(debug=True)

'''
product1 = Products("banana", "fruit")
product2 = Products("tuna", "fish")
db.session.add(product1)
db.session.add(product2)
db.session.commit()
@app.route('/products', methods=['POST'])
def create_product():
	data = request.get_json()
	product_schema = ProductSchema()
	product, error = product_schema.load(data)
	result = product_schema.dump(product.create()).data
	return make_response(jsonify({"product": products}),201)
	
products = [
	{'id': 0,
	'name': 'banana',
	'subcategory': '',
	'category': 'fruit',
	},
	{'id': 1,
	'name': 'tuna',
	'subcategory': 'fish',
	'category': 'meat'
	},
	{'id': 2,
	'name': 'salmon',
	'subcategory': 'fish',
	'category': 'meat'
	}
]

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



#Getting the list of all categories
@app.route('/categories', methods=['GET'])
def listAllCategories() {
	categories = []
	
}

@app.route('/products', methods=['GET'])
def listAll():
	return jsonify(products)

@app.route('/products', methods=['GET'])
def listByCategory():
	if 'category' in request.args:
		category = request.args['category']
	else:
		return "Please specify a category."

	results = []

	for p in products:
		if p['category'] == category:
			results.append(p)
	return jsonify(results)
"""
@app.route('/api/v1/resources/products', methods=['POST'])
def addProduct():
	
@app.route('/api/v1/resources/products', methods=['POST'])
def addCategory():
"""
'''

