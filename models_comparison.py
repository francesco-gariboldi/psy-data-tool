import numpy as np

def normalize_metric(values, reverse=False):
    """
    Normalize a list of metric values between 0 and 1.
    
    Parameters:
    values (list): A list of metric values to normalize.
    reverse (bool): If True, reverse the normalization for metrics that should be minimized.
    
    Returns:
    list: A list of normalized metric values.
    """

    # Attempt to normalize metric values
    try:
        # Check for empty values list (no models to compare)
        if len(values) != 0:
            
            # Convert values to a NumPy array
            values = np.array(values)
            
            # Find the minimum and maximum values
            min_val = values.min()
            max_val = values.max()
            
            # Check for identical values (no variation)
            if min_val == max_val and len(values) > 1:
                raise ValueError("All values are identical; cannot normalize")
            
            # Normalize values
            if reverse:
                # Reverse normalization for metrics that should be minimized
                normalized = (max_val - values) / (max_val - min_val)
            else:
                normalized = (values - min_val) / (max_val - min_val)
            
            return normalized
        else:
            raise ValueError(f"No values to normalize")
    except (ValueError):
        print("Error: Unable to normalize metric values")
        return None


def weighted_evaluation(non_mixed_results, mixed_results, weights=None):
    """
    Perform a weighted evaluation of models based on multiple metrics.
    
    Parameters:
    non_mixed_results (list): A list of dictionaries containing metrics for non-mixed models (aic, bic, r_squared, adj_r_squared).
    mixed_results (list): A list of dictionaries containing metrics for mixed models (aic, bic, marginal_r_squared, conditional_r_squared).
    weights (dict): A dictionary specifying the weights for each metric.
    
    Returns:
    dict: The best models based on the weighted evaluation for non-mixed and mixed models.
    """
    if weights is None:
        # Default weights for each metric (can be adjusted)
        weights = {
            'aic': 0.25,
            'bic': 0.25,
            'r_squared': 0.25,
            'adj_r_squared': 0.25,
            'marginal_r_squared': 0.25,
            'conditional_r_squared': 0.25
        }
    
    def evaluate(results, metric_keys):
        """
        Evaluate the results of a model comparison based on specified metrics.
        
        Parameters:
        - results (list of dict): The results of the model comparison.
        - metric_keys (list of str): The keys of the metrics to be evaluated.
        
        Returns:
        - best_model: A dictionary of the best model (non-mixed or mixed) based on the highest composite score.
        """
        problematic_models = []
        composite_scores = []

        for i, result in enumerate(results):
            try:
                # Extract metric values for the current result
                metrics = {key: result[key] for key in metric_keys if key in result}
                
                # Normalize metrics
                normalized_metrics = {key: normalize_metric([metrics[key]], reverse=(key in ['aic', 'bic']))[0] for key in metrics}
                
                # Calculate composite score
                composite_score = sum(weights[key] * normalized_metrics[key] for key in normalized_metrics)
                composite_scores.append(composite_score)
                
            except ValueError as e:
                # Append the error and problematic formula to the list
                formula = result.get('formula', f'Unknown Model {i}')
                problematic_models.append(f"Error: {e} for model formula '{formula}'")
        
        # Print all problematic models if any errors occurred
        if problematic_models:
            for error in problematic_models:
                print(error)
        
        # If no valid composite scores, print an error and return None
        if not composite_scores:
            print("Error: No models to evaluate")
            return None
        
        # Find the best model (highest composite score)
        best_model_index = np.argmax(composite_scores)
        best_model = results[best_model_index]
        
        return best_model
    
    # Evaluate non-mixed models
    non_mixed_best_model = evaluate(results=non_mixed_results, metric_keys=['aic', 'bic', 'r_squared', 'adj_r_squared'])
    
    # Evaluate mixed models
    mixed_best_model = evaluate(results=mixed_results, metric_keys=['aic', 'bic', 'marginal_r_squared', 'conditional_r_squared'])
    
    # Print best models
    print("\nBest Non-Mixed Model:", non_mixed_best_model)
    print("\nBest Mixed Model:", mixed_best_model)

    return {
        'non_mixed_best_model': non_mixed_best_model,
        'mixed_best_model': mixed_best_model
    }
