import os,sys
from flask import render_template,redirect, url_for,request,jsonify
from flask_login import login_required, login_user, logout_user, current_user
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from layouts import layout1
import callbacks
from login import LoginForm,RegisterForm,login_manager,StockForm
from __init__ import server
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from model import create_user,User,editData,getStockValue
from database import getOwnedStocks

from yahoo import getCompanyList,getStockNow
os.chdir("D:/Euler/Projects/Webtesting")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@server.route('/')
def home():
    return render_template('home.html')

@server.route('/friends/')
@login_required
def friends():
    print(os.getcwd())
    os.chdir("D:/Euler/Projects/Webtesting")
    engine = create_engine('sqlite:///stock.db')
    conn = engine.connect()
    data = conn.execute("select * from user")
    return render_template('friends.html',data = data)


@server.route('/dashboard/',methods = ['GET','POST'])
@login_required
def dashboard():
    owned = getOwnedStocks(current_user.username)

    form = StockForm()

    s = getCompanyList()

    stockValue = 0


    return render_template('dashboard.html', name = current_user.username,form = form,money = current_user.money,value = stockValue,owned=owned,choices = s)

@server.route('/process')
@login_required
def process():
    amount = request.args.get('amount')
    amount = float(amount)
    totalCost = 0

    if amount:
        totalCost = amount* float(getStockNow(request.args.get('company')))


    return render_template('process.html', string=round(totalCost,2))

@server.route('/buyStock')
@login_required
def buyStock():
    text = request.args.get('button')
    buyBoolean = False
    if text =="buy":
        buyBoolean = True
    #print()
    try:
        company = request.args.get('company')
        amount = request.args.get('amount')
        amount = float(amount)
        editData(current_user.username,company ,amount,buyBoolean)
        return render_template('buyStock.html',owned = getOwnedStocks(current_user.username),money = current_user.money)

    except:
        return render_template('buyStock.html',owned = getOwnedStocks(current_user.username),money = current_user.money)

@server.route('/settings/')
@login_required
def settings():
    return render_template('settings.html')
@server.route('/signup/', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data,form.password.data)
        return redirect(url_for('home'))
    return render_template('signup.html',form=form)
@server.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():


        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user,  remember = form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>'+ user.pw_hash+'</h1>'
    return render_template('login.html',form = form)
@server.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))




app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)





app.layout = layout1



@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    return callbacks.update_graph(selected_dropdown_value)#calls callback for dash app

if __name__ == '__main__':
    app.run_server(debug=True)
