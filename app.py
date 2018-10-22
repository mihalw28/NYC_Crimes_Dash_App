import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
from flask_cors import CORS
import pandas as pd
import numpy as np
import os


external_scripts = [
    'https://raw.githubusercontent.com/mihalw28/NYC_Crimes_Dash_App/Start_app/assets/gtag.js'
]


app = dash.Dash('CrimesApp',
                external_scripts=external_scripts)
server = app.server

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://raw.githubusercontent.com/mihalw28/NYC_Crimes_Dash_App/Start_app/assets/gtag.js'
    })


mapbox_access_token = 'pk.eyJ1IjoibWloYWx3MjgiLCJhIjoiY2psejZqZThnMXRndDNxcDFpdWh6YnV2NCJ9.IGbFZyg0dcy61geuwJUByw'


def initialize():
    df = pd.read_csv('https://s3.eu-central-1.amazonaws.com/nyc-crimes-data-app/crimes_app_data.csv')
    df.drop('Unnamed: 0', 1, inplace=True)
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%Y-%m-%d %H:%M:%S')
    df.index = df['Date/Time']
    df.drop('Date/Time', 1, inplace=True)
    totalList = []
    for month in df.groupby(df.index.month):
        dailyList = []
        for weekday in month[1].groupby(month[1].index.weekday):
            dailyList.append(weekday[1])
        totalList.append(dailyList)
    return np.array(totalList)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.P(id='total-rides', className="totalRides"),
            html.P(id='total-rides-selection', className="totalRideSelection"),
            html.P(id='date-value', className="dateValue"),
            dcc.Dropdown(
                id='my-dropdown',
                options=[
                    {'label': 'January', 'value': 'Jan'},
                    {'label': 'February', 'value': 'Feb'},
                    {'label': 'March', 'value': 'Mar'}
                ],
                placeholder="Month:",
                className="two columns"
            ),
            dcc.Dropdown(
                id='race-dropdown',
                options=[
                    {'label': 'Black', 'value': 'Bl'},
                    {'label': 'White Hispanic', 'value': 'Whh'},
                    {'label': 'White', 'value': 'Wh'},
                    {'label': 'Asian/Pac. Isl.', 'value': 'As'},
                    {'label': 'Black Hispanic', 'value': 'Blh'},
                    {'label': 'Amer Ind.', 'value': 'Am'},
                ],
                placeholder='Suspector race:',
                className='two columns'
            ),
            dcc.Dropdown(
                id='age-dropdown',
                options=[
                    {'label': '<18', 'value': 'u18'},
                    {'label': '18-24', 'value': 'u24'},
                    {'label': '25-44', 'value': 'u44'},
                    {'label': '45-64', 'value': 'u64'},
                    {'label': '65+', 'value': 'a65'},
                ],
                placeholder='Suspector age:',
                className='two columns'
            ),
            dcc.Dropdown(
                id='sex-dropdown',
                options=[
                    {'label': 'Female', 'value': 'f'},
                    {'label': 'Male', 'value': 'm'},
                ],
                placeholder='Suspector sex:',
                className='two columns'
            ),
            html.Div([
                html.Div([
                    html.H2("Dash - Crimes in NYC", style = {'font-family': 'Dosis'}),
                ]),
                html.P('Select different months and features of suspectors using \
                        dropdowns and different days using the slider below or \
                        by selecting different time frames on the histogram.',
                    className="explanationParagraph twelve columns"),
                dcc.Graph(id='map-graph'),
            ]),
            html.Div([  
                    dcc.Graph(id='pie_graph'),
                ], className = 'pie bottom three columns'),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='bar-selector',
                        options=[
                            {'label': '0:00', 'value': '0'},
                            {'label': '1:00', 'value': '1'},
                            {'label': '2:00', 'value': '2'},
                            {'label': '3:00', 'value': '3'},
                            {'label': '4:00', 'value': '4'},
                            {'label': '5:00', 'value': '5'},
                            {'label': '6:00', 'value': '6'},
                            {'label': '7:00', 'value': '7'},
                            {'label': '8:00', 'value': '8'},
                            {'label': '9:00', 'value': '9'},
                            {'label': '10:00', 'value': '10'},
                            {'label': '11:00', 'value': '11'},
                            {'label': '12:00', 'value': '12'},
                            {'label': '13:00', 'value': '13'},
                            {'label': '14:00', 'value': '14'},
                            {'label': '15:00', 'value': '15'},
                            {'label': '16:00', 'value': '16'},
                            {'label': '17:00', 'value': '17'},
                            {'label': '18:00', 'value': '18'},
                            {'label': '19:00', 'value': '19'},
                            {'label': '20:00', 'value': '20'},
                            {'label': '21:00', 'value': '21'},
                            {'label': '22:00', 'value': '22'},
                            {'label': '23:00', 'value': '23'}
                        ],
                        multi=True,
                        placeholder="Select certain hours using \
                                    the box-select/lasso tool or \
                                    using the dropdown menu",
                    ),
                    dcc.Graph(id="histogram", className='histogramGraph'),
                    html.P("", id="popupAnnotation", className="popupAnnotation"),
                    dcc.Slider(
                        id="my-slider",
                        min=0,
                        max=6,
                        marks={
                            0: {'label': 'Mondays'},
                            1: {'label': 'Tuesdays'},
                            2: {'label': 'Wednesdays'},
                            3: {'label': 'Thursdays'},
                            4: {'label': 'Fridays'},
                            5: {'label': 'Saturdays'},
                            6: {'label': 'Sundays'}
                        },
                        step=1,
                        included=False,
                        value=0,
                    className='mySlider'),
                ], className = 'bottom twelve columns'),
            ], style={'margin': 'auto 0 auto'},
            className='row'),
            dcc.Checklist(
                id="mapControls",
                options=[
                    {'label': 'Lock Camera', 'value': 'lock'}
                ],
                values=[''],
                labelClassName="mapControls",
                inputStyle={"z-index": "1"}
            ),
        ], className="graphSlider ten columns offset-by-one"),
    ])
], style={"backgroundColor": "rgb(0, 0, 0)"})


