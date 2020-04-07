from api.utils.database import db
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError, pre_load

def must_not_be_blank(data):
	if not data:
		raise ValidationError("Data not provided.")
		
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
	category = db.relationship("Category", backref=db.backref("products", lazy="dynamic"))

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
