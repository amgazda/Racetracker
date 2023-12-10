from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base

f = open("C:\\users\\andre\\pass.txt", "r")
pwd = f.read(12)
f.close()

str = 'mysql+mysqlconnector://root:' + pwd + '@34.41.97.159:3306/racetracker'

db = SQLAlchemy()
DB_NAME = "racetracker.db"
engine = sqlalchemy.create_engine(str, echo=True, isolation_level="READ COMMITTED")

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ClichedTree'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
