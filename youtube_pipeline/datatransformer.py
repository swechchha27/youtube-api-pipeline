"""This python scripts contains all transformation methods
used in the pipeline."""
import pandas as pd


def convert_to_dataframe(data, columns=None):
    """
    Convert a list of dictionaries to a pandas DataFrame.
    :param data: List of dictionaries to convert.
    :param columns: List of columns to include in the DataFrame. 
                    If None passed, return all columns.
    :return: A pandas DataFrame.
    """
    # If no columns are specified, use all keys from the first dictionary
    if columns is None:
        columns = data[0].keys() if data else []

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data, columns=columns)

    # Convert 'publishedAt' column to datetime format
    if df.get('publishedAt') is not None:
        df['publishedAt'] = pd.to_datetime(df['publishedAt'])

    return df