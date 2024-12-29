import json
import os
from scipy.stats import spearmanr

# Function to load JSON data
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON or is empty.")
        return None
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

# Function to calculate similarity coefficient using Spearman rank correlation
def calculate_similarity_coefficient(truthful_data, comparison_data):
    # Find common districts
    common_districts = set(truthful_data.keys()) & set(comparison_data.keys())
    
    if not common_districts:
        print("No common districts found between the datasets.")
        return None
    
    # Rank districts based on their values
    truthful_ranks = [truthful_data[district] for district in common_districts]
    comparison_ranks = [comparison_data[district] for district in common_districts]
    
    # Calculate Spearman rank correlation coefficient
    coefficient, _ = spearmanr(truthful_ranks, comparison_ranks)
    return coefficient

# Function to save similarity coefficients to a JSON file
def save_coefficients_to_json(coefficients, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(coefficients, file, ensure_ascii=False, indent=4)
        print(f"Similarity coefficients saved to {file_name}")
    except Exception as e:
        print(f"Error saving to file {file_name}: {e}")

# Main function
def main():
    # Path to the truthful data file
    truthful_file = "AA1_stat_gov_avg_darba_samaksa.json"
    
    # List of comparison files
    comparison_files = [
        "AA1average_prices_per_m2_privatmajas.json",
        "AA1average_prices_per_m2.json",
        "AA1AVG_NVA_vakances.json",
        "AA1AVG_ss_and_nva.json",
        "AA1AVG_ss_darbavakances.json"
    ]
    
    # Load truthful data
    truthful_data = load_json(truthful_file)
    if truthful_data is None:
        print("Truthful data file could not be loaded. Exiting.")
        return
    
    # Dictionary to hold similarity coefficients
    similarity_coefficients = {}
    
    # Iterate through comparison files and calculate coefficients
    for file_name in comparison_files:
        print(f"\nProcessing file: {file_name}")
        comparison_data = load_json(file_name)
        if comparison_data is None:
            print(f"Skipping file {file_name} due to loading issues.")
            continue
        
        coefficient = calculate_similarity_coefficient(truthful_data, comparison_data)
        if coefficient is not None:
            # Round the coefficient to 3 decimal places
            rounded_coefficient = round(coefficient, 3)
            similarity_coefficients[file_name] = rounded_coefficient
            print(f"Similarity coefficient for {file_name}: {rounded_coefficient:.3f}")
        else:
            print(f"Could not calculate similarity coefficient for {file_name}.")
    
    # Save the similarity coefficients to a JSON file
    save_coefficients_to_json(similarity_coefficients, "AA1Spīrmena_rangu_korelācijas_koeficients.json")

# Run the script
if __name__ == "__main__":
    main()
