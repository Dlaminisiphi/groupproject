from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
#Database
db= SQLAlchemy()
DB_NAME="database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='abc'
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #import blueprints
    from .views import views
    from .auth import auth
    
    #Register them
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, report




        
    create_database(app)

    return app

def create_database(app):
 if not path.exists('website/' + DB_NAME):
    with app.app_context():
       db.create_all()
    print('Created database')



  
