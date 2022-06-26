from flask_migrate import Migrate
from flask_mysqldb import MySQL
from flask import session
from flask_session import Session


db = MySQL()
migrate = Migrate()
sess = Session()