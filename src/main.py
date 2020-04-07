import os, sys, logging
from flask import Flask, jsonify
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.category import category_routes
from api.routes.product import product_routes
from api.config.config import Config, ProductionConfig, TestingConfig, DevelopmentConfig

def create_app(config):
	app = Flask(__name__)
	app.config.from_object(app_config)
	app.register_blueprint(category_routes, url_prefix='/api/categories')
	app.register_blueprint(product_routes, url_prefix='/api/products')
	# START GLOBAL HTTP CONFIGURATIONS
	@app.after_request
	def add_header(response):    
		return response
		
	@app.errorhandler(400)
	def bad_request(e):    
		logging.error(e)    
		return response_with(resp.BAD_REQUEST_400)

	@app.errorhandler(500)
	def server_error(e):    
		logging.error(e)    
		return response_with(resp.SERVER_ERROR_500)
		
	@app.errorhandler(404)
	def not_found(e):    
		logging.error(e)    
		return response_with(resp.SERVER_ERROR_404)
		
	db.init_app(app)
	with app.app_context():
		db.create_all()
	return app


if os.environ.get('WORK_ENV') == 'PROD':
	app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
	app_config = TestingConfig
else:
	app_config = DevelopmentConfig
	
app = create_app(app_config)

if __name__ == "__main__":
	app.run(port=5000, host="0.0.0.0", use_reloader=False)
