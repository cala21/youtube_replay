
from dash.dependencies import Input, Output, State
from  dateutil import parser
from utils import Utils

def get_callbacks(app):
    utils = Utils()

    @app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [
                utils.parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children

    @app.callback(
    Output('history-table', 'data'),
    Input('date-picker-history', 'start_date'),
    Input('date-picker-history', 'end_date'))
    def update_output(start_date, end_date):
        start_date_string = None
        end_date_string = None
        if start_date is not None:
            start_date_object = parser.isoparse(start_date)
            start_date_string = start_date_object.strftime('%B %d, %Y')
        if end_date is not None:
            end_date_object = parser.isoparse(end_date)
            end_date_string = end_date_object.strftime('%B %d, %Y')

        return utils.filter_by_date_range(start_date_string, end_date_string)
            