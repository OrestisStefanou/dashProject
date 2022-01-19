import base64
from base64 import b64encode

import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import config
from database_controllers import csv_excel


def get_callbacks(app):
    @app.callback(
        Output("db-output-message", "children"),
        Output("tables-dropdown", "options"),
        Output("tables-dropdown", "value"),
        Output("database-config", "data"),
        Output("db-connect-loading", "children"),
        Input("db-connect", "n_clicks"),
        State("data_source", "value"),
        State("db-host", "value"),
        State("db-user", "value"),
        State("db-password", "value"),
        State("db-name", "value"),
        prevent_initial_call=True,
    )
    def connect_to_database(n_clicks, data_source, host, user, password, database):
        if n_clicks == 0:
            raise PreventUpdate

        args = {"host": host, "user": user, "password": password, "database": database}
        success = True
        try:
            db_connection_func = config.database_connection_functions[data_source]
            tables_list, db_config = db_connection_func(**args)
            tables_options = [{"label": source, "value": source} for source in tables_list]
            selected_table = tables_list[0]
            output_msg = "Connected successfully"

        except Exception as err:
            success = False
            output_msg = str(err)
            tables_options = None
            selected_table = ""
            db_config = None

        output_msg_component = dbc.Alert(
            output_msg, id="alert-fade", dismissable=True, is_open=True, color="success" if success else "danger"
        )
        # Add db-connect-loading component to output
        return output_msg_component, tables_options, selected_table, db_config, []

    @app.callback(
        Output("db-data", "data"),
        Output("query-loading", "children"),
        Output("query-error", "children"),
        Input("tables-dropdown", "value"),
        Input("run_query_btn", "n_clicks"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        State("query", "value"),
        State("database-config", "data"),
        State("data_source", "value"),
        prevent_initial_call=True,
    )
    def update_db_data(table_name, query_btn_clicks, file_contents, filename, query, db_config, data_source):
        ctx = dash.callback_context
        error = None
        if data_source in config.database_sources:
            execute_query_func = config.database_execute_functions[data_source]
        # If callback function was triggered because user upload a csv/excel file
        if ctx.triggered[0]["prop_id"] == "upload-data.contents":
            if file_contents is None:
                raise PreventUpdate
            df, error = csv_excel.parse_contents(file_contents, filename)

        # If callback function was triggered because user clicked run query button
        elif ctx.triggered[0]["prop_id"] == "run_query_btn.n_clicks":
            if query_btn_clicks == 0:
                raise PreventUpdate
            # Run query button was clicked
            try:
                if data_source in config.database_sources:
                    columns, results = execute_query_func(db_config, query)
                    df = pd.DataFrame(results, columns=columns)
                else:
                    df, error = csv_excel.parse_contents(file_contents, filename)
                    df = df.query(query)
            except Exception as err:
                error = str(err)

        # Callback function was called because user changed the selected database table
        else:
            if table_name == "":
                raise PreventUpdate
            # User selected a table from dropdown menu
            query = f"SELECT * FROM {table_name} LIMIT 1000"
            try:
                columns, results = execute_query_func(db_config, query)
                df = pd.DataFrame(results, columns=columns)
            except Exception as err:
                error = str(err)

        if error:
            error_alert = dbc.Alert(error, id="alert-fade", dismissable=True, is_open=True, color="danger")
            return None, [], error_alert

        return df.to_json(date_format="iso", orient="split"), [], []

    @app.callback(
        Output(component_id="upload-data-div", component_property="style"),
        Output(component_id="database-info-div", component_property="style"),
        Input("data_source", "value"),
    )
    def update_data_source_options(data_source):
        if data_source in config.database_sources:
            return {"display": "none"}, {"display": "block"}
        else:
            return {"display": "block"}, {"display": "none"}

    @app.callback(
        Output("datatable", "children"),
        Input("db-data", "data"),
        prevent_initial_call=True,
    )
    def show_datatable(data):
        if data is None:
            raise PreventUpdate

        df = pd.read_json(data, orient="split")
        datatable = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
        )
        return datatable

    @app.callback(
        Output("plot_x_axis", "options"),
        Output("plot_y_axis", "options"),
        Output("plot_group_by_col", "options"),
        Input("db-data", "data"),
        prevent_initial_call=True,
    )
    def update_plot_dropdowns(data):
        if data is None:
            raise PreventUpdate

        df = pd.read_json(data, orient="split")
        options = [{"label": source, "value": source} for source in list(df.columns)]
        return options, options, options

    @app.callback(
        Output("data_graph", "figure"),
        Input("plot_btn", "n_clicks"),
        State("db-data", "data"),
        State("plot_type", "value"),
        State("plot_x_axis", "value"),
        State("plot_y_axis", "value"),
        State("plot_group_by_col", "value"),
        prevent_initial_call=True,
    )
    def visualize_data(n_clicks, data, plot_type, x_axis_col, y_axis_col, group_by_col):
        if n_clicks == 0:
            raise PreventUpdate

        df = pd.read_json(data, orient="split")
        if x_axis_col not in df.columns:
            raise PreventUpdate  # Maybe show an error for this case

        if y_axis_col not in df.columns:
            raise PreventUpdate

        if group_by_col not in df.columns:
            group_by_col = None

        if plot_type == "scatter":
            fig = px.scatter(
                df,
                x=x_axis_col,
                y=y_axis_col,
                color=group_by_col,
            )
        elif plot_type == "line":
            fig = px.line(
                df,
                x=x_axis_col,
                y=y_axis_col,
                color=group_by_col,
            )
        elif plot_type == "bar":
            fig = px.bar(
                df,
                x=x_axis_col,
                y=y_axis_col,
                color=group_by_col,
            )
        elif plot_type == "pie":
            fig = px.pie(df, values=x_axis_col, names=y_axis_col)
        return fig

    @app.callback(Output("query", "value"), Input("upload-script", "contents"))
    def update_query(file_contents):
        if file_contents is not None:
            _, content_string = file_contents.split(",")
            decoded = base64.b64decode(content_string)
            return decoded.decode("utf-8")

    @app.callback(Output("x_axis_md", "children"), Output("y_axis_md", "children"), Input("plot_type", "value"))
    def update_plot_options(plot_type):
        if plot_type == "pie":
            values_md = "#### Values column"
            names_md = "#### Names column"
            return values_md, names_md
        else:
            values_md = "#### x axis column"
            names_md = "#### y axis column"
            return values_md, names_md

    @app.callback(
        Output("download-figure-png", "data"),
        Input("download-btn", "n_clicks"),
        State("data_graph", "figure"),
        prevent_initial_call=True,
    )
    def download_figure(n_clicks, figure):
        if n_clicks == 0 or figure is None:
            raise PreventUpdate

        fig = go.Figure(data=figure["data"], layout=figure["layout"])

        img_bytes = fig.to_image(format="png")
        encoding = b64encode(img_bytes).decode()

        data = {"base64": True, "content": encoding, "filename": "figure.png", "type": None}
        return data
