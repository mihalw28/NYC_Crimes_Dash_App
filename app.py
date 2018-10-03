# -*- coding: utf-8 -*-

import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as plotly
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
from flask_cors import CORS
import pandas as pd
import numpy as np
import os





app = dash.Dash(__name__)
#server = app.server
#if 'DYNO' in os.environ:
#    app.scripts.append_script({
#        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
#    })

## server here

mapbox_access_token = 'pk.eyJ1IjoibWloYWx3MjgiLCJhIjoiY2psejZqZThnMXRndDNxcDFpdWh6YnV2NCJ9.IGbFZyg0dcy61geuwJUByw'


def initialize():
    df = pd.read_csv('../NYC_Crimes_Dash_App/crimes_app_data.csv')
    df.drop('Unnamed: 0', 1, inplace = True)
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format = '%Y-%m-%d %H:%M:%S')
    df.index = df['Date/Time']
    df.drop('Date/Time', 1, inplace = True)
    totalList = []
    for month in df.groupby(df.index.month):
        dailyList = []
        for day in month[1].groupby(month[1].index.day):
            dailyList.append(day[1])
        totalList.append(dailyList)
    return np.array(totalList)


app.layout = html.Div([
    html.Div([
        html.Div([
            html.P(id = 'total_incidents', className = 'totalIncidents'),
            html.P(id = 'total_incidents_selection', className = 'totalIncidentsSelection'),
            html.P(id = 'date_value', className = 'dateValue'),
            dcc.Dropdown(
                id = 'my_dropdown',
                options = [
                    {'label': 'January', 'value': 'Jan'},
                    {'label': 'February', 'value': 'Feb'},
                    {'label': 'March', 'value': 'Mar'},
                    {'label': 'April', 'value': 'Apr'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'Jun'},
                    {'label': 'July', 'value': 'Jul'},
                    {'label': 'August', 'value': 'Aug'},
                    {'label': 'September', 'value': 'Sep'},
                    {'label': 'October', 'value': 'Oct'},
                    {'label': 'November', 'value': 'Nov'},
                    {'label': 'December', 'value': 'Dec'}
                ],
                value = 'Jan',
                placeholder = 'Please choose a day',
                className = 'day_picker'
            ),
            html.Div([
                html.Div([
                    html.H2('Dash - Crimes in NYC', style = {'font-family': 'Dosis'}),
                ]),
                html.P('Select different days using the dropdown and the slider\
                        below or by selecting different time frames on the\
                        histogram',
                        className = 'explanationParagraph twelve columns'),
                dcc.Graph(id = 'map_graph'),
                dcc.Dropdown(
                    id = 'bar_selector',
                    options = [
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
                    multi = True,
                    placeholder = 'Select certain hours using\
                                   the box-select or lasso tool\
                                   or using the dropdown menu',
                    className = 'bars'
                ),
                dcc.Graph(id = 'histogram'),
                html.P('', id = 'popupAnnotation', className='popupAnnotation')
            ],
            className = 'graph twelve columns'
            ),
        ], 
        style={'margin': 'auto auto'}),
        dcc.Slider(
            id = 'my_slider',
            min = 1,
            step = 1,
            value = 1
        ),
        dcc.Checklist(
            id='mapControls',
            options=[
                {'label': 'Lock Camera', 'value': 'lock'}
            ],
            values=[''],
            labelClassName='mapControls',
            inputStyle={'z-index': '3'}
        ),
    ],
    className = 'graphSilder ten columns offset-by-one'),
],
style={'padding-top': '20px'}
)


def getValue(value):
    val = {
        'Jan': 31,
        'Feb': 28,
        'Mar': 31,
        'Apr': 30,
        'May': 31,
        'Jun': 30,
        'Jul': 31,
        'Aug': 31,
        'Sep': 30,
        'Oct': 31,
        'Nov': 30,
        'Dec': 31
    }
    [value]
    return val

def getIndex(value):
    if(value == None):
        return 0
    val = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'Jun': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11
    }
    [value]
    return val

def getClickIndex(value):
    if(value==None):
        return 0
    return value['points'][0]['x']


@app.callback(Output("my_slider", 'marks'),
              [Input('my_dropdown', 'value')]
)
def update_slider_ticks(value):
    marks = {}
    for i in range(1, getValue(value) + 1, 1):
        if (i is 1 or i is getValue(value)):
            marks.update({i: '{} {}'.format(value, i)})
        else:
            marks.update({i: '{}'.format(i)})
    return marks


@app.callback(Output('my_slider', 'max'),
              [Input('my_dropdown', 'value')]
)
def update_slider_max(value):
    return getValue(value)


@app.callback(Output('bar_selector', 'value'),
              [Input('histogram', 'selectedData')]
)
def update_bar_selector(value):
    holder = []
    if( value is None or len(value) is 0):
        return holder
    for x in value['points']:
        holder.append(str(int(x['x'])))
    return holder


