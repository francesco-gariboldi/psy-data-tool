import pandas as pd
from itertools import combinations, chain

def generate_null_models(response_var):
    models = [f"{response_var} ~ 1"]
    return models

def generate_simple_and_additional_models(df, response_var, predictor_vars):
    """
    Generate all possible simple and additional model formulas (R/Patsy-style)
    from response_var and predictor_vars in a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    response_var (str): The response variable.
    predictor_vars (list): A list of predictor variable names.
    
    Returns:
    list: A list of model formulas.
    """
    
    # Ensure the response_var and predictor_vars are in the DataFrame
    if response_var not in df.columns:
        raise ValueError(f"Response variable '{response_var}' is not in the DataFrame.")
    
    for predictor in predictor_vars:
        if predictor not in df.columns:
            raise ValueError(f"Predictor variable '{predictor}' is not in the DataFrame.")
    
    # Initialize the list to hold all model formulas
    models = []
    
    # Generate simple models (one predictor at a time)
    for predictor in predictor_vars:
        models.append(f"{response_var} ~ {predictor}")
    
    # Generate additional models (combinations of predictors)
    for i in range(2, len(predictor_vars) + 1):
        for combo in combinations(predictor_vars, i):
            models.append(f"{response_var} ~ {' + '.join(combo)}")
    
    return models


def generate_interaction_models(df, response_var, predictor_vars):
    """
    Generate all possible interaction model formulas (R/Patsy-style)
    from response_var and predictor_vars in a DataFrame.
    Generate models that include both the main effects and the interaction terms.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    response_var (str): The response variable.
    predictor_vars (list): A list of predictor variable names.
    
    Returns:
    list: A list of model formulas.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")
    if not isinstance(response_var, str):
        raise ValueError("response_var must be a string")
    if not isinstance(predictor_vars, list) or not all(isinstance(var, str) for var in predictor_vars):
        raise ValueError("predictor_vars must be a list of strings")
    
    # Generate main effects formula
    main_effects = " + ".join(predictor_vars)
    
    # List to store the formulas
    formulas = []
    
    # Add formula with only main effects
    formulas.append(f"{response_var} ~ {main_effects}")
    
    # Generate interaction terms
    for i in range(2, len(predictor_vars) + 1):
        for combo in combinations(predictor_vars, i):
            interaction_terms = " + ".join([":".join(pair) for pair in combinations(combo, 2)])
            formulas.append(f"{response_var} ~ {interaction_terms}")
            if main_effects:
                formulas.append(f"{response_var} ~ {main_effects} + {interaction_terms}")
    
    # Generate individual interaction terms combined with main effects
    for combo in combinations(predictor_vars, 2):
        interaction_term = ":".join(combo)
        formulas.append(f"{response_var} ~ {interaction_term}")
        for var in combo:
            formulas.append(f"{response_var} ~ {var} + {interaction_term}")
    
    return formulas


def generate_multilevel_models(df, response_var, predictor_vars):
    multilevel_models = set()  # Use a set to track unique models
    
    # Generate all combinations of predictors for fixed effects
    for r in range(1, len(predictor_vars) + 1):
        for combo in combinations(predictor_vars, r):
            fixed_effects = ' + '.join(combo)
            
            for grouping_var in predictor_vars:
                # Random intercept models
                random_intercept_formula = f"{response_var} ~ 1 + (1 | {grouping_var})"
                multilevel_models.add(random_intercept_formula)
                
                fixed_effect_random_intercept_formula = f"{response_var} ~ {fixed_effects} + (1 | {grouping_var})"
                multilevel_models.add(fixed_effect_random_intercept_formula)
                
                # Random intercept and slope models
                random_intercept_and_slope_formula = f"{response_var} ~ 1 + ({fixed_effects} | {grouping_var})"
                multilevel_models.add(random_intercept_and_slope_formula)
                
                fixed_effect_random_intercept_and_slope_formula = f"{response_var} ~ {fixed_effects} + ({fixed_effects} | {grouping_var})"
                multilevel_models.add(fixed_effect_random_intercept_and_slope_formula)
                
                # Random slope models without intercept
                random_slope_formula = f"{response_var} ~ 1 + (0 + {fixed_effects} | {grouping_var})"
                multilevel_models.add(random_slope_formula)
                
                fixed_effect_random_slope_formula = f"{response_var} ~ {fixed_effects} + (0 + {fixed_effects} | {grouping_var})"
                multilevel_models.add(fixed_effect_random_slope_formula)
    
    return list(multilevel_models)  # Convert set back to list for the final output

def generate_all_models(df, response_var, predictor_vars):
    null_models = generate_null_models(response_var)
    simple_and_additional_models = generate_simple_and_additional_models(df, response_var, predictor_vars)
    interaction_models = generate_interaction_models(df, response_var, predictor_vars)

    # Check for 'category' dtype columns
    category_columns = df.select_dtypes(include='category')
    if not category_columns.empty:
        multilevel_models = generate_multilevel_models(df, response_var, predictor_vars)
        all_models = null_models + simple_and_additional_models + interaction_models + multilevel_models
    else:
        all_models = null_models + simple_and_additional_models + interaction_models

    # Remove duplicates
    unique_models = set()
    all_models_cleaned = []
    for string in all_models:
        if string not in unique_models:
            all_models_cleaned.append(string)
            unique_models.add(string)
    
    return all_models_cleaned