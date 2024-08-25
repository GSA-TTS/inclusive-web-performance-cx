"""
Loads result to dataframe
"""

import os
import pandas as pd


def load_results_to_dataframe(**kwargs):
    """load results to dataframe"""
    file_path = os.path.join(kwargs["notebook_dir"], kwargs["file_name"])
    return pd.read_csv(file_path)
