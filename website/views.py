from flask import Blueprint, render_template, request, flash
from . import engine, session, pwd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
views = Blueprint('views', __name__)

Base = declarative_base()
names = ("Tire ID","Manufacturer","Compound","Tire Corner","Car Number","Laps Run","Heat Cycles","Date Purchased")
#data = ("Tire ID","Manufacturer","Compound","Tire Corner","Car Number","Laps Run","Heat Cycles","Date Purchased")

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
    buyDate = sqlalchemy.Column(sqlalchemy.Date)
     
    def __repr__(self):
        return "<Store(tireId='{0}', manufacturer='{1}', compound='{2}', tireCorner='{3}', carNumber='{4}', lapsRun='{5}', heatCycles='{6}', buyDate='{7}')>".format(
                            self.tireId, self.manufacturer, self.compound, self.tireCorner, self.carNumber, self.lapsRun, self.heatCycles, self.buyDate)
 
Base.metadata.create_all(engine) # creates the tires table
connection=mysql.connector.connect(host="34.41.97.159", user="root", password=pwd, database="racetracker")

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
        fbuyDate = request.form.get('buy')
        flash('Added', category='success')
        newTire = Tire(tireId=ftireId, manufacturer=fmanufacturer, compound=fcompound, tireCorner=ftireCorner, carNumber=fcarNumber, lapsRun=flapsRun, heatCycles=fheatCycles, buyDate=fbuyDate)
        session.add(newTire)
        session.commit()


    data = request.form
    print(data)
    return render_template("insert.html")

@views.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    data = ("Tire ID","Manufacturer","Compound","Tire Corner","Car Number","Laps Run","Heat Cycles","Date Purchased")
    if request.method == 'POST':
        if request.form['button']=='retr_all':
            cursor=connection.cursor()
            cursor.callproc("retr_all")
            for result in cursor.stored_results():
                data=result.fetchall()
                print(data)
            flash('Success', category='success')
            return render_template("retrieve.html",namesh=names,datas=data)
        elif request.form['button']=='retr_between':
            cursor=connection.cursor()
            if(request.form.get('between_sd'))!='' and request.form.get('between_ed')!='':
                cursor.callproc("retr_between",args=(request.form.get('between_sd'),request.form.get('between_ed')))
                for result in cursor.stored_results():
                    data=result.fetchall()
                    print(data)
                flash('Success', category='success')
                return render_template("retrieve.html",namesh=names,datas=data)
            else:
                flash('Error: empty parameter', category='error')
    return render_template("retrieve.html",namesh=names)

@views.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        if request.form['button']=='sub':
            data=("Placeholder")
            cursor=connection.cursor()
            val=request.form['sid']
            data2=("Placeholder")
            cursor.callproc("all_ids")
            for result in cursor.stored_results():
                data2=result.fetchall()
                print(data2)
            if val!='none':
                cursor.execute("SELECT * FROM tires WHERE tireId="+str(val))
                data=cursor.fetchall()
                print(data)
                return render_template("delete.html",namesh=names,datas=data,dataii=data2,conf=(int(val)),show=True)
            else:
                return render_template("delete.html",namesh=names,dataii=data2)
        elif request.form['button']=='delconf':
            pass
    else:
        data=("Placeholder")
        cursor=connection.cursor()
        cursor.callproc("all_ids")
        for result in cursor.stored_results():
            data=result.fetchall()
            print(data)
        return render_template("delete.html",namesh=names,dataii=data)

