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
    """
    Renames columns in a DataFrame based on a given schema.

    Parameters:
    df (pandas.DataFrame): The DataFrame whose columns are to be renamed.
    schema (dict): A dictionary where keys are the new column names and values are dictionaries 
                   containing the key 'existing_column' which maps to the current column name in the DataFrame.

    Returns:
    pandas.DataFrame: The DataFrame with renamed columns.
    """

    for new_name, parameters in schema.items():
        old_name = parameters.get('existing_column')

        if old_name in df.columns:

            df = df.rename(columns={old_name: new_name})

    return df


def add_columns(df, schema):
    """
    Adds columns to a DataFrame based on a given schema.

    Parameters:
    df (pandas.DataFrame): The DataFrame to which columns will be added.
    schema (dict): A dictionary where keys are column names and values are dictionaries 
                   containing column parameters, such as 'dtype'.

    The function checks if each column specified in the schema is present in the DataFrame.
    If a column is not present, it adds the column to the DataFrame with a default value 
    based on the 'dtype' parameter in the schema. If 'dtype' is 'int64', the default value 
    is 999; otherwise, the default value is NaN.
    """
    for name, parameters in schema.items():
        if name not in df.columns:
            if parameters.get('dtype') == 'int64':
                df[name] = 999
            else:
                df[name] = np.nan


def drop_columns(df, schema):
    """
    Drops columns from a DataFrame that are not present in the given schema.

    Parameters:
    df (pandas.DataFrame): The DataFrame from which columns will be dropped.
    schema (list): A list of column names that should be retained in the DataFrame.

    Returns:
    pandas.DataFrame: The DataFrame with only the columns specified in the schema.
    """

    for column in df.columns:
        if column not in schema:
            df = df.drop(column, axis=1)

    return df


def remove_duplicates(df, schema):
    """
    Remove duplicate rows from a DataFrame based on specified columns.

    Parameters:
    df (pandas.DataFrame): The DataFrame from which duplicates will be removed.
    schema (dict): A dictionary where keys are column names and values are dictionaries 
                   containing parameters. If 'duplicate_pairs' is present in the parameters, 
                   it should be a list of columns to consider for identifying duplicates 
                   along with the key column.

    Returns:
    pandas.DataFrame: The DataFrame with duplicates removed based on the specified columns.
    """

    for column, parameters in schema.items():
        if parameters.get('duplicate_pairs'):
            df = df.drop_duplicates(
                subset=[column]+parameters['duplicate_pairs'])

    return df


def reformat_values(df, replacements):
    """
    Reformat values in a DataFrame based on a replacements dictionary.

    Parameters:
    df (pandas.DataFrame): The DataFrame in which values will be reformatted.
    replacements (dict): A dictionary where keys are column names and values are dictionaries 
                         mapping old values to new values.

    Returns:
    pandas.DataFrame: The DataFrame with reformatted values.
    """
    for col, values in replacements.items():
        df.loc[:, col] = df[col].apply(
            replace_string_patterns, replacements=values)

    return df


def clean_dates(df, schema):
    """
    Clean and format date columns in a DataFrame based on a schema.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing date columns to be cleaned.
    schema (dict): A dictionary where keys are column names and values are dictionaries 
                   containing parameters. If 'dtype' is 'datetime64[ns]', the column will 
                   be converted to datetime, formatted, and forward-filled.

    Returns:
    pandas.DataFrame: The DataFrame with cleaned and formatted date columns.
    """
    for column, parameters in schema.items():
        if parameters['dtype'] == 'datetime64[ns]':
            df[column] = pd.to_datetime(
                df[column], errors='coerce')  # Drops unsavable mess
            df[column] = df[column].dt.strftime('%d-%m-%Y')
            df[column] = df[column].ffill()  # Fills forward to avoid time gaps
    return df


def validate_categories(df, schema: dict, sources: dict):
    """
    Validate and clean categorical columns in a DataFrame based on a schema and sources.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing categorical columns to be validated.
    schema (dict): A dictionary where keys are column names and values are dictionaries 
                   containing parameters. If 'categories' is present, it should be a list 
                   of valid categories or a key to load valid categories from sources.
    sources (dict): A dictionary where keys are source names and values are data sources 
                    to load valid categories from.

    Returns:
    pandas.DataFrame: The DataFrame with validated and cleaned categorical columns.
    """
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
    """
    Convert the text case of string columns in a DataFrame based on a schema.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing string columns to be converted.
    schema (dict): A dictionary where keys are column names and values are dictionaries 
                   containing parameters. If 'text_case' is present, it should be one of 
                   'upper', 'lower', or 'title' to convert the text case accordingly.

    Returns:
    pandas.DataFrame: The DataFrame with converted text case in specified columns.
    """
    for column in df.columns:
        if column in schema and 'text_case' in schema[column]:
            if schema[column]['text_case'] == 'upper':
                df[column] = df[column].str.upper()
            elif schema[column]['text_case'] == 'lower':
                df[column] = df[column].str.lower()
            elif schema[column]['text_case'] == 'title':
                df[column] = df[column].str.title()
    return df
