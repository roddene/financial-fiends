from sqlalchemy import create_engine
from pandas import DataFrame
import yfinance as yf
import pandas as pd
import os
import pathlib
from datetime import datetime,date,timedelta


os.chdir("D:/Euler/Projects/Webtesting/python")
df = pd.read_csv('companies.csv',engine='python')
def getStock(stock):
    stock = stock.replace(".","-")

    return updateData(stock,path)


def updateAll(stocks,start,end):
    i=0
    for stock in stocks:
        i+=1
        print(i)
        pushHistory(stock,start,end,'replace')


def pushHistory(stock,start,end,appendReplace):
    stock = stock.replace(".","-")
    con = create_engine('mysql+mysqldb://root:Supapassword696@localhost:3306/stocks', echo=False)
    try:
        df = yf.download(stock,start,end)
        df =df.drop(columns = ['High','Low','Adj Close','Volume'])
        df.to_sql(con=con, name=stock.lower(), if_exists=appendReplace)
    except:
        print(stock+ " does not exist")


def getStock(stock):
    upToDate(stock)
    return pullHistory(stock)

def getStockNow(stock):

    stock = stock.replace(".","-")
    try:
        print("dowloading stock now")
        df = yf.download(stock,datetime.today().strftime('%Y-%m-%d'))
        print("got stock")
        return df.iloc[0][3]
    except:
        print(stock+ " does not exist")

def pullHistory(stock):

    stock = stock.replace(".","-")
    con = create_engine('mysql+mysqldb://root:Supapassword696@localhost:3306/stocks', echo=False)
    return DataFrame(con.execute('SELECT * FROM '+stock.lower()).fetchall())


df = pd.read_csv('companies.csv',engine='python')
#




#print(df.iloc[0,0])
#updateAll(df['Symbol'].tolist(),"1970-01-01",datetime.today().strftime('%Y-%m-%d'))
#pushHistory("AAPL","1970-01-01",datetime.today().strftime('%Y-%m-%d'),'replace')
#print(pullHistory("AAPL"))

from bdateutil import isbday
import holidays
def recentbday(date):#most recent business day that is not today
    date -=timedelta(1)
    while not isbday(date,holidays=holidays.US()):
        date -=timedelta(1)
    return date.strftime('%Y-%m-%d')

def upToDate(stock):
    data = pullHistory(stock)
    if data.iloc[len(data)-1,0].strftime('%Y-%m-%d') == recentbday(datetime.today()+timedelta(2)):
        return True
    else:
        print("cool")
        pushHistory(stock,(data.iloc[len(data)-1,0]+timedelta(1)).strftime('%Y-%m-%d'),recentbday(datetime.today()),'append')

def getCompanyList():
    os.chdir("D:/Euler/Projects/Webtesting/python")
    df = pd.read_csv('companies.csv',engine='python')
    symbol = df['Symbol'].values.tolist()
    comp = df['Name'].values.tolist()
    return zip(symbol,comp)
#df = yf.download("AAPL",start = data.iloc[len(data)-1,0].strftime('%Y-%m-%d'),end = recentbday(datetime.today()))


#upToDate("AAPL")
#print(pullHistory("AAPL"))
print(getStockNow('MMM'))
