import json
import pandas as pd
from pathlib import Path

# Further optimization could be obtained customizing the report to only compute
# vars dtypes to use less resources.
def load_yprofiling_report():
    '''
    Loads the file 'your_report.json' (stored by default in the same
    directory in which the two python scripts 'ydata_profiling_generator' and
    'psy_data_tool' are stored).
    '''
    report_path = Path("your_report.json")
    try:
        with open(report_path) as f:
            data_profile = json.load(f)
            return data_profile
    except FileNotFoundError:
        print(f"No file called 'your_report.json' was found. Make sure\n"
              "it is located in the same folder as this script.")
    except JSONDecodeError:
        print("This is not a valid JSON document.")
    return None


# Return a dictionary with variables and relative dtype according to
# ydata-profiling.
def build_dtypes_dict(data_profile):
    dtypes_dict = {}
    
    # Check if data_profile was loaded successfully before proceeding.
    if data_profile:
        for variable in data_profile['variables']:
            dtypes_dict[variable] = data_profile['variables'][variable]['type']
        return dtypes_dict
    else:
        print("Failed to load the data profile.")


# "convert_dtypes" is a pandas function, don't use that name or it will
# mask the internal function.
def convert_datatypes(df, report_dtypes):
    # Standardize keys of the report_dtypes dictionary
    standardized_report_dtypes = {
        key.strip().lower().replace(' ', '_').replace('(', '').replace(')', ''): value
        for key, value in report_dtypes.items()
    }
    '''Converts the cleaned pandas.DataFrame dtypes based on a custom mapping'''
    # Define the mapping from custom dtype strings to actual pandas/numpy dtypes.
    # Currently, ydata-profiling recognizes the following types: Boolean,
    # Numerical (actually in the report it's called 'Numeric'), Date, Datetime,
    # Categorical, Time-series, URL, Path, File, Image.
    dtype_mapping = {
        'Boolean': 'bool',
        'Numeric': 'float64',
        'Date': 'datetime64[ns]',
        'DateTime': 'datetime64[ns]',
        'Categorical': 'category',
        'Time-series': 'datetime64[ns]',
        'Text': 'object',
        'URL': 'object',
        'Path': 'object',
        'File': 'object',
        'Image': 'object'
    }

    # Iterate over the dtype_mapping dictionary and convert columns
    for var_name in standardized_report_dtypes.keys():
        try:
            if var_name in df.columns:
                df[var_name] = df[var_name].astype(dtype_mapping[standardized_report_dtypes[var_name]])
            else:
                raise KeyError(f"Column {var_name} not found in DataFrame, probably removed during cleaning.")
        except KeyError as e:
            print(e)
            continue

    return df


# Create Python df copy dataframe to be converted to R's dataframe
# Before creation of the df_r copy of the Pandas df DataFrame, an
# attempt to convert object Categorical variables to string was made.
# Categorical must be made. The conversion of Categorical to string
# is necessary to avoid the error UserWarning: Error while trying to
# convert the column "chronotype". Fall back to string conversion.
# The error is: Converting pandas "Category" series to R factor is
# only possible when categories are strings. 
# Convert Pandas "Category" series to strings.
def adapt_r(df):
    """
    Ensure categorical columns in a Pandas DataFrame have string categories.
    This allows for correct conversion to R's DataFrame where these columns 
    will be treated as factors.

    Parameters:
    df (pd.DataFrame): The input Pandas DataFrame.

    Returns:
    pd.DataFrame: A DataFrame where categorical columns have string categories.
    """
    try:
        # Create a deep copy of the DataFrame to avoid modifying the original
        df_r = df.copy()

        # Convert the categories of all categorical columns to strings
        for column in df_r.select_dtypes(include='category'):
            df_r[column] = df_r[column].cat.rename_categories(str)
        
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None

    return df_r


# A simple ascii chart representing only the changed vars
def represent_dtype_changelog(df, original_dtypes):
    '''Generates a simple ascii chart representing only the changed vars'''
    var_type_changelog = "-----------------------\n"
    var_type_changelog += "Variable conversion log\n"
    var_type_changelog += "-----------------------\n"
    for column in df.columns:
        dtype_before = original_dtypes[column]
        dtype_after = df.dtypes[column]
        if dtype_before != dtype_after:
            var_type_changelog += f"\n{column}: {dtype_before} --> {dtype_after}"
    print(var_type_changelog)
