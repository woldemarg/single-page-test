from typing import List, Union, Optional, Tuple
import pandas as pd
import numpy as np
from dash.development.base_component import Component
import dash_bootstrap_components as dbc
import config as cfg

# %%


def preprocess_dates(row):
    try:
        date_vals = pd.to_datetime(row[['from', 'till']], format=cfg.date_format)
        row['from'] = date_vals[0]
        row['till'] = date_vals[1]
        return row
    except ValueError:
        return None


def make_frame(arr):
    return (pd.DataFrame(
        np.array(arr).reshape(-1, 3),
        columns=['employee', 'from', 'till'])
        .apply(preprocess_dates, axis=1)
        .dropna())