def getValue(value):
    val = {
        'Jan': 6,
        'Feb': 6,
        'Mar': 6
    }[value]
    return val


def getIndex(value):
    if (value==None):
        return 0
    val = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2
    }[value]
    return val


def getRace(value): 
    if (value==None):
        return 'BLACK'
    val = {
        'Bl': 'BLACK',
        'Whh': 'WHITE HISPANIC',
        'Wh': 'WHITE',
        'As': 'ASIAN/PAC.ISL',
        'Blh': 'BLACK HISPANIC',
        'Am': 'AMER IND',
    }[value]
    return val


def getAge(value):
    if (value==None):
        return '18-24'
    val = {
        'u18': '<18',
        'u24': '18-24',
        'u44': '25-44',
        'u64': '45-64',
        'a65': '65+', 
    }[value]
    return val


def getSex(value):
    if (value==None):
        return 'M'
    val = {
        'f': 'F',
        'm': 'M',
    }[value]
    return val


def getTickLabel(value):
    val = {
        0: 'Mondays',
        1: 'Tuesdays',
        2: 'Wednesdays',
        3: 'Thursdays',
        4: 'Fridays',
        5: 'Saturdays',
        6: 'Sundays'
    }[value]
    return val


def getClickIndex(value):
    if (value==None):
        return 0
    return value['points'][0]['x']



# dropdown selector ->  selected
@app.callback(Output("bar-selector", "value"),
              [Input("histogram", "selectedData")])
def update_bar_selector(value):
    holder = []
    if (value is None or len(value) is 0):
        return holder
    for x in value['points']:
        holder.append(str(int(x['x'])))
    return holder


# total number
@app.callback(Output("total-rides", "children"),
              [Input("my-dropdown", "value"), 
               Input('my-slider', 'value')])
