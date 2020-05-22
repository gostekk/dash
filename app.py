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
    hobbyist = get_data('SELECT Hobbyist, COUNT(Hobbyist) FROM data GROUP BY Hobbyist')
    never = get_data('SELECT * FROM data WHERE OpenSourcer = "Never"')
    open_source = get_data('SELECT OpenSourcer, COUNT(OpenSourcer) FROM data GROUP BY OpenSourcer')
    student = get_data('SELECT Student, COUNT(Student) FROM data WHERE Student != "NA" GROUP BY Student')
    developer_full_stack = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, full-stack%"')
    developer_back_end = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, back-end%"')
    developer_front_end = get_data('SELECT * FROM data WHERE DevType LIKE "%Developer, front-end%"')
    developer_desktop = get_data(
        'SELECT DevType FROM data WHERE DevType LIKE "%Developer, desktop or enterprise applications%"')
    developer_mobile = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, mobile%"')
    developer_test = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, QA or test%"')
    developer_game_graphics = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, game or graphics%"')
    educational = get_data('SELECT EDLevel, COUNT(EDlevel) FROM data WHERE EDLevel != "NA" GROUP BY EDLevel')

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
                            {'x': [hobbyist[1][0]], 'y': [hobbyist[1][1]], 'type': 'bar', 'name': hobbyist[1][0]},
                            {'x': [hobbyist[0][0]], 'y': [hobbyist[0][1]], 'type': 'bar', 'name': hobbyist[0][0]},
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
                            {'x': [open_source[0][0]], 'y': [open_source[0][1]], 'type': 'bar',
                             'name': open_source[0][0]},
                            {'x': [open_source[1][0]], 'y': [open_source[1][1]]
                                , 'type': 'bar', 'name': open_source[1][0]},
                            {'x': [open_source[2][0]], 'y': [open_source[2][1]], 'type': 'bar',
                             'name': open_source[2][0]},
                            {'x': [open_source[3][0]], 'y': [open_source[3][1]], 'type': 'bar',
                             'name': open_source[3][0]},
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
                            {'x': [student[0][0]], 'y': [student[0][1]], 'type': 'bar', 'name': student[0][0]},
                            {'x': [student[1][0]], 'y': [student[1][1]], 'type': 'bar', 'name': student[1][0]},
                            {'x': [student[2][0]], 'y': [student[2][1]], 'type': 'bar', 'name': student[2][0]},
                        ],
                        'layout': {
                            'title': 'How Many Developers are Students?'
                        }
                    }
                ),
            ]),

            html.Div(children=[
                dcc.Graph(
                    id='educational_attainment',
                    figure={
                        'data': [
                            {'x': ['Any formal education'], 'y': [educational[2][1]], 'type': 'bar',
                             'name': educational[2][0]},
                            {'x': ['Primary school'], 'y': [educational[5][1]], 'type': 'bar',
                             'name': educational[5][0]},
                            {'x': ['Secondary school'], 'y': [educational[7][1]], 'type': 'bar',
                             'name': educational[7][0]},
                            {'x': ['Some college'], 'y': [educational[8][1]], 'type': 'bar',
                             'name': educational[8][0]},
                            {'x': ['Associate degree'], 'y': [educational[0][1]], 'type': 'bar',
                             'name': educational[0][0]},
                            {'x': ["Bachelor's degree"], 'y': [educational[1][1]], 'type': 'bar',
                             'name': educational[1][0]},
                            {'x': ['Master degree'], 'y': [educational[3][1]], 'type': 'bar',
                             'name': educational[3][0]},
                            {'x': ['Professional degree'], 'y': [educational[6][1]], 'type': 'bar',
                             'name': educational[6][0]},
                            {'x': ['Doctoral degree'], 'y': [educational[4][1]], 'type': 'bar',
                             'name': educational[4][0]},
                        ],
                        'layout': {
                            'title': 'Educational Attainment'
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
