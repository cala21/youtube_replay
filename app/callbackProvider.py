
from dash.dependencies import Input, Output, State
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
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_output(start_date, end_date):
        start_date_string, end_date_string =  utils.parse_date(start_date, end_date)

        return utils.filter_by_date_range(start_date_string, end_date_string)[["date","title"]].to_dict('records')
    
    @app.callback(
    Output('my_graph', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_graph(start_date, end_date):
        data = utils.filter_by_date_range_ads(start_date, end_date)

        return utils.load_graph(data)
    
    @app.callback(
    Output('views-scatter', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))
    def update_scatter(start_date, end_date):
        data = utils.filter_by_date_range(start_date, end_date)

        return utils.load_scatter(data)
            