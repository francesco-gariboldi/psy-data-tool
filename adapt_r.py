# Create Python df copy dataframe to be converted to R's dataframe
# Before creation of the df_r copy of the Pandas df DataFrame, an
# attempt to convert object Categorical variables to string is made.
# Convert Pandas "Category" series to strings.
def adapt_r(df):
    try:
        for column in df.select_dtypes(include='category'):
            df[column] = df[column].astype(str)
    except Exception as e:
        print(e)
        pass    
    
    # Copy the Pandas DataFrame to be converted to R's dataframe
    df_r = df

    # Return the Pandas ready for conversion dataframe
    return df_r
