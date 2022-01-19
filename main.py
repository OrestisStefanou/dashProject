import dash
import dash_bootstrap_components as dbc

from layouts import main_page_layout
from callbacks import main_page_callbacks


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.PULSE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

main_page_callbacks.get_callbacks(app)

app.layout = main_page_layout.get_layout()

if __name__ == "__main__":
    app.run_server(debug=False)
