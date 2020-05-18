# -*- coding: utf-8 -*-
import os
import sqlite3
from ast import literal_eval

import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, g

DATABASE = './db.sqlite3'

server = Flask('Dash')
server.secret_key = os.environ.get('SECRET_KEY', 'secret123')

app = dash.Dash(__name__, server=server)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@server.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_data(query):
    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


with server.app_context():
    have_hobbyist = get_data('SELECT * FROM data WHERE Hobbyist = "Yes"')
    no_have_hobbyist = get_data('SELECT * FROM data WHERE Hobbyist = "No"')
    never = get_data('SELECT * FROM data WHERE OpenSourcer = "Never"')
    no_student = get_data('SELECT * FROM data WHERE Student = "No"')
    full_time_student = get_data('SELECT * FROM data WHERE Student = "Yes, full-time"')
    part_time_student = get_data('SELECT * FROM data WHERE Student = "Yes, part-time"')
    lt_once_year = get_data('SELECT * FROM data WHERE OpenSourcer = "Less than once per year"')
    lt_once_month_gt_once_year = get_data(
        "SELECT * FROM data WHERE OpenSourcer = \"Less than once a month but more than once per year\"")
    ge_once_month = get_data('SELECT * FROM data WHERE OpenSourcer = "Once a month or more often"')


app.layout = html.Div(children=[

    html.Div(style={
        'textAlign': 'center',
    }, children=[
            html.H2(
                children='Developer Profile',
            ),
        ]
    ),

    html.Div(style={
        'float': 'left',
        'margin-left': '55px'
    }, children=[
        dcc.Graph(
            id='hobbyist',
            figure={
                'data': [
                    {'x': ["Yes"], 'y': [len(have_hobbyist)], 'type': 'bar', 'name': 'Yes'},
                    {'x': ["No"], 'y': [len(no_have_hobbyist)], 'type': 'bar', 'name': 'No'},
                ],
                'layout': {
                    'title': 'Coding as a Hobby'
                }
            }
        ),
    ]),

    html.Div(style={
        'float': 'left',
    }, children=[
        dcc.Graph(
            id='student',
            figure={
                'data': [
                    {'x': ["No"], 'y': [len(no_student)], 'type': 'bar', 'name': 'No'},
                    {'x': ["Yes, full-time"], 'y': [len(full_time_student)], 'type': 'bar', 'name': 'Yes, full-time'},
                    {'x': ["Yes, part-time"], 'y': [len(lt_once_year)], 'type': 'bar', 'name': 'Yes, part-time'},
                ],
                'layout': {
                    'title': 'How Many Developers are Students?'
                }
            }
        ),
    ]),

    html.Div(style={'clear': 'both'}),

    html.Div(children=[
        dcc.Graph(
            id='open_sourcer',
            figure={
                'data': [
                    {'x': ["Once a month or more often"], 'y': [len(ge_once_month)], 'type': 'bar',
                     'name': 'Once a month or more often'},
                    {'x': ["Less than once a month..."], 'y': [len(lt_once_month_gt_once_year)]
                        , 'type': 'bar', 'name': 'Less than once a month but more than once per year'},
                    {'x': ["Less than once per year"], 'y': [len(lt_once_year)], 'type': 'bar',
                     'name': 'Less than once per year'},
                    {'x': ["Never"], 'y': [len(never)], 'type': 'bar', 'name': 'Never'},
                ],
                'layout': {
                    'title': 'Contributing to Open Source'
                }
            }
        ),
    ])
])

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(
        debug=literal_eval(os.environ.get('DEBUG', 'True')),
        host=os.environ.get('HOST', '0.0.0.0'),
        port=literal_eval(os.environ.get('PORT', '8000'))
    )
