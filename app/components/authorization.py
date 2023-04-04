from dash import html



def login_button():
    return html.Div(
        style={'textAlign': 'center'},
        children=[
        html.A(
        href='authorize',
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

def login_table():
   return html.Table([
        html.Tr([
            html.Td(html.A('Revoke current credentials', href='/revoke')),
            html.Td('Revoke the access token associated with the current user session. After revoking credentials, if you go to the test page, you should see an invalid_grant error.')
        ]),
        html.Tr([
            html.Td(html.A('Clear Flask session credentials', href='/clear')),
            html.Td('Clear the access token currently stored in the user session. After clearing the token, if you login again, you should go back to the auth flow.'),
        ])
    ])

def logout_button():
    return html.Table([
        html.Tr([
            html.Td(html.A('Logout', href='/logout')),
            html.Td('Logout from Google Services')
        ]),
    ])
