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
    values = np.array(values)
    min_val = values.min()
    max_val = values.max()
    
    if reverse:
        # Reverse normalization for metrics that should be minimized
        normalized = (max_val - values) / (max_val - min_val)
    else:
        normalized = (values - min_val) / (max_val - min_val)
    
    return normalized


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
        # Extract metric values
        metrics = {key: [result[key] for result in results if key in result] for key in metric_keys}
        
        # Normalize metrics
        normalized_metrics = {key: normalize_metric(values, reverse=(key in ['aic', 'bic'])) for key, values in metrics.items()}
        
        # Calculate composite scores
        composite_scores = []
        for i in range(len(results)):
            composite_score = sum(weights[key] * normalized_metrics[key][i] for key in metric_keys if key in normalized_metrics and i < len(normalized_metrics[key]))
            composite_scores.append(composite_score)
        
        # Find the best model (highest composite score)
        best_model_index = np.argmax(composite_scores)
        best_model = results[best_model_index]
        
        return best_model
    
    # Evaluate non-mixed models
    non_mixed_best_model = evaluate(non_mixed_results, ['aic', 'bic', 'r_squared', 'adj_r_squared'])
    
    # Evaluate mixed models
    mixed_best_model = evaluate(mixed_results, ['aic', 'bic', 'marginal_r_squared', 'conditional_r_squared'])
    
    # Print best models
    print("\nBest Non-Mixed Model:", non_mixed_best_model)
    print("\nBest Mixed Model:", mixed_best_model)

    return {
        'non_mixed_best_model': non_mixed_best_model,
        'mixed_best_model': mixed_best_model
    }
