from flask_migrate import Migrate
from flask_mysqldb import MySQL
# from flask import session

db = MySQL()
migrate = Migrate()
# sess = Session()