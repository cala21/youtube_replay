from dash import html
import dash_bootstrap_components as dbc

def header():
    return html.Div( 
        className="app-header",
        children= [
            dbc.Row(html.H1(children="Youtube Replay"), className="title"),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/"),
                    dbc.NavLink("History Analysis", href="/history-analysis"),
                    dbc.NavLink("Interactive Analysis", href="/interactive-analysis")
                ]
            )
        ]
)