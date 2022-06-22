from flask_migrate import Migrate
from flask_mysqldb import MySQL

db = MySQL()
migrate = Migrate()