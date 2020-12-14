#
#
# Mark Gonzalez
# CPSC 362-05
# 12-13-2020
# mgon025@csu.fullerton.edu
#
"""simple web app for a restaurant database"""

from datetime import datetime
from flask import Flask, redirect, flash, render_template, request
from sqlalchemy import exc
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String, unique=True)
    capacity = db.Column(db.Integer)
    dine_in = db.Column(db.Boolean)
    drive_through = db.Column(db.Boolean)
    delivery = db.Column(db.Boolean)
    pick_up = db.Column(db.Boolean)
    # time_start = db.Column(db.Date)
    # time_end = db.Column(db.Date)
    # days_open = db.Column(db.Date)

    def __repr__(self):
        return f'<{self.restaurant_name}, {self.capacity}, {self.dine_in}, {self.drive_through}, {self.delivery}, {self.pick_up}>'

db.create_all()
db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    "home page for the consumers"
    restaurants = Restaurant.query.all()

    if request.method == 'POST':
        restaurants = Restaurant.query.filter(Restaurant.restaurant_name.contains(request.form['service']),
                                              Restaurant.dine_in==bool(request.form.get('dinein')),
                                              Restaurant.drive_through==bool(request.form.get('drivethru')),
                                              Restaurant.delivery==bool(request.form.get('deliver')),
                                              Restaurant.pick_up==bool(request.form.get('pickup'))).all()

    return render_template('home.html', services=restaurants)

@app.route('/restaurant', methods=['GET', 'POST'])
def restaurant_admin():
    "home page for restaurant admin stuff"
    if request.method == 'POST':
        name = request.form['name']
        cap = request.form['capacity']
        dinein = bool(request.form.get('dinein'))
        drivethru = bool(request.form.get('drivethru'))
        deliver = bool(request.form.get('delivery'))
        pickup = bool(request.form.get('pickup'))

        new = Restaurant(restaurant_name=name, capacity=cap, dine_in=dinein,
                         drive_through=drivethru, delivery=deliver, pick_up=pickup)
        db.session.add(new)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash('error: could not insert into database.')

    restaurants = Restaurant.query.all()
    return render_template('admin.html', services=restaurants)

@app.route('/delete/<rid>', methods=['GET'])
def delete(rid=-1):
    "deletes a restaurant from the database"
    trash = Restaurant.query.get(rid)
    if trash is None:
        flash(f'error: restaurant id \'{rid}\' does not exist.')
    else:
        db.session.delete(trash)
        db.session.commit()
    return redirect('/restaurant')

