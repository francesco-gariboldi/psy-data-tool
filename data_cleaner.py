# This module covers handling missing values, removing duplicates,
# converting data types, and renaming columns.
import numpy as np
import pandas as pd


def clean_dataframe(df):
    """
    Clean a pandas DataFrame with generalizable steps.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    
    # Save the original dataframe shape before cleaning
    original_shape = df.shape

    # 1. Drop duplicate rows
    df = df.drop_duplicates()

    # 2. Handle missing values
    # Drop columns with more than 50% missing values
    df = df.dropna(thresh=len(df) * 0.5, axis=1)
    
    # Fill missing values for numeric columns with median
    for col in df.select_dtypes(include=['number']).columns:
        df.fillna(df[col].mean(), inplace=True)
        # df[col].fillna(df[col].median(), inplace=True)
    
    # Fill missing values for categorical columns with mode
    for col in df.select_dtypes(include=['object']).columns:
        df.fillna(df[col].mode(), inplace=True)
        # df.fillna({col: col.mode()[0]}, inplace=True)
    
    # 3. Convert data types
    # Convert columns that should be numeric
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                pass
    
    # Convert date columns to datetime
    for col in df.columns:
        if 'date' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass
    
    # 4. Remove rows with any remaining missing values
    df = df.dropna()
    
    # 5. Standardize column names (to lower cased snake_case)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    # df.columns = df.columns.str.strip().str.lower().str.replace('[ ()]', '', regex=True)   this is a better way to do it with regex (more concise)
    
    cleaned_df = df

    # Print the shape's difference from the original df
    shape_message = "\n-----------------------\n"
    shape_message += f"Original df shape: {original_shape}\n"
    shape_message += f"Cleaned df shape: {cleaned_df.shape}\n"
    shape_message += "-----------------------\n"
    print(shape_message)

    return cleaned_df