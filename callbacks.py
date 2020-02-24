
import pandas as pd
import os
import plotly.graph_objs as go
from yahoo import getStock
def update_graph(selected_dropdown_value):
    os.chdir("D:/Euler/Projects/Webtesting/python")
    #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')
    df = pd.read_csv('companies.csv',engine='python')

    symbol = df['Symbol'].values.tolist()
    comp = df['Name'].values.tolist()

    dropdown = {}
    for i in range(0,len(symbol)):
        dropdown[symbol[i]]=comp[i]


    trace1 = []
    trace2 = []




    if selected_dropdown_value:
        for stock in selected_dropdown_value:
            trace1.append(go.Scatter(x=getStock(stock)[0],y=getStock(stock)[1],mode='lines',
                opacity=0.7,name=f'Open {dropdown[stock]}',textposition='bottom center'))
            trace2.append(go.Scatter(x=getStock(stock)[0],y=getStock(stock)[2],mode='lines',
                opacity=0.6,name=f'Close {dropdown[stock]}',textposition='bottom center'))
        traces = [trace1, trace2]
        data = [val for sublist in traces for val in sublist]
        figure = {'data': data,
            'layout': go.Layout(template='plotly_dark',colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                height=600,title=f"Opening and Closing Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
                xaxis={"title":"Date",
                       'rangeselector': dict(bgcolor = 'rgb(50,50,50)', buttons= list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                          {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                                          {'count': 1, 'label': '1Y', 'step': 'year', 'stepmode': 'backward'},
                                                          {'count': 5, 'label': '5Y', 'step': 'year', 'stepmode': 'backward'},
                                                          {'step': 'all'}])),
                       'rangeslider': {'visible': False}, 'type': 'date'},yaxis={"title":"Price (USD)"})}
        return figure
    else:
        return {'data': None,
            'layout': go.Layout(template="plotly_dark",colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                height=600,title=f"Opening and Closing Prices ",
                xaxis={"title":"Date",
                       'rangeselector' : dict(bgcolor = 'rgb(50, 50, 50)', buttons= list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                          {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                                          {'count': 1, 'label': '1Y', 'step': 'year', 'stepmode': 'backward'},
                                                          {'count': 5, 'label': '5Y', 'step': 'year', 'stepmode': 'backward'},
                                                          {'step': 'all'}])),
                       'rangeslider': {'visible': False}, 'type': 'date'},yaxis={"title":"Price (USD)"})}
