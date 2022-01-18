from dash import dcc
from dash import html

import config


def get_layout():
    return html.Div(
        [
            dcc.Markdown("# Visualization App", className="text-primary"),
            html.Br(),
            dcc.Markdown("#### Select your data source", className="text-primary"),
            dcc.Dropdown(
                id="data_source",
                options=[{"label": source, "value": source} for source in config.data_sources],
                value="mariadb",
                className="text-primary",
            ),
            html.Br(),
            html.Div(id="data_source_options"),
            # Upload csv/excel div
            html.Div(
                id="upload-data-div",
                children=[
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                        style={
                            "width": "30%",
                            "height": "30px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            # "margin": "10px",
                        },
                        # Don't allow multiple files to be uploaded
                        multiple=False,
                    ),
                ],
                style={"display": "none"},
            ),
            # Database connection info div
            html.Div(
                id="database-info-div",
                children=[
                    dcc.Store(id="database-config"),
                    dcc.Store(id="db-data"),
                    dcc.Input(id="db-host", type="text", placeholder="host"),
                    dcc.Input(
                        id="db-user",
                        type="text",
                        placeholder="user",
                    ),
                    dcc.Input(
                        id="db-password",
                        type="password",
                        placeholder="password",
                    ),
                    dcc.Input(
                        id="db-name",
                        type="text",
                        placeholder="database",
                    ),
                    html.Button(id="db-connect", n_clicks=0, children="Connect", className="btn btn-outline-primary"),
                    dcc.Loading(
                        id="connect-loading-",
                        type="default",
                        children=html.Div(id="db-connect-loading"),
                    ),
                    html.Div(id="db-output-message"),
                    html.Br(),
                    dcc.Markdown("##### Tables", className="text-primary"),
                    dcc.Dropdown(id="tables-dropdown", className="text-primary"),
                ],
                style={"display": "none"},
            ),
            html.Br(),
            dcc.Markdown("##### Upload a script", className="text-primary"),
            html.Br(),
            dcc.Upload(
                id="upload-script",
                children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                style={
                    "width": "30%",
                    "height": "30px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    # "margin": "10px",
                },
                multiple=False,
            ),
            html.Br(),
            dcc.Markdown("#### Or Write your query in the textbox below", className="text-primary"),
            dcc.Textarea(id="query", value="", style={"width": "100%", "height": 100}, className="text-primary"),
            html.Button(id="run_query_btn", n_clicks=0, children="Run query", className="btn btn-outline-primary"),
            html.Div(id="query-error"),
            dcc.Loading(id="query-loading"),
            html.Div(id="datatable"),
            html.Br(),
            dcc.Markdown("### Visualize the results", className="text-primary"),
            html.Div(
                [
                    dcc.Markdown("#### Plot type", className="text-primary"),
                    dcc.Dropdown(
                        id="plot_type",
                        options=[{"label": source, "value": source} for source in ["scatter", "line", "bar", "pie"]],
                        value="scatter",
                        className="text-primary",
                    ),
                    html.Br(),
                    dcc.Markdown(id="x_axis_md", children="#### x axis column", className="text-primary"),
                    dcc.Dropdown(id="plot_x_axis", className="text-primary"),
                    html.Br(),
                    dcc.Markdown(id="y_axis_md", children="#### y axis column", className="text-primary"),
                    dcc.Dropdown(id="plot_y_axis", className="text-primary"),
                    html.Br(),
                    dcc.Markdown("#### Group by column", className="text-primary"),
                    dcc.Dropdown(id="plot_group_by_col", className="text-primary"),
                    html.Br(),
                    html.Button(id="plot_btn", n_clicks=0, children="Plot", className="btn btn-outline-primary"),
                    dcc.Graph(id="data_graph"),
                    html.Button(
                        id="download-btn", n_clicks=0, children="Download figure", className="btn btn-outline-primary"
                    ),
                    dcc.Download(id="download-figure-png"),
                ],
            ),
        ],
    )
