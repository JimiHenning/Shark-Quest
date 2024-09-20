import json
import re
import numpy as np
import pandas as pd


def merge_values(row, arg1, *args):
    if row in args:
        return arg1
    else:
        return row


def strip_values(df):
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x)
    return df


def replace_to_nan(series, keys, value=np.nan):
    """
    input series as dataframe['Column']
    input keys as a list of all the keys to replace
    input value as the replacer value for the keys, default is NaN
    """

    return series.replace(keys, value, inplace=True)


def categorize_activity(activity):
    if pd.isna(activity):
        return "Invalid"

    activity = activity.lower()

    for pattern, label in categories:
        if re.search(pattern, activity):
            return label

    return "Other Activity"


# Valid functions :

def load_data(filename):
    """
    Load data from an Excel or CSV file.

    Parameters:
    filename (str): The name of the file to load. The file should be located in the 'sources' directory.
                    The function supports files with '.xls' and '.csv' extensions.

    Returns:
    DataFrame or None: Returns a pandas DataFrame if the file is successfully loaded.
                       Returns None if the file extension is not supported.
    """
    if filename.endswith('.xls'):
        return pd.read_excel('sources/'+filename)
    elif filename.endswith('.csv'):
        return pd.read_csv('sources/'+filename)
    else:
        return None


def get_json(json_filename):
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        json_filename (str): The name of the JSON file (without the .json extension).

    Returns:
        dict: The contents of the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    try:
        with open(json_filename + ".json", "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {json_filename}.json does not exist.")
        raise
    except json.JSONDecodeError:
        print(f"Error: The file {json_filename}.json is not a valid JSON.")
        raise


def replace_string_patterns(value, replacements):
    """
    Replaces string patterns in the given value based on the provided replacements.

    Args:
        value (str): The string in which patterns will be replaced.
        replacements (list of lists): A list of lists where each list contains a pattern and its replacement string.

    Returns:
        str: The modified string with patterns replaced if the input is a string.
        If the input is not a string, it returns the input value unchanged.

    """
    try:
        if isinstance(value, str):
            for pattern, result in replacements:
                value = re.sub(pattern, result, value)
            return value
        else:
            return value
    except re.error as e:
        print(f"Regex error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
