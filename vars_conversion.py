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
    return none


# Return a dictionary with variables and relative dtype according to ydata-profiling.
def build_dtypes_dict(data_profile):
    dtypes_dict = {}
    
    # Check if data_profile was loaded successfully before proceeding.
    if data_profile:
        for variable in data_profile['variables']:
            dtypes_dict[variable] = data_profile['variables'][variable]['type']
        return dtypes_dict
    else:
        print("Failed to load the data profile.")


def convert_dtypes(df, report_dtypes):
    # Standardize keys of the report_dtypes dictionary
    report_dtypes = {
        key.strip().lower().replace(' ', '_').replace('(', '').replace(')', ''): value
        for key, value in report_dtypes.items()
    }
    '''Converts the cleaned pandas.DataFrame dtypes based on a custom mapping'''
    # Define the mapping from custom dtype strings to actual pandas/numpy dtypes
    dtype_mapping = {
        'Numeric': 'float64',
        'Categorical': 'category',
        'Text': 'object'
    }

    # Iterate over the dtype dictionary and convert columns
    for column, dtype in report_dtypes.items():
        try:
            if column in df.columns:
                if dtype in dtype_mapping:
                    if dtype_mapping[dtype] == 'category':
                        df[column] = df[column].astype('category')
                    else:
                        df[column] = pd.to_numeric(df[column], errors='coerce') if dtype == 'Numeric' else df[column].astype(dtype_mapping[dtype])
                else:
                    raise ValueError(f"Unknown dtype: {dtype}")
            else:
                raise KeyError(f"Column {column} not found in DataFrame")
        except KeyError as e:
            print(e)
            continue

    return df


# Function to convert all categorical columns to strings without modifying
# the original DataFrame. This is for compatibility with R's data types
# and creation of the R database equivalent for the Python dataframe.
# In contrast to R's factor function, categorical data is not converting
# input values to strings; categories will end up the same data type as
# the original values. In contrast to R's factor function, there is
# currently no way to assign/change labels at creation time.
def convert_categoricals_to_strings(df):
    df_r = df.copy()  # Create a copy of the original DataFrame
    for col in df_r.select_dtypes(include=['category']).columns:
        df_r[col] = df_r[col].astype(str)  # Convert categorical columns to strings
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