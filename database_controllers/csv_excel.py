import base64
import datetime
import io

from dash import dcc
from dash import html
from dash import dash_table

import pandas as pd


def parse_contents(contents, filename):
    """
    Parse the contents of the file that the user uploaded
    and return a tuple with:
    0. A dataframe with the content's data
    1. An error message if something went wrong
    """
    _, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, "File is not in csv of xls format"
    except Exception as e:
        return None, "There was an error processing this file."

    return df, None
