from dash import (callback,
                  html,
                  Output,
                  Input,
                  State,
                  exceptions,
                  MATCH,
                  ALL)
import dash_bootstrap_components as dbc
import config as cfg
import utils

# %%


def create_input_group(identifier):

    select_options = [{"label": f"employee {i}", "value": f"employee {i}"}
                      for i in range(cfg.NUM_EMPLOYEES)]

    input_group = html.Div(
        dbc.InputGroup(
            [
                dbc.InputGroupText('block'),
                dbc.Select(
                    options=select_options,
                    placeholder='select',
                    id={'type': 'input', 'index': f'{identifier}-employee'}
                ),
                dbc.InputGroupText('from'),
                dbc.Input(
                    type='datetime-local',
                    id={'type': 'input', 'index': f'{identifier}-from'},
                    min=cfg.min_date_str,
                    max=cfg.max_date_str,
                    debounce=True
                ),
                dbc.InputGroupText('till'),
                dbc.Input(
                    type='datetime-local',
                    id={'type': 'input', 'index': f'{identifier}-till'},
                    min=cfg.min_date_str,
                    max=cfg.max_date_str,
                    debounce=True
                ),
                dbc.Button(
                    html.I(className='fa fa-trash'),
                    id={'type': 'clear-button', 'index': identifier}
                )
            ],
            class_name='my-3',
        ),
        id={'type': 'group-holder', 'index': identifier}
    )

    return input_group


def create_input_groups(num_groups):
    input_groups = []
    for i in range(1, num_groups + 1):
        input_groups.append(create_input_group(str(i)))
    return input_groups

# %%


@callback(
    Output({'type': 'group-holder', 'index': MATCH}, 'children'),
    Input({'type': 'clear-button', 'index': MATCH}, 'n_clicks')
)
def remove_input_groups(n_clicks):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    return []


@callback(
    Output('input-groups-container', 'children'),
    Input('add-input-group-button', 'n_clicks'),
    State('input-groups-container', 'children')
)
def add_input_groups(n_clicks, children):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    children.append(create_input_group(str(len(children)+1)))
    return children


@callback(
    Output('output-container', 'children'),
    Input('submit-input-group-button', 'n_clicks'),
    State({'type': 'input', 'index': ALL}, 'value')
)
def submit_input(n_clicks, values):

    if not n_clicks:
        raise exceptions.PreventUpdate

    data = utils.make_frame(values)

    return dbc.Row(dbc.Col(
        dbc.Table.from_dataframe(
            data,
            striped=True,
            bordered=True,
            hover=True),
        width={'size': 6, 'offset': 3}))
