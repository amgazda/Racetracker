from flask import Blueprint, render_template, request, flash
from . import engine, session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
views = Blueprint('views', __name__)

Base = declarative_base()

# Class Store(name, headquarter, storeType)  <--> Pricelist.stores(name, headquarter, storeType)
class Tire(Base):
    __tablename__ = 'tires'
 
    tireId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    manufacturer = sqlalchemy.Column(sqlalchemy.String(length=50))
    compound = sqlalchemy.Column(sqlalchemy.String(length=10))
    tireCorner = sqlalchemy.Column(sqlalchemy.String(length=20))
    carNumber = sqlalchemy.Column(sqlalchemy.Integer)
    lapsRun = sqlalchemy.Column(sqlalchemy.Integer)
    heatCycles = sqlalchemy.Column(sqlalchemy.Integer)
     
    def __repr__(self):
        return "<Store(tireId='{0}', manufacturer='{1}', compound='{2}', tireCorner='{3}', carNumber='{4}', lapsRun='{5}', heatCycles='{6}')>".format(
                            self.tireId, self.manufacturer, self.compound, self.tireCorner, self.carNumber, self.lapsRun, self.heatCycles)
 
Base.metadata.create_all(engine) # creates the tires table


@views.route('/')
def start():
    return render_template("home.html")

@views.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        ftireId = request.form.get('tireId')
        fmanufacturer = request.form.get('manufacturer')
        fcompound = request.form.get('compound')
        ftireCorner = request.form.get('corner')
        fcarNumber = request.form.get('number')
        flapsRun = request.form.get('laps')
        fheatCycles = request.form.get('cycles')
        flash('Added', category='success')
        newTire = Tire(tireId=ftireId, manufacturer=fmanufacturer, compound=fcompound, tireCorner=ftireCorner, carNumber=fcarNumber, lapsRun=flapsRun, heatCycles=fheatCycles)
        session.add(newTire)
        session.commit()


    data = request.form
    print(data)
    return render_template("insert.html")