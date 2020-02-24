import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
os.chdir("D:/Euler/Projects/Webtesting/python")
df = pd.read_csv('companies.csv',engine='python')

symbol = df['Symbol'].values.tolist()
comp = df['Name'].values.tolist()
arr = []
for i in range(0,len(symbol)):
    drop = {}
    drop["label"]= comp[i]
    drop["value"] = symbol[i]
    arr.append(drop)

layout1 = html.Div([
    dcc.Dropdown(id='my-dropdown',options=arr,
        multi=True,style={'fontColor':'white','color':'white','backgroundColor':'black',"display": "block","margin-left": "auto","margin-right": "auto","width": "100%"}),
        html.Br(),
    dcc.Graph(id='my-graph',config={
        'displayModeBar': False
    })
], className="container")
