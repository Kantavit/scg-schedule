from flask_migrate import Migrate
from flask_mysqldb import MySQL
from flask import session
from flask_session import Session
import yagmail
from .config import email, client_secret

db = MySQL()
migrate = Migrate()
sess = Session()
yag = yagmail.SMTP(email,oauth2_file=client_secret)