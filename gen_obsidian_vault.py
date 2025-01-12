import os
import json


def write_models_to_obsidian(vault_path):
    """
    Create an Obsidian vault at the specified path.

    Arguments:
    - vault_path: str (path where the vault will be created)

    Returns:
    - str: Path to the created vault, or None if the vault already exists.
    """
    if not os.path.exists(vault_path):
        os.makedirs(vault_path)
        print(f"Vault created at '{vault_path}'.")
        return vault_path
    else:
        print(f"Vault already exists at '{vault_path}'.")
        print("Please, remove the existing vault or choose another path.")
        return None  # Exit the function


def populate_vault(models_json_path, vault_path):
    """
    Populate an Obsidian vault with models from models.json.

    Links model notes using composite scores to create a relational network of models.

    Arguments:
    - models_json_path: str (path to models.json containing the models data)
    - vault_path: str (path of the vault where the models will be stored)
    """
    # Ensure the models.json file exists
    if not os.path.exists(models_json_path):
        print(f"Error: models.json file not found at '{models_json_path}'.")
        return

    # Ensure the vault directory exists
    if not os.path.exists(vault_path):
        os.makedirs(vault_path)
        print(f"Vault created at '{vault_path}'.")
    else:
        print(f"Using existing vault at '{vault_path}'.")

    # Load models data from models.json
    with open(models_json_path, "r", encoding="utf-8") as json_file:
        models_data = json.load(json_file)

    # Validate models data
    if not all(key in models_data for key in ['non_mixed', 'mixed']):
        print("Error: models.json is missing required keys ('non_mixed', 'mixed').")
        return

    # Function to generate links based on composite score
    def generate_links(model, models, max_links=3):
        """
        Generate a list of links to related models based on similarity in composite scores.

        Arguments:
        - model: dict (current model's data)
        - models: list of dict (all models in the same category)
        - max_links: int (maximum number of links to generate)

        Returns:
        - list of str: Titles of related models
        """
        current_score = model.get('composite_score', float('inf'))
        similar_models = sorted(models, key=lambda x: abs(x.get('composite_score', float('inf')) - current_score))
        # Exclude the current model and limit the number of links
        related_models = [m['formula'] for m in similar_models if m != model][:max_links]
        return related_models

    # Write notes for each model category
    for category, models in models_data.items():
        category_path = os.path.join(vault_path, category)
        os.makedirs(category_path, exist_ok=True)

        for model in models:
            # Sanitize formula for filenames
            model_title = model['formula'].replace(" ", "_").replace("+", "-").replace("/", "_")
            note_path = os.path.join(category_path, f"{model_title}.md")
            links = generate_links(model, models)

            # Write model data and links to a Markdown note
            with open(note_path, "w", encoding="utf-8") as note_file:
                note_file.write(f"# {model['formula']}\n\n")
                note_file.write(f"## Metrics\n")
                for metric, value in model.items():
                    if metric not in ['formula']:  # Exclude the formula from the metrics list
                        note_file.write(f"- **{metric}**: {value}\n")

                if links:
                    note_file.write("\n## Related Models\n")
                    for link in links:
                        link_title = link.replace(" ", "_").replace("+", "-").replace("/", "_")
                        note_file.write(f"- [[{link_title}]]\n")

    print(f"Models successfully populated in Obsidian vault at '{vault_path}'.")
