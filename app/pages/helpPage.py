import dash_bootstrap_components as dbc
from dash import dcc, html
from components import header


layout = html.Div(children=[
    html.H1(children="How to use the YouTube Replay app"),
    html.Hr(),
    html.H4(children='Part 1 : How to Get a Copy of Your YouTube History'),
    
    html.P(children='Your YouTube history is available through Google Takeout, a tool that Google provides to consult practically the history and stored data of any of the products that you have used. Follow these steps to get a copy of your YouTube history:'),
    
    html.Ol(children=[
        html.Li(children=[
            'Go to ',
            html.A(children='https://takeout.google.com/settings/takeout', href='https://takeout.google.com/settings/takeout'),
            ' and log in with your personal account.'
        ]),
        html.Li(children=[
            'Click on "Deselect All" to unselect all products.',
            html.Img(src='assets/deselect_all.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Scroll all the way down to "YouTube and YouTube Music".'),
            html.Img(src='assets/scroll_to_youtube.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Select JSON format and make sure to just select "history" via the "All YouTube data included" link.'),
            html.Img(src='assets/select_history.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Click on "Next" and follow the steps to request the download of your YouTube history.'),
            html.Img(src='assets/final_step.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Once the file is generated, you will receive a notification email. Click on the link provided in the email to download your file.'),
            #html.Img(src='assets/notification_email.png', width=500)
        ]),
        html.Li(children='For security, the file has an expiration date, so make sure to download it before the date indicated in the email.')
    ]),
    
    html.P(children="That's it! Once you have downloaded your YouTube history file, you can upload it to YouTube Replay and start exploring your data."),
    html.Hr(),
    html.H4(children='Part 2 : How to use History Analysis'),
    html.Hr(),
    html.H4(children='Part 3 : How to get Personalized Recommendations'),


], style={'max-width': '800px', 'margin': '0 auto'})