@app.callback(Output('total_incidents', 'children'),
              [Input('my_dropdown', 'value'), Input('my_slider', 'value')]
)
def update_total_rides(value, slider_value):
    return ('Total # of incidents: {:,d}'.format(len(totalList[getIndex(value)][slider_value - 1])))


@app.callback(Output('total_incidents_selection', 'children'),
              [Input('my_dropdown', 'value'), Input('my_slider', 'value'),
               Input('bar_selector', 'value')]
)
def update_total_incidents_selection(value, slider_value, selection):
    if(selection is None or len(selection) is 0):
        return ''
    totalInSelection = 0
    for x in selection:
        totalInSelection += len(totalList[getIndex(value)]
                                         [slider_value - 1]
                                         [totalList[getIndex(value)]
                                         [slider_value - 1].index.hour == int(x)])
    return ('Total incidents in selection: {:,d}'.format(totalInSelection))                                     


@app.callback(Output('date_value', 'children'),
              [Input('my_dropdown', 'value'), Input('my_slider', 'value'),
               Input('bar_selector', 'value')]
)
def update_date(value, slider_value, selection):
    holder = []
    if(value is None or selection is None or len(selection) is 24 or len(selection) is 0):
        return (value, '', slider_value, ' - showing: All')

    for x in selection:
        holder.append(int(x))
    holder.sort()

    if(holder[len(holder) - 1] - holder[0] + 2 == len(holder) + 1 and len(holder) > 2):
        return (value, ' ', slider_value, ' - showing hour(s): ',
                holder[0], '-', holder[len(holder) - 1])

    x = ''
    for h in holder:
        if (holder.index(h) == (len(holder) - 1)):
            x += str(h)
        else:
            x += str(h) + ', '
    return (value, ', ', slider_value, ' - showing hours(s): ', x)


@app.callback(Output('histogram', 'selectedData'),
              [Input('my_dropdown', 'value')]
)
def clear_selection(value):
    if (value is None or len(value) is 0):
        return None


@app.callback(Output('popupAnnotation', 'children'),
              [Input('bar_selector', 'value')]
)
def clear_selection_1(value):
    if (value is None or len(value) is 0):
        return 'Select any of the bars to section data by time'
    else:
        return ''


def get_selection(value, slider_value, selection):
    xVal = []
    yVal = []
    xSelected = []

    colorVal = ["#F4EC15", "#DAF017", "#BBEC19", "#9DE81B", "#80E41D", "#66E01F",
                "#4CDC20", "#34D822", "#24D249", "#25D042", "#26CC58", "#28C86D",
                "#29C481", "#2AC093", "#2BBCA4", "#2BB5B8", "#2C99B4", "#2D7EB0",
                "#2D65AC", "#2E4EA4", "#2E38A4", "#3B2FA0", "#4E2F9C", "#603099"]

    if (selection is not None):
        for x in selection:
            xSelected.append(int(x))
    for i in range(0, 24, 1):
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = ('#FFFFFF')
        xVal.append(i)
        yVal.append(len(totalList[getIndex(value)][slider_value - 1]
                    [totalList[getIndex(value)][slider_value - 1].index.hour == i]))
    return [np.array(xVal), np.array(yVal), np.array(xSelected), np.array(colorVal)]



@app.callback(Output('histogram', 'figure'),
              [Input('my_dropdown', 'value'), Input('my_slider', 'value'),
               Input('bar_selector', 'value')]
)
def update_histogram(value, slider_value, selection):
    [xVal, yVal, xSelected, colorVal] = get_selection(value, slider_value, selection)


    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode='group',
        margin=Margin(l=10, r=0, t=0, b=30),
        showlegend=False,
        plot_bgcolor='#323130',
        paper_bgcolor='rgb(66, 134, 244)',
        height=250,
        dragmode='select',
        xaxis=dict(
            range=[-0.5, 23.5],
            showgrid=False,
            nticks=25,
            fisedrange=True,
            ticksuffix=':00'
        ),
        yaxis=dict(
            range=[0, max(yVal)+max(yVal)/4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode='nonnegative',
            zeroline='hidden'            
        ),
        annotations=[
            dict(x=xi, y=yi,
                 text=str(yi),
                 xanchor='center',
                 yanchor='bottom',
                 showarrow=False,
                 font=dict(
                    color='white'
                 )
            )
            for xi, yi, in zip(xVal, yVal)
        ]
    )


    return go.Figure(
           data=Data([
                go.Bar(
                    x=xVal,
                    y=yVal,
                    marker=dict(
                        color=colorVal
                    ),
                    hoverinfo="x"
                ),
                go.Scatter(
                    opacity=0,
                    x=xVal,
                    y=yVal/2,
                    hoverinfo="none",
                    mode='markers',
                    marker=Marker(
                        color='rgb(66, 134, 244, 0)',
                        symbol="square",
                        size=40
                    ),
                    visible=True
                )
            ]), 
            layout=layout)


