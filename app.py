# -*- coding: utf-8 -*-
from os import path
import sqlite3
from ast import literal_eval
import os.path

import dash
import dash_core_components as dcc
import dash_html_components as html
import wget
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, g

DATABASE = './db.sqlite3'


def init_db():
    if not path.exists(DATABASE):
        url = 'http://51.38.133.46:9000/dash/db.sqlite3'
        wget.download(url)

    return True


init_db()

server = Flask('Dash')
server.secret_key = os.environ.get('SECRET_KEY', 'secret123')

external_stylesheets = [dbc.themes.DARKLY]

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)


def get_db() -> sqlite3.Connection:
    """
    Create connection to database and return it

    :return: Database connection
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@server.teardown_appcontext
def close_connection(exception) -> None:
    """
    Close connections on server teardown

    :param exception: Decorator param
    :return: Nothing
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_data(query: str) -> list:
    """
    Execute given query in database and return result

    :param query: Sql query to database
    :return: List with database data
    """
    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


with server.app_context():
    hobbyist = get_data('SELECT Hobbyist, COUNT(Hobbyist) FROM data GROUP BY Hobbyist')
    never = get_data('SELECT * FROM data WHERE OpenSourcer = "Never"')
    open_source = get_data('SELECT OpenSourcer, COUNT(OpenSourcer) FROM data GROUP BY OpenSourcer')
    student = get_data('SELECT Student, COUNT(Student) FROM data WHERE Student != "NA" GROUP BY Student')
    developer_full_stack = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, full-stack%"')
    developer_back_end = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, back-end%"')
    developer_front_end = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, front-end%"')
    developer_desktop = get_data(
        'SELECT DevType FROM data WHERE DevType LIKE "%Developer, desktop or enterprise applications%"')
    developer_mobile = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, mobile%"')
    developer_test = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, QA or test%"')
    developer_game_graphics = get_data('SELECT DevType FROM data WHERE DevType LIKE "%Developer, game or graphics%"')
    educational = get_data('SELECT EDLevel, COUNT(EDlevel) FROM data WHERE EDLevel != "NA" GROUP BY EDLevel')
    undergrad_major = get_data(
        'SELECT UndergradMajor, COUNT(UndergradMajor) FROM data WHERE UndergradMajor != "NA" GROUP BY UndergradMajor')
    years_code = get_data('SELECT YearsCode, COUNT(YearsCode) FROM data WHERE YearsCode != "NA" GROUP BY YearsCode')
    years_code_pro = get_data(
        'SELECT YearsCodePro, COUNT(YearsCodePro) FROM data WHERE YearsCodePro != "NA" GROUP BY YearsCodePro')

all_developers = len(developer_full_stack) + len(developer_back_end) + len(developer_front_end) \
                 + len(developer_desktop) + len(developer_mobile) + len(developer_test) + len(developer_game_graphics)

all_open_source = 0
for i in range(len(open_source)):
    all_open_source += open_source[i][1]

all_educational = 0
for i in range(len(educational)):
    all_educational += educational[i][1]

years_since_learning_code = []
years_coding_professionally = []


def add_years(start: int, end: int) -> None:
    """

    :param start: First year used in range
    :param end: Last year ending range for
    :return: Nothing
    """
    if start > end:
        ValueError("Start year must be before end year.")

    years = 0

    for i in range(start, end):
        years += years_code[i][1]

    years_since_learning_code.append(years)


def add_years_pro(start: int, end: int) -> None:
    """

    :param start: First year used in range
    :param end: Last year ending range for
    :return: Nothing
    """
    if start > end:
        ValueError("Start year must be before end year.")

    years = 0

    for i in range(start, end):
        years += years_code_pro[i][1]

    years_coding_professionally.append(years)


less_then_10 = years_code[0][1] + years_code[11][1] + years_code[22][1] + years_code[33][1] + years_code[44][1] \
               + years_code[46][1] + years_code[47][1] + years_code[48][1] + years_code[49][1] + years_code[50][1]
years_since_learning_code.append(less_then_10)

add_years(1, 11)
add_years(12, 22)
add_years(23, 33)
add_years(34, 44)

years_since_learning_code.append(years_code[45][1] + years_code[51][1])

