
#from model import User

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SelectField,DecimalField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from __init__ import server
import pandas as pd

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'




class LoginForm(FlaskForm):
    username = StringField('username', validators = [InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password',validators = [InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email(message = 'Invalid email')])
    username = StringField('username', validators = [InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password',validators = [InputRequired(), Length(min=8, max=80)])
class StockForm(FlaskForm):
    df = pd.read_csv('companies.csv',engine='python')
    symbol = df['Symbol'].values.tolist()
    comp = df['Name'].values.tolist()
    s = tuple(zip(symbol,comp))
    stockName = SelectField('Stock',choices=s)
    stockAmount = DecimalField('Amount',places=2)
