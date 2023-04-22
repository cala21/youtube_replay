import dash_bootstrap_components as dbc
from dash import html
from components import header

layout = html.Div(
    children=[
        dbc.Row(header.header()),
        html.H1('Welcome to YouTube Replay!', style={'textAlign': 'center'}),
        html.Hr(),
        html.P('YouTube Replay is an interactive data visualization tool that allows you to gain insights from your YouTube watch history. Simply upload your "watch_history.json" file and start exploring!', style={'textAlign': 'justify'}),
        html.H3('Features:', style={'marginTop': '10px'}),
        html.Ul([
            html.Li('Top Watched Videos'),
            html.Li('Videos vs Ads Watched'),
            html.Li('Word Cloud based on History'),
            html.Li('Genres Watched Over Time'),
            html.Li('Popularity of Watched Videos'),
            html.Li('Watched Video - Time of Day Trend'),
            html.Li('Recommendations based on your viewing history and preferences! (not Youtube\'s algorithm)')
        ], style={'textAlign': 'justify', 'marginLeft': '20px', 'marginTop': '10px'}),
        
        html.P("YouTube Replay is being built as a useful tool for researchers and data enthusiasts. The goal of the app is to provide a comprehensive view of your viewing history, including insights and trends.", style={'textAlign': 'justify'}),
        html.P("You can use this data to analyze your viewing habits on YouTube and gain valuable insights into your interests and behaviors.", style={'textAlign': 'justify'}),
        html.P("Whether you're taking a walk down the YouTube memory-lane or analyze your viewing history for research purposes, we hope that YouTube Replay is the perfect tool for you.", style={'textAlign': 'justify'}),
        
        html.Hr(),
        
        html.Div(children=[
            html.P(children=[
                'YouTube Replay was developed as a research project for ',
                html.A('CSE-6242 : Data and Visual Analytics', href='https://poloclub.github.io/cse6242-2021spring-online/'),
                '. by :'
            ]),
            html.Ul(children=[
                html.Li(children=[
                    html.A('Camilla Lambrocco', href='mailto:clambrocco3@gatech.edu'),
                    ' (clambrocco3@gatech.edu)'
                ]),
                html.Li(children=[
                    html.A('Rishabh Berlia', href='mailto:rberlia3@gatech.edu'),
                    ' (rberlia3@gatech.edu)'
                ]),
                html.Li(children=[
                    html.A('Joshua Jalowiec', href='mailto:jjalowiec3@gatech.edu'),
                    ' (jjalowiec3@gatech.edu)'
                ]),
                html.Li(children=[
                    html.A('Christopher Hodge', href='mailto:chodge9@gatech.edu'),
                    ' (chodge9@gatech.edu)'
                ]),
                html.Li(children=[
                    html.A('David Scott', href='mailto:davidscott@gatech.edu'),
                    ' (davidscott@gatech.edu)'
                ]),
            ]),

            html.P(children=[
                'Checkout the project on ',
                html.A('github', href='https://github.com/cala21/youtube_replay'),
                '.'
            ])
        ], className="footer")
    ])
