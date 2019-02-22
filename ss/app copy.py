# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
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


y = 2005
df = dfALL[(dfALL.co2.notnull()) & (dfALL.renew_typ=='Renewable energies')]

# df = df[(df.year==y) & (df.renew_typ=='Renewable energies')]

# print(df)

available_years = df.year.unique()
available_countries = df.country.unique()


# Dash layout setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id= 'my-id', value='whatever', type='text'),
    html.Div(id='my-div')
    ])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)

def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
    app.scripts.config.serve_locally=True

