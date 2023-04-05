from dash import html
from dash import dcc
from datetime import datetime

def filter_by_date(min, max):
    #Filter pt 1
    return html.Div([
                html.H5(
                    children='Filters by Date:',
                    style = {'textAlign' : 'left', 'color' :'gray'}
                ),
                #Date range picker
                html.Div(['Select a date range: ',
                    dcc.DatePickerRange(
                        id='date-picker',
                        min_date_allowed=min,
                        max_date_allowed=max,
                        start_date_placeholder_text = 'Start date',
                        display_format='MMM-DD-YYYY',
                        first_day_of_week = 1,
                        end_date_placeholder_text = 'End date',
                        style = {'fontSize': '12px','display': 'inline-block', 'borderRadius' : '2px', 'border' : '1px solid #ccc', 'color': '#333', 'borderSpacing' : '0', 'borderCollapse' :'separate'}
                        ),
                        html.Div(id='output-container-date-picker')
                ], style = {'marginTop' : '5px'}
                )

            ],
            style = {'marginTop' : '10px',
                    'marginBottom' : '5px',
                    'textAlign' : 'left',
                    'paddingLeft': 5})