# Importing Python packages
import os
import rpy2
import pandas as pd

# Loading R packages
graphics = rpy2.robjects.packages.importr('graphics') # Equivalent to "library(graphics)"
lme4 = rpy2.robjects.packages.importr('lme4')
lmerTest = rpy2.robjects.packages.importr('lmerTest')
performance = rpy2.robjects.packages.importr('performance')
graphics = rpy2.robjects.packages.importr('graphics')

# Importing my modules
from data_cleaner import clean_dataframe
import ydata_profiling_generator
from vars_conversion import load_yprofiling_report, build_dtypes_dict, convert_dtypes, represent_dtype_changelog, convert_categoricals_to_strings
from print_models_amount import models_amount_msg
import models_generator
import models_features
import models_comparison
import r_warnings
import r_graphics


# A function to automate models generation, models performances
# and graphical representations for psychological research. It
# generates a JSON report and takes data from it for an
# intelligent categorization of the database variablels.
def explore_data(df, response_var, predictor_vars, print_r_warnings=True):
    '''A function to automate models generation, models performances
    and graphical representations for psychological research. It
    generates a JSON report and takes data from it for an
    intelligent categorization of the database variablels.
    '''
    # Set environment variable for R_HOME
    os.environ['R_HOME'] = '/usr/lib/R'

    # Generate ydata-profiling report
    ydata_profiling_generator.generate_profiling_report(df)

    # Clean the dataframe
    df = clean_dataframe(df)

    # Load ydata-profiling report and process data types
    data_profile = load_yprofiling_report()
    report_dtypes = build_dtypes_dict(data_profile)
    original_dtypes = df.dtypes

    # Convert the DataFrame dtypes
    df = convert_dtypes(df, report_dtypes)
    represent_dtype_changelog(df, original_dtypes)

    # Activate pandas to R conversion
    rpy2.robjects.pandas2ri.activate()

    # Convert categorical dtypes to strings for R compatibility
    df_r = convert_categoricals_to_strings(df)

    # Transfer the DataFrame to R
    # The pandas2ri.py2ri function support the reverse operation to convert DataFrames
    # into the equivalent R object (that is, data.frame)
    # From release 2.0.0rc1 the function py2ri() moved to the new module 'conversion'.
    # Adding the prefix conversion. to calls to those functions will be enough
    # to update existing code.
    # It works but needs modification.
    rpy2.robjects.globalenv['df_r'] = rpy2.robjects.pandas2ri.py2rpy(df_r)

    # Generate model formulas based on the response and predictor variables
    model_formulas = models_generator.generate_all_models(df, response_var, predictor_vars)
    models_amount_msg(model_formulas)

    # Compute evaluation indexes
    evaluation_results = models_features.compute_models_indexes(df, model_formulas)

    # Perform weighted evaluation
    best_models = models_comparison.weighted_evaluation(evaluation_results['non_mixed'], evaluation_results['mixed'])

    # Print R warnings if print_warnings is True
    if print_r_warnings:
        r_warnings.print_r_warnings()

    # Plot diagnostics for the best models
    r_graphics.plot_best_models_diagnostics(best_models, df_r)
    
    # Print R warnings again if print_warnings is True
    if print_r_warnings:
        r_warnings.print_r_warnings()