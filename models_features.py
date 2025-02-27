import os
import rpy2
from tqdm import tqdm
import warnings
import statsmodels.formula.api as smf
import gc
import json

os.environ['R_HOME'] = '/usr/lib/R'  # Set env variable R_HOME through python

def compute_models_indexes(df, model_formulas, batch_size=10, output_file=os.path.join(os.getcwd(), "models.json")):
    """
    Evaluate a list of model formulas using linear regression and determine the best model.
    Save results in a JSON file instead of a text file.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data.

    model_formulas (list): A list of model formula strings to be evaluated.
    
    batch_size (int): The number of models to process in each batch.
    
    output_file (str): The JSON file to write the results to.
    
    Returns:
    dict: A dictionary with keys 'non_mixed' and 'mixed' containing lists of model performance metrics.
    """
    non_mixed_results = []
    mixed_results = []

    # Process all formulas in batches
    for i in tqdm(range(0, len(model_formulas), batch_size), desc="Evaluating models"):
        batch_formulas = model_formulas[i:i + batch_size]

        for formula in batch_formulas:
            result = None
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")

                    if '|' in formula:
                        try:
                            lmer_fit = rpy2.robjects.r['lmer'](formula, data=rpy2.robjects.globalenv['df_r'])
                            aic = rpy2.robjects.r['AIC'](lmer_fit)[0]
                            bic = rpy2.robjects.r['BIC'](lmer_fit)[0]
                            r2_values = rpy2.robjects.r['r2'](lmer_fit)
                            marginal_r_squared = r2_values[0]
                            conditional_r_squared = r2_values[1]
    
                            result = {
                                'formula': formula,
                                'aic': aic,
                                'bic': bic,
                                'marginal_r_squared': marginal_r_squared[0],
                                'conditional_r_squared': conditional_r_squared[0],
                            }
                            mixed_results.append(result)
                            
                        except rpy2.rinterface_lib.embedded.RRuntimeError as e:
                            print(f"Skipping model '{formula}' due to an error: {e}")
                    else:
                        model = smf.ols(formula=formula, data=df).fit()
                        num_params = len(model.params)
                        num_observations = model.nobs
                        if model.df_resid <= 0 or num_observations <= num_params:
                            raise ValueError(
                                f"Residual degrees of freedom is zero or negative, "
                                f"or observations ({num_observations}) are <= parameters ({num_params})."
                            )

                        result = {
                            'formula': formula,
                            'aic': model.aic,
                            'bic': model.bic,
                            'r_squared': model.rsquared,
                            'adj_r_squared': model.rsquared_adj,
                        }
                        non_mixed_results.append(result)
            except (ZeroDivisionError, FloatingPointError, ValueError) as e:
                print(f"Warning: Issue with model '{formula}': {e}")
            except MemoryError as e:
                print(f"MemoryError: Issue with model '{formula}': {e}")
            
            gc.collect()

    # Sort results by AIC
    non_mixed_results = sorted(non_mixed_results, key=lambda x: x['aic'])
    mixed_results = sorted(mixed_results, key=lambda x: x['aic'])

    models_indexes = {
        'non_mixed': non_mixed_results,
        'mixed': mixed_results,
    }

    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(models_indexes, json_file, indent=4)
            print(f"Results successfully written to {output_file}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
    
    return models_indexes
