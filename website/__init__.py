from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()#defining database object
DB_NAME = "database.db"#setting our DB name to database.db


def create_app():
	app = Flask(__name__)#initialization off flask app
	app.config['SECRET_KEY'] = 'HJDJDDJDJJD'#encrypts cookies or data related to our website
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'#LOCATION OR WHERE DATABSE IS STORED(telling flask it is stored in website folder)
	db.init_app(app) #initializing database with flask app created  

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix = '/')#registering the blueprint of the views route
	app.register_blueprint(auth, url_prefix = '/')#registering the blueprint of the auth route

	from .models import User, Note

	with app.app_context():
		db.create_all()

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))
 

	return app

