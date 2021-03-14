from typing import Union
from typing import Dict
import pandas as pd
import requests
import json
import os
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas import Series, DataFrame

# ------------------------------------------------------------------------------
# Start app add Bootstraps Theme


app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# ------------------------------------------------------------------------------
# Import and clean data (importing  csv into pandas)

df = pd.read_csv('American_Bear.csv')

# Create string out of location

df2 = df['Location'].str.replace('near', '')

# Split columns into City and State

df2 =df2.str.split(',', expand=True)
df2.rename(columns={0: 'City',
                        1:'State'},
               inplace=True, errors='raise')

# Concat City and Stat

df_col2: Union[DataFrame, Series] = pd.concat([df, df2], axis = 1)

#----------------------------------------------------------------

# See if there are any Nans


#print(df_col2[df_col2['State'].isna()])

#--------------------------------

df_col2.iloc[92, df_col2.columns.get_loc('State')] = 'Wyoming'
df_col2.iloc[100, df_col2.columns.get_loc('State')] = 'New York'

#------------------------------------------------------------------
#API Call and get the lat. and long values

for i, row in df_col2.iterrows():
        apiAddress = str(df_col2.at[i, 'City']) + str(df_col2.at[i, 'State'])

        parameters: Dict[str, str] = {
            'key': os.environ.get('API_KEY'),
            'location': apiAddress
            }

        response = requests.get('http://www.mapquestapi.com/geocoding/v1/batch', params=parameters)
    # print(response.text)

        data = json.loads(response.text)['results']

# Get the Lat and Lng of all the bear attacks

        lat = data[0]['locations'][0]['latLng']['lat']
        lng = data[0]['locations'][0]['latLng']['lng']

        df_col2.at[i, 'lat'] = lat
        df_col2.at[i, 'lng'] = lng

# save data to CSV

df_col2.to_csv('Bear_Go')

#------------------------------------------------------------------

app.layout = html.Div([
        html.H1("Bear Attack Dashboard", style={'text-align': 'center'}),

        html.P(
        "The following is a dashboard showcasing bear attacks in the United States.  Bears are extremely dangerous.  They can run up to 35 mph weigh, climb, swim and open car doors.  Large bears can survive multiple rounds from a fire arm.  If a bear wants to kill you, they will and there is almost nothing you can do about it. I created this dashboard to bring awareness to the problem.The map displays all human deaths from bears in the past one years. Use the dropdown menu to select the type of bear. "),
        html.Br(),

        dcc.Dropdown(id='Slct_bear',
                     options=[
                         {'label': 'Polar Bear', 'value': 'Polar Bear'},
                         {'label': 'Black Bear', 'value': 'Black bear'},
                         {'label': 'Brown Bear', 'value': 'Brown bear'},
                         ],
                        value='Polar Bear',
                        multi=False,
                        style={'width': "40%"},
                        clearable=False),

#-------------------------------------------------------------------------
#html layout of the page

        html.Br(),
        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='bear_graph', figure={}),
        html.Br()
    ])

#------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='bear_graph', component_property= 'figure')],
     [Input(component_id='Slct_bear', component_property='value')]

)

def update_graph(Slct_bear):
    container = "The bear selected by the use was: {}".format(Slct_bear)

    dff = df_col2
    dff = dff[dff['Type of bear'] == Slct_bear]

    #Plotly Express
    fig = px.scatter_mapbox(dff, lat='lat', lon='lng', hover_name='City', zoom=3,
                            height=500)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={'r':10,'t':10, 'l':10, 'b':10})
    fig.show()

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=False)


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.




# See PyCharm help at https://www.jetbrains.com/help/pycharm/

