from dash import html


def login_button():
    return html.Div(
        style={'textAlign': 'center'},
        children=[
        html.A(
        href='google/',
        className='login-btn',
        style={'textDecoration': 'none'},
        children=[
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png',
                style={'width': '50px', 'height': '50px'},
                alt='Google'
            ),
            html.Div(
                className='btn-text',
                children='Login with Google'
            )
        ]
    )
])