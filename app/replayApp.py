from dash import Dash
import dash_bootstrap_components as dbc
from uuid import uuid4
from dash.long_callback import DiskcacheLongCallbackManager

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SIMPLEX],
    suppress_callback_exceptions=True,
    title="Youtube Replay")
app._favicon = "favicon.ico"
