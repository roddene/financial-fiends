from __init__ import server
from sqlalchemy import func,and_
from flask_sqlalchemy import SQLAlchemy
from model import User,db,StockData
from yahoo import df


def getOwnedStocks(user):
    curUser = User.query.filter_by(username = user).first()
    userStock = StockData.query.filter_by(id=curUser.id).first()
    ownedStock = {}
    for stock in df['Symbol'].values.tolist():
        if not getattr(userStock,stock) == 0:
            ownedStock[stock] = getattr(userStock,stock)
    return ownedStock
