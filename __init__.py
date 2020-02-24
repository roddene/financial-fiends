from flask_bootstrap import Bootstrap
from flask import Flask
server = Flask(__name__)
server.config['SECRET_KEY'] = 'Secret'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
Bootstrap(server)
