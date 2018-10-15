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




app = dash.Dash('UberApp')
server = app.server
#if 'DYNO' in os.environ:
#    app.scripts.append_script({
#        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
#    })

mapbox_access_token = 'pk.eyJ1IjoibWloYWx3MjgiLCJhIjoiY2psejZqZThnMXRndDNxcDFpdWh6YnV2NCJ9.IGbFZyg0dcy61geuwJUByw'


def initialize():
    df = pd.read_csv('../NYC_Crimes_Dash_App/crimes_app_data.csv')
    #df.drop('Unnamed: 0', 1, inplace=True)
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%Y-%m-%d %H:%M:%S')
    df.index = df['Date/Time']
    df.drop('Date/Time', 1, inplace=True)
    df.round({'Latitude': 4, 'Longitude': 4})
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
                #value="Jan",
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
                    {'label': 'All', 'value': 'all'}
                ],
                #value='All',
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
                    {'label': "All", 'value': 'all'}
                ],
                #value='All',
                placeholder='Suspector age:',
                className='two columns'
            ),
            dcc.Dropdown(
                id='sex-dropdown',
                options=[
                    {'label': 'Female', 'value': 'f'},
                    {'label': 'Male', 'value': 'm'},
                    {'label': 'Both', 'value': 'both'}
                ],
                #value='b',
                placeholder='Suspector sex:',
                className='two columns'
            ),
            html.Div([
                html.Div([
                    html.H2("Dash - Crimes in NYC", style = {'font-family': 'Dosis'}),
                ]),
                html.P('Select different days using the dropdown and the slider\
                        below or by selecting different time frames on the\
                        histogram',
                    className="explanationParagraph twelve columns"),
                dcc.Graph(id='map-graph'),
            ]),
            html.Div([  
                    dcc.Graph(id='pie_graph'),
                ], className = 'pie bottom three columns'), #), #should be 'columns', but for now 'coluns'
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
            dcc.Checklist(
                id='incidentTypeControls',
                options=[
                    {'label': 'FELONY', 'value': 'fel'},
                    {'label': 'MISDEMEANOR', 'value': 'mis'},
                    {'label': 'VIOLATION', 'value': 'vio'}
                ],
                values=['fel', 'mis', 'vio'],
                labelClassName='incidentTypeControls',
                inputStyle={'z-index': '1'}
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
    if(value==None):
        return 0
    val = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2
    }[value]
    return val


def all_races(arg1, arg2):
    x = totalList[getIndex(arg1)][arg2].SUSP_RACE
    return x


def all_ages(arg1, arg2):
    x = totalList[getIndex(arg1)][arg2].SUSP_AGE_GROUP
    return x


def all_sexes(arg1, arg2):
    x = totalList[getIndex(arg1)][arg2].SUSP_SEX
    return x


def getRace(value, *args):
    if(value==None):
        return all_races(*args)
    val = {
        'Bl': 'BLACK',
        'Whh': 'WHITE HISPANIC',
        'Wh': 'WHITE',
        'As': 'ASIAN/PAC.ISL',
        'Blh': 'BLACK HISPANIC',
        'Am': 'AMER IND',
        'all': all_races(*args)
    }[value]
    return val


def getAge(value, *args):
    if(value==None):
        return all_ages(*args)
    val = {
        'u18': '<18',
        'u24': '18-24',
        'u44': '25-44',
        'u64': '45-64',
        'a65': '65+', 
        'all': all_ages(*args)
    }[value]
    return val


