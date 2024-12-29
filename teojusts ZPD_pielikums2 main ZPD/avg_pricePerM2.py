import json
import os
import numpy as np

output_dir = 'dzivoklu_data'  # Directory where JSON files are stored
output_file = 'AA1average_prices_per_m2.json'  # Final output file to save averages

# Provided list of locations with additional attributes (URL details are ignored here)
locations = [
    {"name": "Centrs2"},
    {"name": "Āgenskalns"},
    {"name": "Aplokciems"},
    {"name": "Berģi"},
    {"name": "Bieriņi"},
    {"name": "Bolderāja"},
    {"name": "Brekši"},
    {"name": "Čiekurkalns"},
    {"name": "Dārzciems"},
    {"name": "Daugavgrīva"},
    {"name": "Dreiliņi"},
    {"name": "Dzegužkalns"},
    {"name": "Grīziņkalns"},
    {"name": "Iļģuciems"},
    {"name": "Imanta"},
    {"name": "Jugla"},
    {"name": "Ķengarags"},
    {"name": "Ķīpsala"},
    {"name": "Klīversala"},
    {"name": "Krasta_r-ns"},
    {"name": "Kundziņsala"},
    {"name": "Latgales_priekšpilsēta"},
    {"name": "Mangaļi"},
    {"name": "Mangaļsala"},
    {"name": "Mežaparks"},
    {"name": "Mežciems"},
    {"name": "Pļavnieki"},
    {"name": "Purvciems"},
    {"name": "Šampēteris-Pleskodāle"},
    {"name": "Sarkandaugava"},
    {"name": "Šķirotava"},
    {"name": "Teika"},
    {"name": "Torņakalns"},
    {"name": "Vecmīlgrāvis"},
    {"name": "Vecrīga"},
    {"name": "Zasulauks"},
    {"name": "Ziepniekkalns"},
    {"name": "Zolitūde"},
    {"name": "Andrejsala"},
    {"name": "Skanste"},
    {"name": "Avoti"},
    {"name": "Brasa"}
]

def load_combined_data(location_name):
    active_file = os.path.join(output_dir, f"{location_name}_prices.json")
    archive_file = os.path.join(output_dir, f"archive_{location_name}_prices.json")
    combined_data = []

    # Load active data
    if os.path.exists(active_file):
        with open(active_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Check if data is a list or a dictionary with 'one_time_purchase'
            if isinstance(data, list):
                combined_data.extend(data)  # Directly extend if it's a list
            elif isinstance(data, dict) and 'one_time_purchase' in data:
                combined_data.extend(data['one_time_purchase'])  # Extend from the 'one_time_purchase' key

    # Load archived data
    if os.path.exists(archive_file):
        with open(archive_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Check if data is a list or a dictionary with 'one_time_purchase'
            if isinstance(data, list):
                combined_data.extend(data)  # Directly extend if it's a list
            elif isinstance(data, dict) and 'one_time_purchase' in data:
                combined_data.extend(data['one_time_purchase'])  # Extend from the 'one_time_purchase' key

    return combined_data


# Calculate the average price per square meter for all locations
def calculate_avg_price_per_m2(locations):
    avg_prices = {}

    for location in locations:
        location_name = location["name"]
        combined_data = load_combined_data(location_name)

        # Extract valid 'Price_per_m²' entries
        prices_per_m2 = [
            entry['Price_per_m²'] for entry in combined_data
            if 'Price_per_m²' in entry and isinstance(entry['Price_per_m²'], (int, float))
        ]

        # Calculate average price per m²
        if prices_per_m2:
            avg_prices[location_name] = round(np.mean(prices_per_m2), 2)
        else:
            avg_prices[location_name] = None  # No valid data found

    # Sort the dictionary by price (descending order)
    sorted_avg_prices = {k: v for k, v in sorted(avg_prices.items(), key=lambda item: item[1] if item[1] is not None else -float('inf'), reverse=True)}

    return sorted_avg_prices

# Save results to a JSON file
def save_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Main script execution
if __name__ == "__main__":
    avg_prices = calculate_avg_price_per_m2(locations)
    save_to_json(avg_prices, output_file)
    print(f"Average prices per m² saved to {output_file}")
