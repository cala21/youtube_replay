from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html


def header():
    return html.Div( 
        className="sidebar-style",
        children= [
            #dbc.Row(html.H1(children="Youtube Replay"), className="title"),
            html.Img(src='assets/youtube_replay.png', style={'height':'8%', 'width':'100%'}),
            html.Hr(),
            html.P(
                "Uncover insights and trends with YouTube Replay - the ultimate research tool for analyzing your viewing history.", className="side-nav-font"
            ),
            html.Hr(),

            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/",active="exact"),
                    dbc.NavLink("How To Use?", href="/help-page",active="exact"),
                    dbc.NavLink("History Analysis", href="/history-analysis",active="exact"),
                    dbc.NavLink("Personalized Recommendations", href="/recommendations",active="exact"),
                ],
                pills=True,
                vertical=True,
            ),
            html.Hr(),
            html.Div(children=[
                html.P(children=[
                'Copyright ',
                html.Span('©', className='copy'),
                ' 2023 YouTube Replay.', 
                html.Br(),
                'Licensed under the ',
                html.A('MIT License', href='https://opensource.org/licenses/MIT'),
                '.'
                ])
                ], className='footer'
            )
    ])