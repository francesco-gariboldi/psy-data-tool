import numpy as np
import json
import os
import sys


def normalize_metric(values, reverse=False):
    """
    Normalize a list of metric values between 0 and 1.
    
    Parameters:
    values (list): A list of metric values to normalize.
    reverse (bool): If True, reverse the normalization for metrics that should be minimized.
    
    Returns:
    list: A list of normalized metric values.
    """
    try:
        if len(values) == 0:
            raise ValueError("No values to normalize")

        values = np.array(values)
        min_val = values.min()
        max_val = values.max()
        
        if min_val == max_val and len(values) > 1:
            raise ValueError("All values are identical; cannot normalize")

        normalized = (max_val - values) / (max_val - min_val) if reverse else (values - min_val) / (max_val - min_val)
        return normalized
    except ValueError as e:
        print(f"Normalization Error: {e}")
        return None


def weighted_evaluation(non_mixed_results, mixed_results, weights=None, models_json_path=None):
    """
    Perform a weighted evaluation of models based on multiple metrics, appending composite scores
    to each model in models.json.

    Parameters:
    - non_mixed_results (list): A list of dictionaries for non-mixed models.
    - mixed_results (list): A list of dictionaries for mixed models.
    - weights (dict): A dictionary specifying the weights for each metric.
    - models_json_path (str): Path to the models.json file to update.

    Returns:
    dict: The best models with updated composite scores.
    """
    # Define IS_COLAB based on the environment
    try:
        IS_COLAB = 'google.colab' in str(get_ipython())
    except NameError:
        IS_COLAB = False

    # Set the models.json path if running in Google Colab
    try:
        if IS_COLAB:
            # If running in Google Colab, use Colab's directory for models.json
            models_json_path = "/content/psy-data-tool/models.json"
        else:
            print("Not in colab. I'll retrieve the 'models.json' path from the local OS")
    except ImportError:
        # Otherwise, use a local path relative to the current working directory
        models_json_path = os.path.join(os.getcwd(), "models.json")
        sys.exit(1)
    
    if weights is None:
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
        Add composite scores to each model and find the best one.

        Parameters:
        - results (list of dict): Models to evaluate.
        - metric_keys (list of str): Metrics used in evaluation.

        Returns:
        dict: The best model based on the composite score.
        """
        composite_scores = []
        problematic_models = []

        # Extract metric values for normalization
        metrics_data = {key: [r.get(key, float('inf')) for r in results] for key in metric_keys}
        normalized_metrics = {key: normalize_metric(values, reverse=(key in ['aic', 'bic'])) for key, values in metrics_data.items()}

        for i, result in enumerate(results):
            try:
                # Calculate composite score and put it in the composite_scores list
                composite_score = sum(weights[key] * normalized_metrics[key][i] for key in metric_keys if key in result)
                result['composite_score'] = composite_score
                composite_scores.append(composite_score)
            except ValueError as e:
                formula = result.get('formula', f'Unknown Model {i}')
                problematic_models.append(f"Error: {e} for model formula '{formula}'")

        # Report problematic models
        if problematic_models:
            for error in problematic_models:
                print(error)

        # Find and return the best model's formula
        if composite_scores:
            best_model_index = np.argmax(composite_scores)
            return results[best_model_index], composite_scores
        else:
            print("Error: No valid models to evaluate.")
            return None

    # Evaluate non-mixed and mixed models (formulae)
    non_mixed_best_model = evaluate(non_mixed_results, ['aic', 'bic', 'r_squared', 'adj_r_squared'])
    mixed_best_model = evaluate(mixed_results, ['aic', 'bic', 'marginal_r_squared', 'conditional_r_squared'])

    # Save the updated results to models.json
    if models_json_path:
        try:
            with open(models_json_path, "r", encoding="utf-8") as json_file:
                models_data = json.load(json_file)

            models_data['non_mixed'] = non_mixed_results
            models_data['mixed'] = mixed_results

            with open(models_json_path, "w", encoding="utf-8") as json_file:
                json.dump(models_data, json_file, indent=4)

            print(f"Updated models.json with composite scores at '{models_json_path}'")
        except Exception as e:
            print(f"Error updating models.json: {e}")

    # Return the best models and composite_scores list
    return {
        'non_mixed_best_model': non_mixed_best_model,
        'mixed_best_model': mixed_best_model
    }
