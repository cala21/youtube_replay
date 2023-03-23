from dash import html
import dash_core_components as dcc
from datetime import datetime

def filter_by_date():
    #Filter pt 1
    return html.Div([
                html.H5(
                    children='Filters by Date:',
                    style = {'text-align' : 'left', 'color' :'gray'}
                ),
                #Date range picker
                html.Div(['Select a date range: ',
                    dcc.DatePickerRange(
                        id='date-picker-sales',
                        start_date=datetime(2021, 1, 1),
                        end_date=datetime.today(),
                        start_date_placeholder_text = 'Start date',
                        display_format='MMM-DD-YYYY',
                        first_day_of_week = 1,
                        end_date_placeholder_text = 'End date',
                        style = {'font-size': '12px','display': 'inline-block', 'border-radius' : '2px', 'border' : '1px solid #ccc', 'color': '#333', 'border-spacing' : '0', 'border-collapse' :'separate'})
                ], style = {'margin-top' : '5px'}
                )

            ],
            style = {'margin-top' : '10px',
                    'margin-bottom' : '5px',
                    'text-align' : 'left',
                    'paddingLeft': 5})