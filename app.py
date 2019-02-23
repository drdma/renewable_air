import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc     #ASI package
from dash.dependencies import Input, Output
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os

path1 = os.path.expanduser('~/Dropbox/Programming/Python/Climate change/data/EU_RenewableEng_Prod_05-16.csv')
df1 = pd.read_csv(path1)

path2 = os.path.expanduser('~/Dropbox/Programming/Python/Climate change/data/CO2Emm_Global_1970-16.csv')
df2 = pd.read_csv(path2)

# Merge 2 dataframes: renewable energy generation and CO2 emissions of EU countries
dfALL = pd.merge(df1, df2, how='left', left_on=['Country', 'Year'], right_on=['ISO_NAME', 'Year'])

# drop repeated and useless columns
dfALL = dfALL.drop(['Units', 'Indicator', 'ISO_CODE', 'ISO_NAME'], axis=1)

dfALL.rename(columns={'Year':'year',
                  'Country':'country',
                  'Product':'renew_typ',
                  'Value':'renew_ene',
                  'GHG per capita emissions':'ghg',
                  'CO2/cap':'co2'}, inplace='True')

# Convert renewable energy column from object type to numeric, and set invalid entries to NaN
dfALL['renew_ene'] = pd.to_numeric(dfALL.renew_ene, errors='coerce')

# some countries do not have co2 entries, use known countries only (for training)
df = dfALL[dfALL.co2.notnull()]

available_years = df.year.unique()
available_countries = df.country.unique()
available_renewtypes = df.renew_typ.unique()

# remove 'Renewable energies' entry (convert to list first)
available_renewtypes = available_renewtypes.tolist()
available_renewtypes.remove('Renewable energies')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501


def row(children):
    return html.Div(children, className='row')




app.layout = html.Div([
    
    dbc.Row([
        #header
        html.H1(
            children = 'Can renewable energy reduce carbon emissions?',
            className='nine columns'
            ),
        html.Div(
            children = 'Dora Ma',
            className='three columns'
            ),
    ]),

    #Check boxes for selecting renewable energy or co2 to display on graph
    row([
        #Checkboxes for renewable energy and CO2 for graph
        html.Div([
            dcc.Checklist(
                id = 'checkRC',
                options=[
                    {'label': 'Renewable energy', 'value': 'renewEne'},
                    {'label': 'CO2 emissions', 'value': 'co2'}
                    ],
                values=['renewEne', 'co2']
                )
            ], className='three columns'
        ),

        html.Div([
            #make slider for years
            dcc.Slider(
                id = 'year-slider',
                min = df.year.min(),
                max = df.year.max(),
                value = df.year.min(),
                marks = {str(y): str(y) for y in available_years}
                )], className='nine columns', style={'marginBottom': 40}
            ),

        html.Div([

            #Make graph of all countries vs renewable energy
            dcc.Graph(id = 'all-countries-renewEne'),

            ], className='nine columns'
            )
        ]),
    
    row([
        #Dropdown and textarea for progression graph
        html.Div([
            #Dropdown for countries
            dcc.Dropdown(
                id = 'dropdown-country',
                options = [{'label': i, 'value': i} for i in available_countries],
                value = 'Albania'
                ),
            #text area
            dcc.Textarea(
                placeholder = 'description of country....',
                value = 'This is a textarea',
                style = {'width': '100%'}
                )
            ], className='six columns'
            ),

        #Make text and graph of specific country progression
        html.Div([
            dcc.Graph(id = 'country-progression')
            ], className='six columns'
            )
        ])
])

@app.callback(
        Output('all-countries-renewEne', 'figure'),
        [
            Input('year-slider', 'value'),
            Input('checkRC', 'values')
        ]
        )


def update_figure1(selected_year, RC):
    filtered_df = df[(df.year==selected_year) & (df.renew_typ=='Renewable energies')]

    global renewC, co2C

    if RC==[]:
        renewC = 'rgb(255,255,255)' #white
        co2C = 'rgb(255,255,255)' #white
    elif RC==['renewEne']:
        renewC = 'rgb(102,204,0)' #green
        co2C = 'rgb(255,255,255)' #white
    elif RC==['co2']:
        renewC = 'rgb(255,255,255)' #white
        co2C = 'rgb(160,160,160)' #grey
    elif RC==['renewEne','co2']:
        renewC = 'rgb(102,204,0)' #green
        co2C = 'rgb(160,160,160)' #grey
    elif RC==['co2','renewEne']:
        renewC = 'rgb(102,204,0)' #green
        co2C = 'rgb(160,160,160)' #grey


    trace1= go.Bar(
                x = filtered_df.country,
                y = filtered_df.renew_ene,
                width = 0.4,
                offset = 0,
                marker = dict(
                    color= renewC
                    ),
                name = 'Renewable energy'
            )

    trace2= go.Bar(
                x = filtered_df.country,
                y = filtered_df.co2,
                name = 'co2',
                width = 0.4,
                offset = 0.4,
                marker = dict(
                    color= co2C                   
                    ),
                yaxis='y2'
            )


    return{
            'data': [trace1, trace2],
            'layout': go.Layout(
                yaxis=dict(
                    range=[0, 40000],
                    ),
                yaxis2=dict(
                    range=[0, 25],
                    overlaying= 'y',
                    side='right'
                    )
                )
            }


@app.callback(
        Output('country-progression', 'figure'),
        [Input('dropdown-country', 'value')]
        )

def update_figure2 (selected_country):
    filtered_df = df[df.country == selected_country]

    traces = []
    traces.append(
            go.Scatter(
                x = filtered_df.year,
                y = filtered_df.co2,
                name = 'co2',
                fill = 'tozeroy',
                fillcolor = 'rgba(192, 192, 192, 0.4)',
                mode = 'none',
                yaxis='y2'
                )
            )
    for i in available_renewtypes:
        df_renewtype = filtered_df[filtered_df.renew_typ== i]
        traces.append(
                go.Scatter(
                    x = df_renewtype.year,
                    y = df_renewtype.renew_ene,
                    name = i
                    )
                )


    return{
            'data': traces,
            'layout': go.Layout(
                yaxis2=dict(
                    overlaying = 'y',
                    side = 'right'
                    )
                )
            }




if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
