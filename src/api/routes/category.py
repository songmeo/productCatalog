from flask import Blueprint
from flask import request, jsonify
from api.utils.responses import response_with 
from api.utils import responses as resp
from api.models.category import Category, CategorySchema
from api.utils.database import db

category_routes = Blueprint("category_routes", __name__)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@category_routes.route('/')
def get_categories():
	categories = Category.query.all()
	result = categories_schema.dump(categories)
	return jsonify({"categories": result})

@category_routes.route("/<int:pk>")
def get_category(pk):
	try:
		category = Category.query.get(pk)
	except IntegrityError:
		return {"message": "Category could not be found."}, 400
	category_result = category_schema.dump(category)
	products_result  = products_schema.dump(category.products.all())
	return {"category": category_result, "products": products_result}
	
@category_routes.route("/", methods=['POST'])
def new_category():
	try:
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
	except Exception as e:
		print(e)
		return response_with(resp.INVALID_INPUT_422)

@category_routes.route("/category/<int:id>", methods=['PUT'])
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
	return response_with(resp.SUCCESS_200, value={"category": result})

@category_routes.route("/category/<int:id>", methods = ['DELETE'])
def delete_category_by_id(id):
	get_category = Category.query.get(id)
	db.session.delete(get_category)
	db.session.commit()
	return {"message": "Deleted category"}