def update_total_rides(value, slider_value):
    return ("Total # of incidents: {:,d}"
            .format(len(totalList[getIndex(value)][slider_value])))


# dropdowns + slider -> # of selected crimes from selected month 
@app.callback(Output('total-rides-selection', 'children'),
              [Input('my-dropdown', 'value'), 
               Input('my-slider', 'value'),
               Input('bar-selector', 'value'),
               Input('race-dropdown', 'value'),
               Input('age-dropdown', 'value'),
               Input('sex-dropdown', 'value')])
def update_total_rides_selection(value, slider_value, selection,
                                 race_value, age_value, sex_value):
    if (selection is None or len(selection) is 0):
        return ""
    totalInSelction = 0
    for x in selection:
        totalInSelction += len(totalList[getIndex(value)][slider_value]
                               [(totalList[getIndex(value)][slider_value].index.hour == int(x)) 
                              & (totalList[getIndex(value)][slider_value].SUSP_RACE == getRace(race_value))
                              & (totalList[getIndex(value)][slider_value].SUSP_AGE_GROUP == getAge(age_value))
                              & (totalList[getIndex(value)][slider_value].SUSP_SEX == getSex(sex_value))])
    return ('Total incidents in selection: {:,d}'
            .format(totalInSelction))                                     

# dropdown + slider -> selected day and hours
@app.callback(Output('date-value', 'children'),
              [Input('my-dropdown', 'value'), 
               Input('my-slider', 'value'),
               Input('bar-selector', 'value')])
def update_date(value, slider_value, selection):
    holder = []
    
    if (value is None or selection is None or len(selection) is 24
        or len(selection) is 0):
        return (value, ' {}'.format(getTickLabel(slider_value)), ' - showing: All')

    for x in selection:
        holder.append(int(x))
    holder.sort()

    if (holder[len(holder)-1]-holder[0]+2 == len(holder)+1 and len(holder) > 2):
        return (value, ' {}'.format(getTickLabel(slider_value)), ' - showing hour(s): ',
                holder[0], '-', holder[len(holder)-1])

    x = ''
    for h in holder:
        if (holder.index(h) == (len(holder)-1)):
            x += str(h)
        else:
            x += str(h) + ', '
    return (value, ' {}'.format(getTickLabel(slider_value)), ' - showing hours(s): ', x)


# pie chart
@app.callback(Output('pie_graph', 'figure'),
                     [Input('my-dropdown', 'value'), 
                      Input('my-slider', 'value'),
                      Input('race-dropdown', 'value'),
                      Input('age-dropdown', 'value'),
                      Input('sex-dropdown', 'value')])
