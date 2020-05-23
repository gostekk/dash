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
    undergrad_major = get_data(
        'SELECT UndergradMajor, COUNT(UndergradMajor) FROM data WHERE UndergradMajor != "NA" GROUP BY UndergradMajor')
    years_code = get_data('SELECT YearsCode, COUNT(YearsCode) FROM data WHERE YearsCode != "NA" GROUP BY YearsCode')


def add_years(start, end):
    years = 0
    for i in range(start, end):
        years += years_code[i][1]
    years_since_learning_code.append(years)


years_since_learning_code = []
less_then_10 = years_code[0][1] + years_code[11][1] + years_code[22][1] + years_code[33][1] + years_code[44][1] \
               + years_code[46][1] + years_code[47][1] + years_code[48][1] + years_code[49][1] + years_code[50][1]
years_since_learning_code.append(less_then_10)

add_years(1, 11)
add_years(12, 22)
add_years(23, 33)
add_years(34, 44)

years_since_learning_code.append(years_code[45][1] + years_code[51][1])

category = ['Developer Roles', 'Education', 'Experience']

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
    elif category_name == 'Education':
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

            html.Div(children=[
                dcc.Graph(
                    id='undergraduate_major',
                    figure={
                        'data': [
                            {'x': ['Computer science...'], 'y': [undergrad_major[6][1]], 'type': 'bar',
                             'name': undergrad_major[6][0]},
                            {'x': ['Another engineering...'], 'y': [undergrad_major[5][1]], 'type': 'bar',
                             'name': undergrad_major[5][0]},
                            {'x': ['Information systems...'], 'y': [undergrad_major[9][1]], 'type': 'bar',
                             'name': undergrad_major[9][0]},
                            {'x': ['Web development...'], 'y': [undergrad_major[11][1]], 'type': 'bar',
                             'name': undergrad_major[11][0]},
                            {'x': ['Natural science'], 'y': [undergrad_major[3][1]], 'type': 'bar',
                             'name': undergrad_major[3][0]},
                            {'x': ['Mathematics...'], 'y': [undergrad_major[10][1]], 'type': 'bar',
                             'name': undergrad_major[10][0]},
                            {'x': ['Business discipline'], 'y': [undergrad_major[0][1]], 'type': 'bar',
                             'name': undergrad_major[0][0]},
                            {'x': ['Humanities discipline'], 'y': [undergrad_major[2][1]], 'type': 'bar',
                             'name': undergrad_major[2][0]},
                            {'x': ['Social science'], 'y': [undergrad_major[4][1]], 'type': 'bar',
                             'name': undergrad_major[4][0]},
                            {'x': ['Fine arts...'], 'y': [undergrad_major[7][1]], 'type': 'bar',
                             'name': undergrad_major[7][0]},
                            {'x': ['Any declared a major'], 'y': [undergrad_major[8][1]], 'type': 'bar',
                             'name': undergrad_major[8][0]},
                            {'x': ['Health science'], 'y': [undergrad_major[1][1]], 'type': 'bar',
                             'name': undergrad_major[1][0]},
                        ],
                        'layout': {
                            'title': 'Undergraduate Major'
                        }
                    }
                ),
            ]),
        ]
    else:
        return [
            html.Div(children=[
                dcc.Graph(
                    id='years_since_learning_to_code',
                    figure={
                        'data': [
                            {'x': ['Less then 10 years'], 'y': [years_since_learning_code[0]], 'type': 'bar',
                             'name': 'Less then 10 years'},
                            {'x': ['10 to 19 years'], 'y': [years_since_learning_code[1]], 'type': 'bar',
                             'name': '10 to 19 years'},
                            {'x': ['20 to 29 years'], 'y': [years_since_learning_code[2]], 'type': 'bar',
                             'name': '20 to 29 years'},
                            {'x': ['30 to 39 years'], 'y': [years_since_learning_code[3]], 'type': 'bar',
                             'name': '30 to 39 years'},
                            {'x': ['40 to 49 years'], 'y': [years_since_learning_code[4]], 'type': 'bar',
                             'name': '40 to 49 years'},
                            {'x': ['50 years or more'], 'y': [years_since_learning_code[5]], 'type': 'bar',
                             'name': '50 years or more'},
                        ],
                        'layout': {
                            'title': 'Years Since Learning to Code'
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
