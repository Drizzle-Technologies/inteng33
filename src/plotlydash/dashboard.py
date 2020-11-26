"""Instantiate a Dash app."""
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from .layout import html_layout

from .data import create_ID_devices_options, create_occupancy_dataframe, create_table_dataframe, set_table_columns


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    # Dash app is created binded to the route '/' and the flask app.
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/',
        update_title=None,
        assets_folder='static'
    )

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Gets all the devices IDs
    device_ids = create_ID_devices_options()

    # Defines the options for the number of observations desired in the graph
    n_lines_options = [{"label": "5", "value": 5}, {"label": "10", "value": 10}, {"label": "25", "value": 25},
                       {"label": "50", "value": 50}, {"label": "100", "value": 100}]

    # Creates the devices table dataframe
    df = create_table_dataframe()

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.Div(children=[
                    html.Label(
                        'Insira um ID de dispositivo',
                        htmlFor='device-id'
                    ),
                    # Choose a device to be displayed in the graph
                    dcc.Dropdown(
                        id='device-id',
                        options=[{"label": ID, "value": ID} for ID in device_ids],
                        placeholder='id',
                        searchable=False,
                        className='w-40',
                    ),
                ]),
                html.Div(children=[
                    html.Label(
                        'Número de Observações',
                        htmlFor='device-nlines'
                    ),
                    # Choose the number of observations to be displayed on the graph
                    dcc.Dropdown(
                        id='device-nlines',
                        options=n_lines_options,
                        placeholder='obs',
                        searchable=False,
                        className='w-40',
                    ),
                ])
            ], className="d-flex w-60 justify-content-around"),
            html.Div(children=[
                # Occupancy record graph
                dcc.Graph(
                    id='device-graph'
                ),
                # Uploaded every 10 seconds
                dcc.Interval(
                    id='update-graph',
                    interval=10**4,
                    n_intervals=0
                )
            ],
                    className='mb-5'
            ),
            html.Div(
                children=[
                    # Devices table
                    dash_table.DataTable(
                        id='devices-table',
                        columns=set_table_columns(df),
                        data=df.to_dict('records'),
                        sort_action='native',
                        style_data_conditional=[
                            # Colors the device's row if the current number of people exceeds a treshold
                            {
                                'if': {
                                    'filter_query': '{current_occupancy} > {max_people_alert}',
                                },
                                'backgroundColor': '#fff3cd',
                                'color': '#856404',
                            },
                            {
                                'if': {
                                    'filter_query': '{current_occupancy} > {max_people}',
                                },
                                'backgroundColor': '#f8d7da',
                                'color': '#721c24',
                            },
                        ],
                    ),
                    # Update table every 5 seconds
                    dcc.Interval(
                        id='update-table',
                        interval=5*10**3,
                        n_intervals=0
                    )
                ]
            )
        ]
    )

    @dash_app.callback(
        Output('device-graph', 'figure'),
        [Input('device-id', 'value'), Input('device-nlines', 'value'), Input('update-graph', 'n_intervals')]
    )
    def update_graph(ID_device, n_lines, n):
        """Callback updates graph every ten seconds"""

        # Gets the occupancy dataframe
        occupancy_record = create_occupancy_dataframe(ID_device, n_lines=n_lines)

        # Creates plotly figure
        fig = go.Figure()

        # If a device ID is chosen in the dropdown
        if ID_device:
            # Adds a line with the occupancy record of the device
            fig.add_trace(go.Scatter(x=occupancy_record["timestamp"], y=occupancy_record["occupancy"],
                                     mode='lines+markers',
                                     name='lines+markers',))

        fig.update_layout(xaxis_title='Data e Hora', yaxis_title=f'Número de pessoas',
                          title=dict(text='Ocupação do estabelecimento', x=0.5, font={'size': 15}))
        fig.update_xaxes(nticks=10, showgrid=True)
        fig.update_yaxes(showgrid=True)

        # returns plotly graph
        return fig

    @dash_app.callback(
        Output('devices-table', 'data'),
        [Input('update-table', 'n_intervals')]
    )
    def update_table(n):
        """Callback updates table every 5 seconds"""

        # Updates table dataframe
        devices_df = create_table_dataframe()

        # returns the dataframe as a dictionary
        return devices_df.to_dict('records')

    # returns dashapp
    return dash_app.server