def get_lat_lon_color(selectedData, value, slider_value):
    listStr = 'totalList[getIndex(value)][slider_value - 1]'
    if (selectedData is None or len(selectedData) is 0):
        return listStr
    elif (int(selectedData[len(selectedData) - 1]) - int(selectedData[0])+2 == len(selectedData)+1\
          and len(selectedData) > 2):
        listStr += "[(totalList[getIndex(value)][slider_value-1].index.hour>"+str(int(selectedData[0]))+") & \
                    (totalList[getIndex(value)][slider_value-1].index.hour<" + str(int(selectedData[len(selectedData)-1]))+")]"
    else:
        listStr += '['
        for point in selectedData:
            if (selectedData.index(point) is not len(selectedData) - 1):
                listStr += 'totalList[getIndex(value)][slider_value - 1].index.hour==' + str(int(point)) + ') | '
            else:
                listStr += "(totalList[getIndex(value)][slider_value-1].index.hour==" + str(int(point)) + ')]'
    return listStr


@app.callback(Output('map_graph', 'figure'),
              [Input('my_dropdown', 'value'), Input('my_slider', 'value'),
              Input('bar_selector', 'value')],
              [State('map_graph', 'relayoutData'),
               State('mapControls', 'values')])
def update_graph(value, slider_value, selectedData, prevLayout, mapControls):
    zoom = 12.0
    latInitial = 40.7272
    lonInitial = -73.991251
    bearing = 0

    listStr = get_lat_lon_color(selectedData, value, slider_value)

    if (prevLayout is not None and mapControls is not None and 'lock' in mapControls):
        zoom = float(prevLayout['mapbox']['zoom'])
        latInitial = float(prevLayout['mapbox']['center']['lat'])
        lonInitial = float(prevLayout['mapbox']['center']['lon'])
        bearing = float(prevLayout['mapbox']['bearing'])
    return go.Figure(
        data=Data([
            Scattermapbox(
                lat=eval(listStr)['Lat'],
                lon=eval(listStr)['Lon'],
                mode='markers',
                hoverinfo='lat+lon+text',
                text=eval(listStr).index.hour,
                marker=Marker(
                    color=np.append(np.insert(eval(listStr).index.hour, 0, 0), 23),
                    colorscale=[[0, "#F4EC15"], [0.04167, "#DAF017"],
                                [0.0833, "#BBEC19"], [0.125, "9DE81B"],
                                [0.1667, "#80E41D"], [0.2083, "#66E01F"],
                                [0.25, "#4CDC20"], [0.292, "#34D822"],
                                [0.333, "#24D249"], [0.375, "#25D042"],
                                [0.4167, "#26CC58"], [0.4583, "#28C86D"],
                                [0.50, "#29C481"], [0.54167, "#2AC093"],
                                [0.5833, "#2BBCA4"],
                                [1.0, "#613099"]],
                    opacity=0.5,
                    size=5,
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
                        titleside='left'
                    )
                ),
            ),
            Scattermapbox(
                lat=['40.781', '40.857', '40.659', '40.585', '40.716'],
                lon=['-73.974', '-73.898', '-73.957', '-74.165', '-73.827'],
                mode='markers',
                hoverinfo='text',
                text=['Manhattan', 'Bronx', 'Brooklyn', 'Staten Island', 'Queens'],
                # opacity=0.5,
                marker=Marker(
                    size=6,
                    color='#ffa0a0'
                ),
            ),
        ]),
        layout=Layout(
            autosize=True,
            height=750,
            margin=Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial, # 40.7272
                    lon=lonInitial # -73.991251
                ),
                #style='dark',
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                'mapbox.zoom': 12,
                                'mapbox.center.lon': '-73.991251',
                                'mapbox.center.lat': '40.7272',
                                'mapbox.bearing': 0,
                                # 'mapbox.style': 'dark'
                            }],
                            label='Raset Zoom',
                            method='relayout'
                        )
                    ]),
                    direction='left',
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
                                }],
                            label='Manhattan',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11.5,
                                    'mapbox.center.lon': '-73.898',
                                    'mapbox.center.lat': '40.857',
                                    'mapbox.bearing': 0,
                                }],
                            label='Bronx',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11.5,
                                    'mapbox.center.lon': '-73.957',
                                    'mapbox.center.lat': '40.659',
                                    'mapbox.bearing': 0,
                                }],
                            label='Brooklyn',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11.5,
                                    'mapbox.center.lon': '-74.165',
                                    'mapbox.center.lat': '40.585',
                                    'mapbox.bearing': 0,
                                }],
                            label='Staten Island',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11.5,
                                    'mapbox.center.lon': '-73.827',
                                    'mapbox.center.lat': '40.716',
                                    'mapbox.bearing': 0,
                                }],
                            label='Queens',
                            method='relayout'
                        )
                    ]),
                    direction="down",
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#FFFFFF"
                    ),
                    x=0,
                    y=0.05
                )
            ]
        )
    )


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]


for css in external_css:
    app.css.append_css({'external_url': css})


@app.server.before_first_request
def defineTotalList():
    global totalList
    totalList = initialize()


if __name__ == '__main__':
    app.run_server(debug=True)