def getSex(value, *args):
    if(value==None):
        return 'M'
    val = {
        'f': 'F',
        'm': 'M', 
        'both': all_sexes(*args)
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


'''@app.callback(Output("my-slider", "marks"),
              [Input("my-dropdown", "value")])
def update_slider_ticks(value):
    for i in range(0, getValue(value)+1):
        if (i is 0 or i is getValue(value)):
            marks.update({i: '{}'.format(marks[value])})
        else:
            marks.update({i: '{}'.format(i)})
    return marks


@app.callback(Output("my-slider", "max"),
              [Input("my-dropdown", "value")])
def update_slider_max(value):
    return getValue(value)'''


@app.callback(Output("bar-selector", "value"),
              [Input("histogram", "selectedData")])
def update_bar_selector(value):
    holder = []
    if (value is None or len(value) is 0):
        return holder
    for x in value['points']:
        holder.append(str(int(x['x'])))
    return holder


@app.callback(Output("total-rides", "children"),
              [Input("my-dropdown", "value"), 
               Input('my-slider', 'value')]
)
def update_total_rides(value, slider_value):
    return ("Total # of incidents: {:,d}".format(len(totalList[getIndex(value)][slider_value])))


@app.callback(Output('total-rides-selection', 'children'),
              [Input('my-dropdown', 'value'), 
               Input('my-slider', 'value'),
               Input('bar-selector', 'value')]
)
def update_total_rides_selection(value, slider_value, selection):
    if (selection is None or len(selection) is 0):
        return ""
    totalInSelction = 0
    for x in selection:
        totalInSelction += len(totalList[getIndex(value)]
                                         [slider_value]
                                         [totalList[getIndex(value)]
                                                [slider_value].index.hour == int(x)])
    return ('Total incidents in selection: {:,d}'
            .format(totalInSelction))                                     


@app.callback(Output('date-value', 'children'),
              [Input('my-dropdown', 'value'), Input('my-slider', 'value'),
               Input('bar-selector', 'value')]
)
def update_date(value, slider_value, selection):
    holder = []
    
    if (value is None or selection is None or len(selection) is 24 or len(selection) is 0):
        return (value, ' {}'.format(getTickLabel(slider_value)), ' - showing: All')

    for x in selection:
        holder.append(int(x))
    holder.sort()

    if(holder[len(holder)-1]-holder[0]+2 == len(holder)+1 and len(holder) > 2):
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
                      Input('sex-dropdown', 'value')]
)
def make_pie(value, slider_value, race_value, age_value, sex_value):

    boro_color = {
        'MANHATTAN': '#fae13d',
        'BRONX': '#3ef989',
        'BROOKLYN': '#42c9fa',
        'STATEN ISLAND': '#d14af2',
        'QUEENS': '#de5959'
    }
    
    boros_dict = totalList[getIndex(value)][slider_value].BORO_NM[(totalList[getIndex(value)][slider_value].SUSP_RACE == getRace(race_value, value, slider_value))
                                                                 & (totalList[getIndex(value)][slider_value].SUSP_AGE_GROUP == getAge(age_value, value, slider_value))
                                                                 & (totalList[getIndex(value)][slider_value].SUSP_SEX == getSex(sex_value, value, slider_value))].value_counts().to_dict()

    
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
                marker=dict(
                    colors = getBorosColors(labels),
                    line=dict(
                        color='rgb(0, 0, 0)',
                        width=1.2,
                    )
                ),
                opacity=0.8
            ),
        ], 
        layout=go.Layout(
            title='Incidents in boroughs on {}'.format(getTickLabel(slider_value)),
            titlefont=dict(
                size=13,
                color='rgb(255, 255, 255)'
            ),
            showlegend=False,
            height=285,
            margin=dict(l=15, r=50, t=50, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    )
    return figure


@app.callback(Output('histogram', 'selectedData'),
              [Input('my-dropdown', 'value')])
def clear_selection(value):
    if(value is None or len(value) is 0):
        return None


@app.callback(Output('popupAnnotation', 'children'),
              [Input('bar-selector', 'value')])
def clear_selection1(value):
    if(value is None or len(value) is 0):
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

    if(selection is not None):
        for x in selection:
            xSelected.append(int(x))
    for i in range(0, 24, 1):
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = ('#ffffff')
        xVal.append(i)
        yVal.append(len(totalList[getIndex(value)][slider_value]
                    [totalList[getIndex(value)][slider_value].index.hour == i]))

    return [np.array(xVal), np.array(yVal), np.array(xSelected), np.array(colorVal)]



@app.callback(Output('histogram', 'figure'),
              [Input('my-dropdown', 'value'), Input('my-slider', 'value'),
               Input('bar-selector', 'value')]
)
def update_histogram(value, slider_value, selection):

    [xVal, yVal, xSelected, colorVal] = get_selection(value, slider_value, selection)

    layout = go.Layout(
        bargap=0,
        bargroupgap=0,
        barmode='group',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        plot_bgcolor='#323130',
        paper_bgcolor='rgb(66, 134, 244, 0)',
        height=250,
        dragmode='select',
        xaxis=dict(
            range=[-0.5, 23.5],
            showticklabels=True,
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=':00'
        ),
        yaxis=dict(
            range=[0, max(yVal)+max(yVal)/2],
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
                go.Scatter(
                    opacity=0,
                    x=xVal,
                    y=yVal/2,
                    hoverinfo="none",
                    mode='markers',
                    marker=dict(
                        color='rgb(66, 134, 244)',
                        symbol="square",
                        size=40
                    ),
                    visible=True
                )
            ], layout=layout)


def get_lat_lon_color(selectedData, value, slider_value):
    listStr = 'totalList[getIndex(value)][slider_value-1]'
    if(selectedData is None or len(selectedData) is 0):
        return listStr
    elif(int(selectedData[len(selectedData)-1])-int(selectedData[0])+2 == len(selectedData)+1 and len(selectedData) > 2):
        listStr += "[(totalList[getIndex(value)][slider_value-1].index.hour>"+str(int(selectedData[0]))+") & \
                    (totalList[getIndex(value)][slider_value-1].index.hour<" + str(int(selectedData[len(selectedData)-1]))+")]"
    else:
        listStr += "["
        for point in selectedData:
            if (selectedData.index(point) is not len(selectedData)-1):
                listStr += "(totalList[getIndex(value)][slider_value-1].index.hour==" + str(int(point)) + ") | "
            else:
                listStr += "(totalList[getIndex(value)][slider_value-1].index.hour==" + str(int(point)) + ")]"

    return listStr


@app.callback(Output('map-graph', 'figure'),
              [Input('my-dropdown', 'value'), Input('my-slider', 'value'),
              Input('bar-selector', 'value')],
              [State('map-graph', 'relayoutData'),
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
        data=[
            go.Scattermapbox(
                lat=eval(listStr)['Latitude'],
                lon=eval(listStr)['Longitude'],
                mode='markers',
                hoverinfo='lat+lon+text',
                text=eval(listStr).index.hour,
                marker = dict(
                    color=np.append(np.insert(eval(listStr).index.hour, 0, 0), 23),
                    colorscale='Viridis',
                    reversescale=True,
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
                style='mapbox://styles/mihalw28/cjmrjsycy0m1r2snnp9kkl14n',
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
                                'mapbox.style': 'mapbox://styles/mihalw28/cjmrjsycy0m1r2snnp9kkl14n'
                            }],
                            label='Reset Zoom',
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
                                'mapbox.style': 'mapbox://styles/mihalw28/cjmrjsycy0m1r2snnp9kkl14n'
                                }],
                            label='Manhattan',
                            method='relayout'
                        ),  
                    ]),
                    #direction="down",
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
                    x=0.01,
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
                                'mapbox.style': 'mapbox://styles/mihalw28/cjmrjsycy0m1r2snnp9kkl14n'
                                }],
                            label='Bronx',
                            method='relayout'
                        ),  
                    ]),
                    #direction="down",
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
                    x=0.01,
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
                                'mapbox.style': 'mapbox://styles/mihalw28/cjmrjsycy0m1r2snnp9kkl14n'
                                }],
                            label='Brooklyn',
                            method='relayout'
                        ),  
                    ]),
                    #direction="down",
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
                    x=0.01,
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
                                'mapbox.style': 'mapbox://styles/mihalw28/cjmrjsycy0m1r2snnp9kkl14n'
                                }],
                            label='Staten Island',
                            method='relayout'
                        ),  
                    ]),
                    #direction="down",
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
                    x=0.01,
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
                                'mapbox.style': 'mapbox://styles/mihalw28/cjmrjsycy0m1r2snnp9kkl14n'
                                }],
                            label='Queens',
                            method='relayout'
                        ),  
                    ]),
                    #direction="down",
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
                    x=0.01,
                    y=0.37
                ),
            ]
        )
    )


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.before_first_request
def defineTotalList():
    global totalList
    totalList = initialize()


if __name__ == '__main__':
    app.run_server(debug=True)
