import rpy2

# Print the non-mixed model performances
def best_non_mixed_model_performances(best_models, df_r, response_var, predictor_vars):
    if best_models.get('non_mixed_best_model'):
        non_mixed_best_formula = best_models['non_mixed_best_model'][0]['formula']
        r_non_mixed_best_formula = rpy2.robjects.StrVector([non_mixed_best_formula])
        rpy2.robjects.globalenv['non_mixed_best_formula'] = r_non_mixed_best_formula[0] 
        print("\n\n------------------------------------------------------------------")
        print(f"\nNon-mixed best model formula: {non_mixed_best_formula}\n")

        # Fit the non-mixed model
        non_mixed_best_model = rpy2.robjects.r(f"lm({non_mixed_best_formula}, data=df_r)")   

        # Print the summary of the non-mixed model
        summary = rpy2.robjects.r(f"summary(non_mixed_best_model)")
        print(f"# Summary {summary}\n")

        # Compute the performances of the mixed model
        performances = rpy2.robjects.r(f"performance::performance(non_mixed_best_model)")

        # Print the confidence intervals for the non-mixed model
        #conf_intervals = rpy2.robjects.r(f"confint(non_mixed_best_model)")
        #print(f"Confidence intervals: {conf_intervals}\n")

        # Print the performances
        print(performances)
    else:
        print("\n\nNon-mixed best model is missing or invalid.\n\n")




# Print the mixed model performances
def best_mixed_model_performances(best_models, df_r, response_var, predictor_vars, cat_predictor_var):
    # Check if mixed best model is available
    if best_models.get('mixed_best_model'):
        mixed_best_formula = best_models['mixed_best_model'][0]['formula']
        r_mixed_best_formula = rpy2.robjects.StrVector([mixed_best_formula])
        rpy2.robjects.globalenv['mixed_best_formula'] = r_mixed_best_formula[0]
        
        # Print the mixed model formula
        print("\n\n------------------------------------------------------------------")
        print(f"\nMixed best model formula: {mixed_best_formula}\n")

        # Fit the mixed model
        mixed_best_model = rpy2.robjects.r(f"lmer({mixed_best_formula}, data=df_r)")

        # Print the summary of the non-mixed model
        summary = rpy2.robjects.r(f"summary(mixed_best_model)")
        print(f"# Summary \n{summary}\n")

        # Compute the performances of the mixed model
        performances = rpy2.robjects.r(f"performance::performance(mixed_best_model)")
        
        #Print the confidence intervals for the mixed model
        #conf_intervals = rpy2.robjects.r(f"confint(mixed_best_model)")
        #print(f"Confidence intervals: {conf_intervals}\n")

        # Print the performances
        print(performances)
    
        # Print fixed effects
        fixed_effects = rpy2.robjects.r(f"fixef(mixed_best_model)")
        print(f"Fixed effects: {fixed_effects}\n")

        # Print random effects
        random_effects = rpy2.robjects.r(f"ranef(mixed_best_model)")
        print(f"Random effects: {random_effects}\n")
    else:
        print("\n\nMixed best model is missing or invalid.\n\n")
