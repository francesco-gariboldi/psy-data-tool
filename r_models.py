import os
import rpy2
import r_warnings
import IPython
import matplotlib.pyplot as plt

# Print the non-mixed model performances
def best_non_mixed_model_performances(best_models, df_r, response_var, predictor_vars):
    # Plot for non-mixed model if available
    if best_models.get('non_mixed_best_model'):
        non_mixed_formula = best_models['non_mixed_best_model']['formula']
        r_non_mixed_formula = rpy2.robjects.StrVector([non_mixed_formula])
        rpy2.robjects.globalenv['non_mixed_formula'] = r_non_mixed_formula[0] 
        print(f"\nNon-mixed model formula: {non_mixed_formula}")

        # Fit the non-mixed model
        non_mixed_model = rpy2.robjects.r(f"lm({non_mixed_formula}, data=df_r)")

        # Print the non-mixed model variables
        print(f"\nResponse variable: {response_var}")
        print(f"Predictor variables: {predictor_vars}\n")    

        # Print the summary of the non-mixed model
        summary = rpy2.robjects.r(f"summary(non_mixed_model)")
        print(f"# Summary {summary}\n")

        # Compute the performances of the mixed model
        performances = rpy2.robjects.r(f"performance::performance(non_mixed_model)")

        # Print the performances
        print(performances)
    else:
        print("Non-mixed best model is missing or invalid.")




# Print the mixed model performances
def mixed_best_model_performances(best_models, df_r, response_var, predictor_vars, cat_predictor_var):
    # Check if mixed best model is available
    if best_models.get('mixed_best_model'):
        mixed_formula = best_models['mixed_best_model']['formula']
        r_mixed_formula = rpy2.robjects.StrVector([mixed_formula])
        rpy2.robjects.globalenv['mixed_formula'] = r_mixed_formula[0]
        
        # Print the mixed model formula
        print("\n------------------------------------------------------------------")
        print(f"\nMixed model formula: {mixed_formula}")

        # Fit the mixed model
        mixed_model = rpy2.robjects.r(f"lmer({mixed_formula}, data=df_r)")

        # Print the mixed model variables
        print(f"\nResponse variable: {response_var}")
        print(f"Predictor variables: {predictor_vars}\n")

        # Print the summary of the non-mixed model
        summary = rpy2.robjects.r(f"summary(mixed_model)")
        print(f"# Summary \n{summary}\n")

        # Compute the performances of the mixed model
        performances = rpy2.robjects.r(f"performance::performance(mixed_model)")

        # Print the performances
        print(performances)
    
        # Print fixed effects
        fixed_effects = rpy2.robjects.r(f"fixef(mixed_model)")
        print(f"Fixed effects: {fixed_effects}\n")

        # Print random effects
        random_effects = rpy2.robjects.r(f"ranef(mixed_model)")
        print(f"Random effects: {random_effects}\n")
    else:
        print("Mixed best model is missing or invalid.")
