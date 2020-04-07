class Config(object):
	DEBUG = False
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:////home/kat/adcash/database/products.db'
	
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:////home/kat/adcash/database/products.db'
	SQLALCHEMY_ECHO = False
	
class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:////home/kat/adcash/database/products.db'
	SQLALCHEMY_ECHO = False
