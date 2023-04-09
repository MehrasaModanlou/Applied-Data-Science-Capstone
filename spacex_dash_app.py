


# Import required libraries
import pandas as pd
import dash
# import dash_html_components as html  # deprecated
from dash import html
# import dash_core_components as dcc  # deprecated
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    # dcc.Dropdown(id='site-dropdown',...)
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'Cape Canaveral Launch Complex 40 (CAFS LC-40)', 'value': 'CCAFS LC-40'},
            {'label': 'Cape Canaveral Space Launch Complex 40 (CCAFS SLC-40)', 'value': 'CCAFS SLC-40'},
            {'label': 'Kennedy Space Center Launch Complex 39A (KSC LC-39A)', 'value': 'KSC LC-39A'},
            {'label': 'Vandenberg Air Force Base Space Launch Complex (VAFB SLC-4E)', 'value': 'VAFB SLC-4E'}],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    # dcc.RangeSlider(id='payload-slider',...)

    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    # marks={0: '0', 100: '100'},
                    value=[min_payload, max_payload]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Place to add @app.callback Decorator
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        return px.pie(filtered_df, 
                      values='class',
                      names='Launch Site',
                      title='Launch Success Rate For All Sites')
    # return the outcomes in pie chart for a selected site
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
    return px.pie(filtered_df,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]    
    if entered_site=='ALL':
        return px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
    else:
        return px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Success count on Payload mass for site {entered_site}")


# Run the app
if __name__ == '__main__':
    app.run_server()

# Finding Insights Visually
# Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data, and answer the following questions:
#
# Which site has the largest successful launches? KSC LC-39A
# Which site has the highest launch success rate? KSC LC-39A (success rate 76.9%)
# Which payload range(s) has the highest launch success rate? 2000-4000
# Which payload range(s) has the lowest launch success rate? 6000-8000
# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
# launch success rate? FT (15 successes, 8 failures)