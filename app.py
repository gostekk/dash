# -*- coding: utf-8 -*-
import os
import sqlite3
from ast import literal_eval

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
        'SELECT * FROM data WHERE OpenSourcer = "Less than once a month but more than once per year"')
    ge_once_month = get_data('SELECT * FROM data WHERE OpenSourcer = "Once a month or more often"')
    developer_full_stack = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, full-stack%"')
    developer_back_end = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, back-end%"')
    developer_front_end = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, front-end%"')
    developer_desktop = get_data(
        'SELECT * FROM data WHERE DevType LIKE "%Developer, desktop or enterprise applications%"')
    developer_mobile = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, mobile%"')
    developer_test = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, QA or test%"')
    developer_game_graphics = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, game or graphics%"')

category = ['Developer Roles', 'Education']

app.layout = html.Div(children=[

    html.Div(style={
        'textAlign': 'center',
    }, children=[
        html.H2(
            children='Developer Profile',
        ),
    ]),

    html.Div([
        dcc.Dropdown(
            id='category',
            options=[{'label': i, 'value': i} for i in category],
            value='Developer Roles'
        )
    ]),

    html.Div(id='content')
])


@app.callback(
    Output('content', 'children'),
    [Input('category', 'value')]
)
def update_content(category_name):
    if category_name == 'Developer Roles':
        return [
            html.Div(children=[
                dcc.Graph(
                    id='developer_type',
                    figure={
                        'data': [
                            {'x': ["Full-stack"], 'y': [len(developer_full_stack)], 'type': 'bar',
                             'name': 'Developer, full-stack'},
                            {'x': ["Back-end"], 'y': [len(developer_back_end)], 'type': 'bar',
                             'name': 'Developer, back-end'},
                            {'x': ["Front-end"], 'y': [len(developer_front_end)], 'type': 'bar',
                             'name': 'Developer, front-end'},
                            {'x': ["Desktop or enterprise applications"], 'y': [len(developer_desktop)],
                             'type': 'bar', 'name': 'Developer, desktop or enterprise applications'},
                            {'x': ["Mobile"], 'y': [len(developer_mobile)], 'type': 'bar',
                             'name': 'Developer, mobile'},
                            {'x': ["QA or test"], 'y': [len(developer_test)], 'type': 'bar',
                             'name': 'Developer, QA or test'},
                            {'x': ["Game or graphics"], 'y': [len(developer_game_graphics)], 'type': 'bar',
                             'name': 'Developer, game or graphics'},
                        ],
                        'layout': {
                            'title': 'Developer Type'
                        }
                    }
                ),
            ]),

            html.Div(children=[
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
            ]),
        ]
    else:
        return [
            html.Div(children=[
                dcc.Graph(
                    id='student',
                    figure={
                        'data': [
                            {'x': ["No"], 'y': [len(no_student)], 'type': 'bar', 'name': 'No'},
                            {'x': ["Yes, full-time"], 'y': [len(full_time_student)], 'type': 'bar',
                             'name': 'Yes, full-time'},
                            {'x': ["Yes, part-time"], 'y': [len(lt_once_year)], 'type': 'bar',
                             'name': 'Yes, part-time'},
                        ],
                        'layout': {
                            'title': 'How Many Developers are Students?'
                        }
                    }
                ),
            ]),
        ]


external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(
        debug=literal_eval(os.environ.get('DEBUG', 'True')),
        host=os.environ.get('HOST', '0.0.0.0'),
        port=literal_eval(os.environ.get('PORT', '8000'))
    )
