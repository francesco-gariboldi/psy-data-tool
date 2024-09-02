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
