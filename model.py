from flask_sqlalchemy import SQLAlchemy
from flask import Flask,url_for, render_template
import bcrypt
from __init__ import server
from flask_login import UserMixin
from sqlalchemy import func, and_
from yahoo import df,getStock,getStockNow
from decimal import *

db = SQLAlchemy(server)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(500))
    salt = db.Column(db.String(100))
    confirmed = db.Column(db.Boolean, default=False)
    money = db.Column(db.Numeric(10,2))

    def __init__(self, username, email, password,money):
        self.username = username.lower()
        self.email = email.lower()
        self.pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.money = money

    def is_active(self):
        return True

    def is_authenticated(self):
        if self.confirmed == 1:
            return True
        else:
            return False

    def is_annonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.pw_hash.encode('utf-8'))

    def is_admin(self):
        if self.email in ['roddene1@gmail.com']:
            return True
        else:
            return False

#from S.mail import generate_confirmation_token, send_email


def create_user(username, email, password):
    newuser = User(username, email, password,10000.69)
    db.session.add(newuser)
    newuserStock = StockData()
    db.session.add(newuserStock)
    db.session.commit()
    db.session.remove()


    #token = generate_confirmation_token(newuser.email)
    #confirm_url = url_for('regular.verify_email', token=token, _external=True)
    #html = render_template('activate.html', confirm_url=confirm_url)
    #subject = "Please confirm your email"
    #send_email(newuser.email, subject, html)
    return newuser




class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    for c in df['Symbol'].values.tolist():
        locals()[str(c)] = db.Column(db.Float,default = 0)

def getStockValue(user,stock):
    id = User.query.filter_by(username = user).first().id
    userStock = StockData.query.filter_by(id=id).first()
    return getattr(userStock,stock)
def editData(user,stock,amount,buy):
    curUser = User.query.filter_by(username = user).first()
    userStock = StockData.query.filter_by(id=curUser.id).first()
    stockValue = getStockValue(user,stock)
    buyAmount = amount*getStockNow(stock)
    print(buyAmount)
    if buy:
        if buyAmount<=curUser.money:
            setattr(userStock,stock,stockValue+float(amount))
            print(curUser.money)
            curUser.money-=Decimal(buyAmount)
        else:
            print("Not enough money")
    else:
        if amount <= getattr(userStock,stock):
            setattr(userStock,stock,stockValue-float(amount))
            curUser.money+=Decimal(buyAmount)
        else:
            print("not enough stock")
    db.session.commit()