def make_pie(value, slider_value, race_value, age_value, sex_value):

    boro_color = {
        'MANHATTAN': '#fae13d',
        'BRONX': '#3ef989',
        'BROOKLYN': '#42c9fa',
        'STATEN ISLAND': '#d14af2',
        'QUEENS': '#de5959'
    }
    
    boros_dict = totalList[getIndex(value)][slider_value].BORO_NM[
                        (totalList[getIndex(value)][slider_value].SUSP_RACE == getRace(race_value))
                      & (totalList[getIndex(value)][slider_value].SUSP_AGE_GROUP == getAge(age_value))
                      & (totalList[getIndex(value)][slider_value].SUSP_SEX == getSex(sex_value))].value_counts().to_dict()

    labels = list(boros_dict.keys())
    values = list(boros_dict.values())
    
    def getBorosColors(value):
        colors = []
        for label in labels:
            colors.append(boro_color.get(label))
        return colors

    figure=go.Figure(
        data=[
            go.Pie(
                labels = labels,
                values = values,
                hoverinfo='label',
                hole=0.4,
                direction='clockwise',
                textfont=dict(
                    color='rgb(255, 255, 255)',
                    size=12
                ),
                marker=dict(
                    colors = getBorosColors(labels),
                    line=dict(
                        color='rgb(0, 0, 0)',
                        width=1.2,
                    ),
                ),
                opacity=0.8
            ),
        ], 
        layout=go.Layout(
            title='Incidents in boroughs on {}'.format(getTickLabel(slider_value)),
            titlefont=dict(
                size=13,
                color='rgb(255, 255, 255)',
            ),
            showlegend=False,
            height=285,
            margin=dict(l=15, r=50, t=50, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        ),
    )
    return figure

# just clean
@app.callback(Output('histogram', 'selectedData'),
              [Input('my-dropdown', 'value')])
def clear_selection(value):
    if (value is None or len(value) is 0):
        return None

# bar selector -> annotation
@app.callback(Output('popupAnnotation', 'children'),
              [Input('bar-selector', 'value')])
def clear_selection1(value):
    if (value is None or len(value) is 0):
        return 'Select any of the bars to section data by time'
    else:
        return ''

# bar colors
def get_selection(value, slider_value, selection, race_value, age_value, sex_value):
    xVal = []
    yVal = []
    xSelected = []

    colorVal = ['#440154','#470f61','#481d6e','#482a79','#453681','#424386',
                '#3d4e8a','#375b8c','#32668d','#2d718e','#297b8e','#25868d',
                '#21928c','#209b89','#23a685','#2cb17e','#3bba75','#51c46a',
                '#69cd5c','#86d44b','#a4da38','#c3df25','#e0e31b','#fde725']

    if (selection is not None):
        for x in selection:
            xSelected.append(int(x))
    for i in range(0, 24):
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = ('#ffffff')
        xVal.append(i)
        yVal.append(len(totalList[getIndex(value)][slider_value] \
                    [(totalList[getIndex(value)][slider_value].index.hour == i) \
                    & (totalList[getIndex(value)][slider_value].SUSP_RACE == getRace(race_value)) \
                    & (totalList[getIndex(value)][slider_value].SUSP_AGE_GROUP == getAge(age_value)) \
                    & (totalList[getIndex(value)][slider_value].SUSP_SEX == getSex(sex_value))]))

    return [np.array(xVal), np.array(yVal), np.array(xSelected), np.array(colorVal)]


# dropdowns + slider - > updated histogram
@app.callback(Output('histogram', 'figure'),
              [Input('my-dropdown', 'value'), Input('my-slider', 'value'),
               Input('bar-selector', 'value'), Input('race-dropdown', 'value'),
               Input('age-dropdown', 'value'), Input('sex-dropdown', 'value')])
def update_histogram(value, slider_value, selection, race_value, age_value, sex_value):

    [xVal, yVal, xSelected, colorVal] = get_selection(value, slider_value, selection, race_value, age_value, sex_value)

    layout = go.Layout(
        bargap=0,
        bargroupgap=0,
        barmode='group',
        margin=dict(l=0, r=0, t=0, b=23),
        showlegend=False,
        plot_bgcolor='#515d58',
        paper_bgcolor='rgb(66, 134, 244, 0)',
        height=250,
        dragmode='select',
        xaxis=dict(
            range=[-0.5, 23.5],
            showticklabels=True,
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=':00',
            tickfont=dict(
                color='black'
            ),
        ),
        yaxis=dict(
            range=[0, max(yVal)+max(yVal)/4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode='nonnegative',
            zeroline=False            
        ),
        annotations=[
            dict(x=xi, y=yi,
                 text=str(yi),
                 xanchor='center',
                 yanchor='bottom',
                 showarrow=False,
                 font=dict(
                    color='white'
                 ),
                 ) for xi, yi in zip(xVal, yVal)],
    )

    return go.Figure(
           data=[
                go.Bar(
                    x=xVal,
                    y=yVal,
                    marker=dict(
                        color=colorVal,
                        line=dict(
                            color='rgb(0, 0, 0)',
                            width=1.2
                        )
                    ),
                    hoverinfo="x"
                ),
            ], layout=layout)

# color scatter points on map
def get_lat_lon_color(selectedData, value, slider_value, race_value, age_value, sex_value):
    listStr = 'totalList[getIndex(value)][slider_value]\
               [(totalList[getIndex(value)][slider_value].SUSP_RACE == getRace(race_value)) & \
                (totalList[getIndex(value)][slider_value].SUSP_AGE_GROUP == getAge(age_value)) & \
                (totalList[getIndex(value)][slider_value].SUSP_SEX == getSex(sex_value))]'
    if (selectedData is None or len(selectedData) is 0):
        return listStr
    elif (int(selectedData[len(selectedData) - 1]) - int(selectedData[0]) + 2 == len(selectedData) + 1 and len(selectedData) > 2):
        listStr = 'totalList[getIndex(value)][slider_value]\
                   [(totalList[getIndex(value)][slider_value].SUSP_RACE == getRace(race_value)) & \
                    (totalList[getIndex(value)][slider_value].SUSP_AGE_GROUP == getAge(age_value)) & \
                    (totalList[getIndex(value)][slider_value].SUSP_SEX == getSex(sex_value)) & \
                    (totalList[getIndex(value)][slider_value].index.hour >=' +  str(int(selectedData[0])) + ') & \
                    (totalList[getIndex(value)][slider_value].index.hour <=' + str(int(selectedData[len(selectedData)-1])) + ')]'
    else:
        listStr = 'totalList[getIndex(value)][slider_value]\
                   [(totalList[getIndex(value)][slider_value].SUSP_RACE == getRace(race_value)) & \
                    (totalList[getIndex(value)][slider_value].SUSP_AGE_GROUP == getAge(age_value)) & \
                    (totalList[getIndex(value)][slider_value].SUSP_SEX == getSex(sex_value)) & ('
        for point in selectedData:
            if (selectedData.index(point) is not len(selectedData) - 1):
                listStr += '(totalList[getIndex(value)][slider_value].index.hour == ' + str(int(point)) + ') | '
            else:
                listStr += '(totalList[getIndex(value)][slider_value].index.hour == ' + str(int(point)) + '))]'
    return listStr

# update map
@app.callback(Output('map-graph', 'figure'),
              [Input('my-dropdown', 'value'), Input('my-slider', 'value'),
              Input('bar-selector', 'value'), Input('race-dropdown', 'value'),
              Input('age-dropdown', 'value'), Input('sex-dropdown', 'value')],
              [State('map-graph', 'relayoutData'),
               State('mapControls', 'values')])
def update_graph(value, slider_value, selectedData, race_value, age_value, sex_value, prevLayout, mapControls):
    zoom = 10.0
    latInitial = 40.727044
    lonInitial = -73.920119
    bearing = 0

    listStr = get_lat_lon_color(selectedData, value, slider_value, race_value, age_value, sex_value)

    if (prevLayout is not None and mapControls is not None and 'lock' in mapControls):
        zoom = float(prevLayout['mapbox']['zoom'])
        latInitial = float(prevLayout['mapbox']['center']['Latitude'])
        lonInitial = float(prevLayout['mapbox']['center']['Longitude'])
        bearing = float(prevLayout['mapbox']['bearing'])
    return go.Figure(
        data=[
            go.Scattermapbox(
                lat=round(eval(listStr)['Latitude'], 4),
                lon=round(eval(listStr)['Longitude'], 4),
                mode='markers',
                hoverinfo='lat+lon+text',
                text=eval(listStr).index.hour,
                marker = dict(
                    color=np.append(np.insert(eval(listStr).index.hour, 0, 0), 23),
                    colorscale='Viridis',
                    reversescale=False,
                    opacity=0.8,
                    size=7,
                    colorbar=dict(
                        thicknessmode='fraction',
                        title='Time of<br>Day',
                        x=0.935,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(
                            color='white'
                        ),
                        titlefont=dict(
                            color='white'
                        ),
                        titleside='top'
                    )
                ),
            ),
            go.Scattermapbox(
                lat=['40.781', '40.857', '40.659', '40.585', '40.716'],
                lon=['-73.974', '-73.898', '-73.957', '-74.165', '-73.827'],
                mode='markers',
                hoverinfo='text',
                text=['Manhattan', 'Bronx', 'Brooklyn', 'Staten Island', 'Queens'],
                opacity=0.1,
                marker=dict(
                    size=6,
                    color='#ffa0a0',
                ),
            ),
        ],
        layout=go.Layout(
            autosize=True,
            height=750,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial,
                    lon=lonInitial
                ),
                style='mapbox://styles/mihalw28/cjneeuqo61t8l2rnnv8iruvgn',
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                'mapbox.zoom': 10,
                                'mapbox.center.lon': '-73.991251',
                                'mapbox.center.lat': '40.7272',
                                'mapbox.bearing': 0, 
                                'mapbox.style': 'mapbox://styles/mihalw28/cjneeuqo61t8l2rnnv8iruvgn'
                            }],
                            label='Reset Zoom',
                            method='relayout'
                        )
                    ]),
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    type='buttons',
                    x=0.45,
                    xanchor='left',
                    yanchor='bottom',
                    bgcolor='#323130',
                    borderwidth=1,
                    bordercolor='#6d6d6d',
                    font=dict(
                        color='#FFFFFF'
                    ),
                    y=0.02
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                'mapbox.zoom': 11.5,
                                'mapbox.center.lon': '-73.974',
                                'mapbox.center.lat': '40.781',
                                'mapbox.bearing': 0,
                                'mapbox.style': 'mapbox://styles/mihalw28/cjneeuqo61t8l2rnnv8iruvgn'
                                }],
                            label='Manhattan',
                            method='relayout'
                        ),  
                    ]),
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    bordercolor='#fae13d',
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#fae13d"
                    ),
                    x=0.007,
                    y=0.57, 
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                'mapbox.zoom': 11.5,
                                'mapbox.center.lon': '-73.898',
                                'mapbox.center.lat': '40.857',
                                'mapbox.bearing': 0,
                                'mapbox.style': 'mapbox://styles/mihalw28/cjneeuqo61t8l2rnnv8iruvgn'
                                }],
                            label='Bronx',
                            method='relayout'
                        ),  
                    ]),
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    bordercolor='#3ef989',
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#3ef989"
                    ),
                    x=0.007,
                    y=0.52
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                'mapbox.zoom': 11.5,
                                'mapbox.center.lon': '-73.957',
                                'mapbox.center.lat': '40.659',
                                'mapbox.bearing': 0,
                                'mapbox.style': 'mapbox://styles/mihalw28/cjneeuqo61t8l2rnnv8iruvgn'
                                }],
                            label='Brooklyn',
                            method='relayout'
                        ),  
                    ]),
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    bordercolor='#42c9fa',
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#42c9fa"
                    ),
                    x=0.007,
                    y=0.47
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                'mapbox.zoom': 11.5,
                                'mapbox.center.lon': '-74.165',
                                'mapbox.center.lat': '40.585',
                                'mapbox.bearing': 0,
                                'mapbox.style': 'mapbox://styles/mihalw28/cjneeuqo61t8l2rnnv8iruvgn'
                                }],
                            label='Staten Island',
                            method='relayout'
                        ),  
                    ]),
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    bordercolor='#d14af2',
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#d14af2"
                    ),
                    x=0.007,
                    y=0.42
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                'mapbox.zoom': 11.5,
                                'mapbox.center.lon': '-73.827',
                                'mapbox.center.lat': '40.716',
                                'mapbox.bearing': 0,
                                'mapbox.style': 'mapbox://styles/mihalw28/cjneeuqo61t8l2rnnv8iruvgn'
                                }],
                            label='Queens',
                            method='relayout'
                        ),  
                    ]),
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    bordercolor='#de5959',
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#de5959"
                    ),
                    x=0.007,
                    y=0.37
                ),
            ]
        )
    )


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]


for css in external_css:
    app.css.append_css({"external_url": css})





@app.server.before_first_request
def defineTotalList():
    global totalList
    totalList = initialize()


if __name__ == '__main__':
    app.run_server(debug=True)
