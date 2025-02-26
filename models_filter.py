# A “nonsense‐filtering” function that tries to catch the most common causes
# of infeasible models (in particular, random‐effects terms that blow up the
# number of parameters relative to the data size).

import re
import pandas as pd

def filter_dumb_models(df, model_list):
    """
    Removes model formulas that are unlikely to be computed successfully,
    mainly where the random-effects structure implies more parameters than data.
    
    Args:
        df (pd.DataFrame): The dataset.
        model_list (list): A list of R/Patsy-style formulas.

    Returns:
        list: A filtered list of model formulas that are more likely to be feasible.
    """
    filtered = []
    n = df.shape[0]  # total number of observations
    
    # Regex to find random-effects terms of the form (something | groupingVar)
    random_effect_pattern = r"\((.*?)\s*\|\s*(.*?)\)"
    
    for formula in model_list:
        # Find all random-effect blocks, e.g. "(1 + x | group)" => [("1 + x", "group")]
        random_effects = re.findall(random_effect_pattern, formula)
        
        skip_this_formula = False
        
        for rand_part, grouping_var in random_effects:
            # If the grouping variable is not in the DataFrame, skip immediately
            if grouping_var not in df.columns:
                skip_this_formula = True
                break
            
            # Count unique levels
            unique_levels = df[grouping_var].nunique()
            
            # If grouping var is purely numeric/float with large cardinality, usually dumb
            # (Unless you explicitly turned it into a categorical or few-level factor)
            if pd.api.types.is_numeric_dtype(df[grouping_var]) and unique_levels > 10:
                skip_this_formula = True
                break
            
            # Split the random part by '+' to count intercept vs slopes
            # e.g. "1 + x + y" => intercept=1 + 2 slopes
            #      "0 + x + y" => no intercept, 2 slopes
            # We remove spaces to avoid splitting on them
            terms = rand_part.replace(" ", "").split("+")
            
            random_intercepts = 0
            random_slopes = 0
            for t in terms:
                if t == '1':
                    random_intercepts += 1
                elif t.startswith("0"):
                    # "0" means no intercept, so we ignore that piece
                    pass
                else:
                    # anything else is presumably a slope
                    random_slopes += 1
            
            # Total random effects = (intercepts + slopes) * number_of_levels
            total_rand_effects = (random_intercepts + random_slopes) * unique_levels
            
            # If that total is >= N, it's probably unidentifiable
            if total_rand_effects >= n:
                skip_this_formula = True
                break
        
        if not skip_this_formula:
            filtered.append(formula)
    
    return filtered
