# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
launch_sites = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites = launch_sites['Launch Site']

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All sites', 'value': 'All sites'}, 
                                        {'label': launch_sites[0], 'value': launch_sites[0]}, 
                                        {'label': launch_sites[1], 'value': launch_sites[1]}, 
                                        {'label': launch_sites[2], 'value': launch_sites[2]}, 
                                        {'label': launch_sites[3], 'value': launch_sites[3]}, 
                                    ],
                                    value='All',
                                    placeholder='Select a launch site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min = 0.,
                                    max = 10000.,
                                    step = 1000.,
                                    marks={
                                        0: '0 kg',
                                        1000: '1000 kg',
                                        2000: '2000 kg',
                                        3000: '3000 kg',
                                        4000: '4000 kg',
                                        5000: '5000 kg',
                                        6000: '6000 kg',
                                        7000: '7000 kg',
                                        8000: '8000 kg',
                                        9000: '9000 kg',
                                        10000: '10000 kg'
                                    },
                                    value = [spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value')
               )
def generate_pie_chart(site):
    if site == 'All sites':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Ratio of successful launches from different sites')
    else:
        df = spacex_df[spacex_df['Launch Site']==site]
        df = df.groupby('class').count().reset_index()
        df.rename(columns={'Launch Site':'class count'}, inplace=True)
        fig = px.pie(df, values='class count', names='class', title='Lauching result for launch site '+site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')]
               )
def generate_scatter_plot(site, payload):
    if site == 'All sites':
        fig = px.scatter(data_frame=spacex_df, x='Payload Mass (kg)', y='class', \
            color="Booster Version Category", range_x=[payload[0], payload[1]], \
            title='correlation between payload mass (kg) and success for all sites')
    else:
        df = spacex_df[spacex_df['Launch Site']==site]
        fig = px.scatter(data_frame=df, x='Payload Mass (kg)', y='class', \
            color="Booster Version Category", range_x=[payload[0], payload[1]],\
            title='correlation between payload mass (kg) and success for site '+site)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
