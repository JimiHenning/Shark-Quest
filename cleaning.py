# Functions
import numpy as np


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


def replace_string_patterns(value, replacements):

    if isinstance(value, str):

        for pattern, result in replacements:
            value = re.sub(pattern, result, value)
        return value

    else:

        return value


def dictionnary_from_json(json_filename):
    with open(json_filename+".json", "r") as json_file:
        data = json.load(json_file)
    return data
