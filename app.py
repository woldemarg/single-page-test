import pandas as pd
import numpy as np
from dash import (Dash,
                  callback,
                  html,
                  dcc,
                  Output,
                  Input,
                  # exceptions,
                  ALL)
import dash_bootstrap_components as dbc
from sp_class import ScatterPlot
import callbacks
import utils
import config as cfg

# %%

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    dbc.icons.FONT_AWESOME]

app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           prevent_initial_callbacks=True,
           # suppress_callback_exceptions=True
           )

server = app.server

rng = pd.date_range(start=cfg.min_date, end=cfg.max_date).to_list()

dates = np.random.choice(rng, 80)

empls = np.random.choice([f'employee {i}' for i in range(cfg.NUM_EMPLOYEES)], 80)

df = (pd.DataFrame(
    zip(empls, dates),
    columns=['employee', 'dates'])
    .drop_duplicates()
    .sort_values('employee', ascending=False))

marker_style = {
    'marker': {
        'color': 'blue',
        'size': 8}
}

plot_layout = {
    'showlegend': False,
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)'
}

scatter_plot = ScatterPlot(df, style=marker_style, layout=plot_layout)

# Define layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        # figure=scatter_plot.initial_figure,
                        id='plot')),
                width={'size': 8, 'offset': 2})),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                children=callbacks.create_input_groups(1),
                                id='input-groups-container'),
                            dbc.Button(
                                'add block',
                                id='add-input-group-button',
                            ),
                        ],
                        style={'height': '300px', 'overflowY': 'auto'}
                    )),
                width={'size': 8, 'offset': 2})),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    'submit',
                    id='submit-input-group-button',
                    class_name='my-3'
                ),
                width={'size': 2, 'offset': 2}
            )
        ),
        html.Div([], id='output-container')
    ]
)

# Define callbacks


@callback(
    Output('plot', 'figure'),
    Input({'type': 'input', 'index': ALL}, 'value')
)
def gather_input(values):

    if not any(values):
        # raise exceptions.PreventUpdate
        return scatter_plot.initial_figure

    # data = (pd.DataFrame([
    #     ['Bob', '2023-05-05T10:15', '2023-05-05T10:25'],
    #     ['Alice', '2023-06-05T10:15', '2023-06-05T10:25'],
    #     ['Alice', '2023-06-08T10:25', '2023-06-10T10:35'],
    #     ['Alice', '2023-06-08T10:25', '2023-06-12T10:35']],
    #     columns=['employee', 'from', 'till'])
    #     .apply(preprocess_dates, axis=1)
    #     .dropna())

    data = utils.make_frame(values)

    if data.empty:
        return scatter_plot.initial_figure

    data_melt = (data
                 .melt(
                     id_vars='employee',
                     value_name='dates',
                     var_name='from_till',
                     ignore_index=False)
                 .drop('from_till', axis=1)
                 .assign(dates=lambda x:
                         x['dates'].dt.normalize())
                 .reset_index()
                 .drop_duplicates()
                 .set_index('dates')
                 .sort_index()
                 .groupby(['index', 'employee'], sort=False, as_index=False)
                 .apply(lambda x: x.asfreq('D', method='ffill'))
                 .reset_index(level=1)
                 .drop_duplicates(['employee', 'dates']))

    scatter_plot.update_plot(
        data_melt,
        style={'marker': {'size': 16, 'symbol': 'x-thin-open', 'color': 'red'}})

    return scatter_plot.updated_figure


if __name__ == '__main__':
    app.run_server(debug=True)
