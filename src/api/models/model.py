from api.utils.database import db
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

##### MODELS #####
associations = db.Table('associations',
	db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
	db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	products = db.relationship(
				"Product", 
				secondary=associations, lazy="subquery",
				back_populates="categories")
	def __init__(self, name):
		self.name = name
	def create(self):
		db.session.add(self)
		db.session.commit()
		return self

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	categories = db.relationship(
				"Category", 
				secondary=associations, lazy="subquery",
				back_populates="products")
	def __init__(self, name):
		self.name = name
		
	def create(self):
		db.session.add(self)
		db.session.commit()
		return self

##### SCHEMAS #####
def must_not_be_blank(data):
	if not data:
		raise ValidationError("Data not provided.")

class ProductSchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str(required=True, validate=must_not_be_blank)
	categories = fields.Nested(lambda: CategorySchema(only=("id", "name")))
	
class CategorySchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str(required=True, validate=must_not_be_blank)
	products = fields.List(fields.Nested(ProductSchema(only=("id", "name"))))


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True, only=("id", "name"))
product_schema = ProductSchema()
products_schema = ProductSchema(many=True, only=("id", "name"))
