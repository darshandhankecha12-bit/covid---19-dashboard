import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html,dcc
from dash.html import Output
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc

app = dash.Dash(
   __name__,
   external_stylesheets=[dbc.themes.BOOTSTRAP])

external_stylesheet = [
    {
        'href':'jetbrains://pycharm/navigate/reference?project=covid-%2019_dashboard&path=assets%2Fstyle.css',
        'rel':'stylesheets',
        'integrity':'',
        'cross origin':'anonymous',
    }
]

patients = pd.read_csv('IndividualDetails.csv')

total = patients.shape[0]
active = patients[patients['current_status']=='Hospitalized'].shape[0]
recovered = patients[patients['current_status']=='Recovered'].shape[0]
deaths = patients[patients['current_status']=='Deceased'].shape[0]

options = [
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value':'Hospitalized'},
    {'label':'Recovered', 'value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'}
]

#app = dash.Dash(__name__ , external_stylesheets=external_stylesheet)

app.layout = html.Div([
    html.H1("COVID VIRUS  COVID-19 PANDEMIC",style = {'color':'white','text-align':'center'}),


html.Div(className = 'row mb-4',children=[

        html.Div(className ='col-md-3',children=[
            html.Div(className='card bg-danger text -white mb-3',children=[
                html.Div(className='card-body',children=[
                    html.H2("Total Cases"),
                    html.H3(total),
                    ],)
                ],),
            ],),

        html.Div(className ='col-md-3',children=[
            html.Div(className='card bg-info',children=[
                html.Div(className='card-body',children=[
                    html.H2("Active Cases"),
                    html.H3(active),
                    ],)
                ],),
            ],),

        html.Div(className ='col-md-3',children=[
            html.Div(className='card bg-success',children=[
                html.Div(className='card-body',children=[
                    html.H2("Recovered Cases"),
                    html.H3(recovered),
                    ],)
                ],),
            ],),

html.Div(className ='col-md-3',children=[
            html.Div(className='card bg-warning',children=[
                html.Div(className='card-body',children=[
                    html.H2("Death Cases"),
                    html.H3(deaths),
                    ],)
                ],),
            ],),

    ],),

    #html.Div([],className = 'row'),

html.Div(className = 'row',children = [
    html.Div(className ='col-md-12',children=[
        html.Div(className='card',children=[
            html.Div(className= 'card-body',children=[
                dcc.Dropdown(id='picker',options=options,value='All'),
                dcc.Graph(id='bar'),
            ])
        ])
    ])
],),

],className = 'container')

@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(value):
    if value == 'All':
        df = patients
    else:
        df = patients[patients['current_status']==value]

    pbar = df['detected_state'].value_counts().reset_index()
    pbar.columns = ['state','count']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=pbar['state'],
        y=pbar['count'],
    ))

    fig.update_layout(title ='State Total Count')

    return fig

if __name__ == "__main__":
    app.run(debug = True,port=8051)
