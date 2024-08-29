import os
os.environ['R_HOME'] = '/usr/lib/R'  # Set env variable R_HOME through python
import rpy2
from tqdm import tqdm
import warnings
import statsmodels.formula.api as smf
import gc

def compute_models_indexes(df, model_formulas, batch_size=10, output_file = os.path.join(os.getcwd(), "models.txt")):
    """
    Evaluate a list of model formulas using linear regression and determine the best model.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data.
    model_formulas (list): A list of model formula strings to be evaluated.
    batch_size (int): The number of models to process in each batch.
    output_file (str): The file to write the results to.
    
    Returns:
    dict: A dictionary with keys 'non_mixed' and 'mixed' containing lists of model performance metrics.
    """
    non_mixed_results = []
    mixed_results = []

    # Overwrite the file if it exists
    open(output_file, "w", encoding="utf-8").close()

    # Process all formulas in batches of 10 (batch_size) models each. 
    for i in tqdm(range(0, len(model_formulas), batch_size), desc="Evaluating models"):
        # Build a batch of 10 formulas
        batch_formulas = model_formulas[i:i+batch_size]

        # Extract metrics for each formula in batch
        for formula in batch_formulas:
            result = None
            try:
                # Ignore warnings during model fitting
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")

                    # Check if a model is a mixed effects model (based on the presence of random effects)
                    if '|' in formula:
                        try:
                            # Fit the mixed effect model using R's lmer function
                            lmer_fit = rpy2.robjects.r['lmer'](formula, data=rpy2.robjects.globalenv['df_r'])
    
                            # Extract relevant metrics from the lmer model
                            aic = rpy2.robjects.r['AIC'](lmer_fit)[0]
                            bic = rpy2.robjects.r['BIC'](lmer_fit)[0]
    
                            # Packages/functions: See performance::r2(), MuMIn::r.squaredGLMM()
                            # The r2glmm package computes partial R2 values for fixed effects (only for
                            # lmer, lme, and glmmPQL models).
                            r2_values = rpy2.robjects.r['r2'](lmer_fit)
                            marginal_r_squared = r2_values[0]
                            conditional_r_squared = r2_values[1]
    
                            result = {
                                'formula': formula,
                                'aic': aic,
                                'bic': bic,
                                'marginal_r_squared': marginal_r_squared[0],
                                'conditional_r_squared': conditional_r_squared[0],
                                'model': lmer_fit
                            }
                            mixed_results.append(result)
                            
                        except rpy2.rinterface_lib.embedded.RRuntimeError as e:
                            print(f"Skipping model '{formula}' due to an error during dummy fitting: {e}")
                    else:                    
                        # Fit the model using Python's statsmodels
                        model = smf.ols(formula=formula, data=df).fit()
                        
                        # More detailed logging and an additional check for problematic models
                        num_params = len(model.params)
                        num_observations = model.nobs
                        if model.df_resid <= 0 or num_observations <= num_params:
                            raise ValueError(
                                f"Residual degrees of freedom is zero or negative, or number of observations "
                                f"({num_observations}) is not greater than the number of parameters ({num_params})."
                            )

                        result = {
                            'formula': formula,
                            'aic': model.aic,
                            'bic': model.bic,
                            'r_squared': model.rsquared,
                            'adj_r_squared': model.rsquared_adj,
                            'model': model
                        }
                        non_mixed_results.append(result)
            except (ZeroDivisionError, FloatingPointError, ValueError) as e:
                print(f"Warning: Issue encountered with model '{formula}': {e}")

            except MemoryError as e:
                print(f"MemoryError: Issue encountered with model '{formula}': {e}")
            
            # Force garbage collection to free up memory
            gc.collect()
        
        # Write intermediate results to file
        with open(output_file, "a", encoding="utf-8") as file:
            for result in non_mixed_results:
                file.write(f"Model Formula: {result['formula']}\n")
                file.write(f"AIC: {result['aic']}\n")
                file.write(f"BIC: {result['bic']}\n")
                file.write(f"R-squared: {result['r_squared']}\n")
                file.write(f"Adjusted R-squared: {result['adj_r_squared']}\n")
                file.write("\n")
            for result in mixed_results:
                file.write(f"Model Formula: {result['formula']}\n")
                file.write(f"AIC: {result['aic']}\n")
                file.write(f"BIC: {result['bic']}\n")
                file.write(f"Marginal R-squared: {result['marginal_r_squared']}\n")
                file.write(f"Conditional R-squared: {result['conditional_r_squared']}\n")
                file.write("\n")

        # Clear results to avoid excessive memory usage
        non_mixed_results.clear()
        mixed_results.clear()
    
    # Read the results back and sort by AIC (or any other preferred metric)
    final_non_mixed_results = []
    final_mixed_results = []
    with open(output_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        result = {}
        for line in lines:
            if line.startswith("Model Formula:"):
                if result:
                    if 'r_squared' in result:
                        final_non_mixed_results.append(result)
                    else:
                        final_mixed_results.append(result)
                    result = {}
                result['formula'] = line.split(": ")[1].strip()
            elif line.startswith("AIC:"):
                result['aic'] = float(line.split(": ")[1].strip())
            elif line.startswith("BIC:"):
                result['bic'] = float(line.split(": ")[1].strip())
            elif line.startswith("R-squared:"):
                result['r_squared'] = float(line.split(": ")[1].strip())
            elif line.startswith("Adjusted R-squared:"):
                result['adj_r_squared'] = float(line.split(": ")[1].strip())
            elif line.startswith("Marginal R-squared:"):
                try:
                    result['marginal_r_squared'] = float(line.split(": ")[1].strip())
                except ValueError:
                    continue  # Skip lines with non-numeric values
            elif line.startswith("Conditional R-squared:"):
                try:
                    result['conditional_r_squared'] = float(line.split(": ")[1].strip())
                except ValueError:
                    continue  # Skip lines with non-numeric values
        if result:
            if 'r_squared' in result:
                final_non_mixed_results.append(result)
            else:
                final_mixed_results.append(result)
    
    final_non_mixed_results = sorted(final_non_mixed_results, key=lambda x: x['aic'])
    final_mixed_results = sorted(final_mixed_results, key=lambda x: x['aic'])

    return {
        'non_mixed': final_non_mixed_results,
        'mixed': final_mixed_results
}