# The main function of the psy-data-tool project

# Importing Python packages
import os
import rpy2
import pandas as pd
from IPython.display import display, Image

# Set env variable R_HOME through python. Change the path according to your
# platform/OS and your filesystem.
os.environ['R_HOME'] = '/usr/lib/R'

# Loading R packages
graphics = rpy2.robjects.packages.importr('graphics') # Equivalent to "library(graphics)"
lme4 = rpy2.robjects.packages.importr('lme4')
lmerTest = rpy2.robjects.packages.importr('lmerTest')
performance = rpy2.robjects.packages.importr('performance')
graphics = rpy2.robjects.packages.importr('graphics')
ggplot2 = rpy2.robjects.packages.importr('ggplot2')
gglm = rpy2.robjects.packages.importr('gglm')
gridExtra = rpy2.robjects.packages.importr('gridExtra')

# Importing my modules
from data_cleaner import clean_dataframe
import ydata_profiling_generator
from vars_conversion import load_yprofiling_report, build_dtypes_dict, convert_datatypes, represent_dtype_changelog, adapt_r
from print_models_amount import models_amount_msg
import models_generator
import models_features
import models_comparison
import r_warnings
import r_graphics
import r_models
import gen_obsidian_vault


# Generate a JSON report and take data from it for an
# intelligent categorization of the database variablels.
def xplore_data(df, response_var, predictor_vars, print_r_warnings=True, vault_path=""):
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
    df = convert_datatypes(df, report_dtypes)
    represent_dtype_changelog(df, original_dtypes)

    # Activate pandas to R conversion
    rpy2.robjects.pandas2ri.activate()

    # Adapt the DataFrame to be converted to R's dataframe
    df_r = adapt_r(df)

    # Transfer the DataFrame to R's global environment
    rpy2.robjects.globalenv['df_r'] = rpy2.robjects.pandas2ri.py2rpy(df_r)

    # Generate model formulas based on the response and predictor variables
    model_formulas = models_generator.generate_all_models(df, response_var, predictor_vars)

    # Output generated models amount
    models_amount_msg(model_formulas)
    
    # Output generated models formulas
    for model in model_formulas:
        print(f"{model}\n")

    # Print the R dataframe structure after conversion
    rpy2.robjects.r("str(df_r)")
    
    # Compute evaluation indexes
    models_indexes = models_features.compute_models_indexes(df, model_formulas)

    # Perform weighted evaluation and return the best models formulae and
    # the relative composite scores
    best_models = models_comparison.weighted_evaluation(models_indexes['non_mixed'], models_indexes['mixed'])

    # Print R warnings if print_warnings is True
    if print_r_warnings:
        r_warnings.print_r_warnings()

    # Plot for the best models diagnostics
    r_graphics.plot_best_models_diagnostics_ggplot2(best_models, df_r)
    
    # Print R warnings again if print_warnings is True
    if print_r_warnings:
        r_warnings.print_r_warnings()

    # Best non-mixed model performances
    r_models.best_non_mixed_model_performances(best_models, df_r, response_var, predictor_vars)

    # Best mixed model performances
    r_models.best_mixed_model_performances(best_models, df_r, response_var, predictor_vars, cat_predictor_var = None)

    # Scatterplots of the effects of the best models
    r_graphics.dynamic_scatterplot(df_r, response_var, predictor_vars)

    # Return response variable and predictor variables
    return response_var, predictor_vars, best_models, df_r

    # Define the path for the Obsidian vault creation
    if vault_path=="":
        return None
    else:
        gen_obsidian_vault.write_models_to_obsidian(vault_path=vault_path)
        gen_obsidian_vault.populate_vault(models_json_path, vault_path)
