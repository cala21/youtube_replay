from dash import Dash
import dash_bootstrap_components as dbc
from uuid import uuid4
from dash.long_callback import DiskcacheLongCallbackManager

## Diskcache
import diskcache
launch_uid = uuid4()
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(
    cache, cache_by=[lambda: launch_uid], expire=60,
)
# long_callback_manager=long_callback_manager

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SIMPLEX],
    suppress_callback_exceptions=True,
    title="Youtube Replay")
app._favicon = "favicon.ico"
