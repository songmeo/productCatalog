import flask
from flask import request, jsonify, abort, make_response

app = flask.Flask(__name__)

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

@app.route('/', methods=['GET'])
def home():
	return "<h1>Product Catalogue</h1>"
	
@app.route('/api/v1/resources/products/all', methods=['GET'])
def listAll():
	return jsonify(products)

@app.route('/api/v1/resources/products', methods=['GET'])
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

@app.route('/api/v1/resources/products', methods=['POST'])
def addProduct():
	if not request.json:
		abort(400)
	product = {
		'id': products[-1]['id'] + 1,
		'name': request.json['name'],
		'subcategory': request.json['subcategory'],
		'category': request.json['category']
	}
	products.append(product)
	return jsonify(products)

@app.errorhandler(404)
def notFound(error):
	error = "not found"
	return make_response(jsonify(error), 404)

if __name__ == '__main__':
	app.run(debug=True)
