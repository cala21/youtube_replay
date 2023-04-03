from dash import html
import dash_bootstrap_components as dbc

def header():
    return html.Div( 
        className="app-header",
        children= [
            dbc.Row(html.H1(children="Youtube Replay"), className="title"),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/",active="exact"),
                    dbc.NavLink("History Analysis", href="/history-analysis",active="exact"),
                    dbc.NavLink("Interactive Analysis", href="/interactive-analysis",active="exact"),
                    dbc.NavLink("Login", href="/login",active="exact")

                ],
                pills=True
            )
        ]
)