less_then_10_pro = years_code_pro[0][1] + years_code_pro[11][1] + years_code_pro[22][1] + years_code_pro[33][1] + \
                   years_code_pro[44][1] + years_code_pro[46][1] + years_code_pro[47][1] + years_code_pro[48][1] \
                   + years_code_pro[49][1] + years_code_pro[50][1]
years_coding_professionally.append(less_then_10_pro)

add_years_pro(1, 11)
add_years_pro(12, 22)
add_years_pro(23, 33)
add_years_pro(34, 44)

years_coding_professionally.append(years_code_pro[45][1] + years_code_pro[51][1])

categories = [
    dbc.DropdownMenuItem('Developer Roles', id='developer_roles'),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem('Education', id='education'),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem('Experience', id='experience')
]

colors = {
    'first_background': '#000000',
    'second_background': '#212121',
    'text_color': '#FFFFFF',
}

app.layout = html.Div(children=[

    html.Div(children=[
        dbc.NavbarSimple(children=[
            dbc.DropdownMenu(categories, label='Categories', color='secondary')
        ],
            brand='Developer Profile',
            color='dark',
            dark='True',
        ),
    ]),

    html.Div(id='content')
])


@app.callback(
    Output('content', 'children'),
    [
        Input('developer_roles', 'n_clicks'),
        Input('education', 'n_clicks'),
        Input('experience', 'n_clicks')
    ]
)
def update_content(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        category_name = 'developer_roles'
    else:
        category_name = ctx.triggered[0]['prop_id'].split('.')[0]
    if category_name == 'developer_roles':
        return [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='developer_type',
                                figure={
                                    'data': [
                                        {'x': ['Full-stack'], 'y': [(len(developer_full_stack) / all_developers) * 100],
                                         'type': 'bar', 'name': 'Developer, full-stack'},
                                        {'x': ['Back-end'], 'y': [(len(developer_back_end) / all_developers) * 100],
                                         'type': 'bar', 'name': 'Developer, back-end'},
                                        {'x': ['Front-end'], 'y': [(len(developer_front_end) / all_developers) * 100],
                                         'type': 'bar', 'name': 'Developer, front-end'},
                                        {'x': ['Desktop or enterprise applications'],
                                         'y': [(len(developer_desktop) / all_developers) * 100], 'type': 'bar',
                                         'name': 'Developer, desktop or enterprise applications'},
                                        {'x': ['Mobile'], 'y': [(len(developer_mobile) / all_developers) * 100],
                                         'type': 'bar', 'name': 'Developer, mobile'},
                                        {'x': ['QA or test'], 'y': [(len(developer_test) / all_developers) * 100],
                                         'type': 'bar', 'name': 'Developer, QA or test'},
                                        {'x': ['Game or graphics'],
                                         'y': [(len(developer_game_graphics) / all_developers) * 100],
                                         'type': 'bar', 'name': 'Developer, game or graphics'},
                                    ],
                                    'layout': {
                                        'title': 'Developer Type (%)',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='hobbyist',
                                figure={
                                    'data': [
                                        {
                                            'values': [hobbyist[1][1], hobbyist[0][1]],
                                            'type': 'pie',
                                            'labels': [hobbyist[1][0], hobbyist[0][0]],
                                        },
                                    ],
                                    'layout': {
                                        'title': 'Coding as a Hobby',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='open_sourcer',
                                figure={
                                    'data': [
                                        {'x': [open_source[0][0]], 'y': [(open_source[0][1] / all_open_source) * 100],
                                         'type': 'bar', 'name': open_source[0][0]},
                                        {'x': [open_source[1][0]], 'y': [(open_source[1][1] / all_open_source) * 100],
                                         'type': 'bar', 'name': open_source[1][0]},
                                        {'x': [open_source[2][0]], 'y': [(open_source[2][1] / all_open_source * 100)],
                                         'type': 'bar', 'name': open_source[2][0]},
                                        {'x': [open_source[3][0]], 'y': [(open_source[3][1] / all_open_source * 100)],
                                         'type': 'bar', 'name': open_source[3][0]},
                                    ],
                                    'layout': {
                                        'title': 'Contributing to Open Source (%)',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            )
        ]
    elif category_name == 'education':
        return [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='student',
                                figure={
                                    'data': [
                                        {
                                            'values': [student[0][1], student[1][1], open_source[2][1]],
                                            'type': 'pie',
                                            'labels': [student[0][0], student[1][0], student[2][0]],
                                        },
                                    ],
                                    'layout': {
                                        'title': 'How Many Developers are Students?',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='educational_attainment',
                                figure={
                                    'data': [
                                        {'x': ['Any formal education'],
                                         'y': [(educational[2][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Any formal education'},
                                        {'x': ['Primary school'], 'y': [(educational[5][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Primary school'},
                                        {'x': ['Secondary school'], 'y': [(educational[7][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Secondary school'},
                                        {'x': ['Some college'], 'y': [(educational[8][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Some college'},
                                        {'x': ['Associate degree'], 'y': [(educational[0][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Associate degree'},
                                        {'x': ["Bachelor's degree"], 'y': [(educational[1][1] / all_educational) * 100],
                                         'type': 'bar', 'name': "Bachelor's degree"},
                                        {'x': ['Master degree'], 'y': [(educational[3][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Master degree'},
                                        {'x': ['Professional degree'],
                                         'y': [(educational[6][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Professional degree'},
                                        {'x': ['Doctoral degree'], 'y': [(educational[4][1] / all_educational) * 100],
                                         'type': 'bar', 'name': 'Doctoral degree'},
                                    ],
                                    'layout': {
                                        'title': 'Educational Attainment (%)',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='undergraduate_major',
                                figure={
                                    'data': [
                                        {
                                            'values': [undergrad_major[6][1], undergrad_major[5][1],
                                                       undergrad_major[9][1],
                                                       undergrad_major[11][1], undergrad_major[3][1],
                                                       undergrad_major[10][1],
                                                       undergrad_major[10][1], undergrad_major[0][1],
                                                       undergrad_major[2][1],
                                                       undergrad_major[4][1], undergrad_major[7][1],
                                                       undergrad_major[8][1],
                                                       undergrad_major[1][1]],
                                            'type': 'pie',
                                            'labels': [undergrad_major[6][0], undergrad_major[5][0],
                                                       undergrad_major[9][0],
                                                       undergrad_major[11][0], undergrad_major[3][0],
                                                       undergrad_major[10][0],
                                                       undergrad_major[10][0], undergrad_major[0][0],
                                                       undergrad_major[2][0],
                                                       undergrad_major[4][0], undergrad_major[7][0],
                                                       undergrad_major[8][0],
                                                       undergrad_major[1][0]],
                                        },
                                    ],
                                    'layout': {
                                        'title': 'Undergraduate Major',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            ),
        ]
    else:
        return [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='years_since_learning_to_code',
                                figure={
                                    'data': [
                                        {
                                            'values': [years_since_learning_code[0], years_since_learning_code[1],
                                                       years_since_learning_code[2], years_since_learning_code[3],
                                                       years_since_learning_code[4], years_since_learning_code[5]],
                                            'type': 'pie',
                                            'labels': ['Less then 10 years', '10 to 19 years', '20 to 29 years',
                                                       '30 to 39 years',
                                                       '40 to 49 years', '50 years or more'],
                                        },
                                    ],
                                    'layout': {
                                        'title': 'Years Since Learning to Code',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(children=[
                            dcc.Graph(
                                id='years_coding_professionally',
                                figure={
                                    'data': [
                                        {
                                            'values': [years_coding_professionally[0], years_coding_professionally[1],
                                                       years_coding_professionally[2], years_coding_professionally[3],
                                                       years_coding_professionally[4], years_coding_professionally[5]],
                                            'type': 'pie',
                                            'labels': ['Less then 10 years', '10 to 19 years', '20 to 29 years',
                                                       '30 to 39 years',
                                                       '40 to 49 years', '50 years or more'],
                                        },
                                    ],
                                    'layout': {
                                        'title': 'Years Coding Professionally',
                                        'plot_bgcolor': colors['second_background'],
                                        'paper_bgcolor': colors['second_background'],
                                        'font': {
                                            'color': colors['text_color']
                                        }
                                    }
                                }
                            ),
                        ]),
                    ]
                ),
                style={'backgroundColor': colors['first_background']}
            )
        ]


if __name__ == '__main__':
    app.run_server(
        debug=literal_eval(os.environ.get('DEBUG', 'True')),
        host=os.environ.get('HOST', '0.0.0.0'),
        port=literal_eval(os.environ.get('PORT', '8000'))
    )
