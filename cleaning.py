import json
import re
import numpy as np
import pandas as pd


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
        with open(json_filename + ".json", "r", encoding="utf-8") as json_file:
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


def rename_columns(df, schema):

    for new_name, parameters in schema.items():
        old_name = parameters.get('existing_column')

        if old_name in df.columns:

            df = df.rename(columns={old_name: new_name})

    return df


def add_columns(df, schema):
    for name, parameters in schema.items():
        if name not in df.columns:
            if parameters.get('dtype') == 'int64':
                df[name] = 999
            else:
                df[name] = np.nan


def drop_columns(df, schema):

    for column in df.columns:
        if column not in schema:
            df = df.drop(column, axis=1)

    return df


def remove_duplicates(df, schema):

    for column, parameters in schema.items():
        if parameters.get('duplicate_pairs'):
            df = df.drop_duplicates(
                subset=[column]+parameters['duplicate_pairs'])

    return df


def reformat_values(df, replacements):

    for col, values in replacements.items():

        df.loc[:, col] = df[col].apply(
            replace_string_patterns, replacements=values)

    return df


def clean_dates(df, schema):
    for column, parameters in schema.items():
        if parameters['dtype'] == 'datetime64[ns]':
            df[column] = pd.to_datetime(
                df[column], errors='coerce')  # Drops unsavable mess
            df[column] = df[column].dt.strftime('%d-%m-%Y')
            df[column] = df[column].ffill()  # Fills forward to avoid time gaps
    return df


def validate_categories(df, schema: dict, sources: dict):

    for column in df.select_dtypes(include=['category']).columns:

        valid_categories = schema[column]['categories']
        default_category = schema[column].get('default_category', np.nan)

        if isinstance(valid_categories, str):
            valid_categories = load_data(
                sources[valid_categories]).iloc[:, 0].tolist() + [default_category]

        df[column] = df[column].astype('string')
        df[column] = pd.Categorical(
            df[column], categories=set(valid_categories), ordered=True)
        df[column] = df[column].where(df[column].isin(
            valid_categories), other=default_category)

        df[column] = df[column].astype('category')
    return df


def convert_text_case(df, schema):
    for column in df.columns:
        if column in schema and 'text_case' in schema[column]:
            if schema[column]['text_case'] == 'upper':
                df[column] = df[column].str.upper()
            elif schema[column]['text_case'] == 'lower':
                df[column] = df[column].str.lower()
            elif schema[column]['text_case'] == 'title':
                df[column] = df[column].str.title()
    return df
