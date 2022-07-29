from flask import Flask
from .extensions import db, migrate, sess
from .routes.employee import employee
from .routes.manager import manager
from .routes.director import director
from .config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, secret_key

# Database from Hostinger 
def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
    app.config['MYSQL_DB'] = MYSQL_DB
    db.init_app(app)

    app.secret_key = secret_key
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    
    migrate.init_app(app, db)

    app.register_blueprint(employee)
    app.register_blueprint(manager)
    app.register_blueprint(director)
    
    return app
