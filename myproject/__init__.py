from flask import Flask
from .extensions import db, migrate
from .routes.employee import employee
from .routes.manager import manager

# Database from Hostinger 
def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = "sql596.main-hosting.eu"
    app.config['MYSQL_USER'] = "u662141035_sts"
    app.config['MYSQL_PASSWORD'] = "Hellothailand123-"
    app.config['MYSQL_DB'] = "u662141035_OT"
    db.init_app(app)

    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    
    migrate.init_app(app, db)

    app.register_blueprint(employee)
    app.register_blueprint(manager)
    
    return app
