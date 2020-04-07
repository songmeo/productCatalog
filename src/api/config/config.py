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

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_ECHO = False
	JWT_SECRET_KEY = 'JWT-SECRET'
	SECRET_KEY = 'SECRET-KEY'
	SECURITY_PASSWORD_SALT = 'PASSWORD-SALT'
	MAIL_DEFAULT_SENDER= ''
	MAIL_SERVER= 'smtp.gmail.com'
	MAIL_PORT= 465
	MAIL_USERNAME= ''
	MAIL_PASSWORD= ''
	MAIL_USE_TLS= False
	MAIL_USE_SSL= True
	UPLOAD_FOLDER= 'images'
