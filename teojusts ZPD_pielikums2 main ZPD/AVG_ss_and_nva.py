import json
import os

def calculate_price(price):
    """
    Adjust price according to rules.
    """
    try:
        price = float(price.strip())  # Strip any whitespace and convert to float
    except ValueError:
        return None  # Return None if price is not a valid number

    # Ignore invalid prices (e.g., 0, 00, etc.)
    if price == 0:
        return None
    elif 0 < price <= 25:
        return price * 165
    elif 26 <= price <= 180:
        return price * 20
    elif 181 <= price <= 399:
        return price * 4
    elif 400 <= price <= 699:
        return price / 0.69
    elif 700 <= price <= 5000:
        return price
    else:
        return None

def load_combined_data(district_name):
    """
    Load data for a specific district by using the district's JSON filename.
    """
    file_name = f"{district_name}_vakances.json"  # Construct filename from district name
    if not os.path.exists(file_name):
        print(f"File not found: {file_name}")
        return []
    
    combined_data = []
    print(f"Loading data from {file_name}")
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                combined_data.extend(data)  # Extend if it's a list
            else:
                print(f"Data in {file_name} is not in the expected format")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {file_name}: {e}")
    
    return combined_data

def load_nva_wage_data(file_name):
    """
    Load NVA wage data from the given JSON file.
    """
    if not os.path.exists(file_name):
        print(f"File not found: {file_name}")
        return {}
    
    print(f"Loading wage data from {file_name}")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                print(f"Data in {file_name} is not in the expected format")
                return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_name}: {e}")
        return {}

def calculate_avg_price_per_district(districts, wage_data):
    """
    Calculate average price per district based on district JSON files and NVA wage data.
    Exclude districts with less than 6 values.
    """
    district_prices = {}

    for district in districts:
        # Load the data for the specific district
        combined_data = load_combined_data(district)

        if not combined_data:
            print(f"No data found for {district}")
            continue

        # Process data and calculate prices
        prices = []
        for entry in combined_data:
            price = calculate_price(entry.get("price", ""))

            if price is not None:
                prices.append(price)

        # Add wage data from the NVA file
        if district in wage_data:
            wages = wage_data[district]
            if isinstance(wages, list):
                prices.extend(wages)  # Extend with wage data

        # Only include districts with 6 or more valid values
        if len(prices) >= 6:
            # Calculate average price for the district
            avg_price = sum(prices) / len(prices)
            district_prices[district] = round(avg_price, 2)
        else:
            print(f"Skipping {district} because it has fewer than 6 valid prices.")

    return district_prices

def save_to_json(data, file_name):
    """
    Save the processed average prices to a JSON file.
    Sort the data in descending order.
    """
    # Sort data by the average price in descending order
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)

# List of districts corresponding to the filenames (without "_vakances.json")
districts = [
    "aganskalns", "Bergi", "Bierini", "Bolderaja", "centrs2", "Ciekurkalns", 
    "Darzciems", "Daugavgriva", "Dreilini", "DzegužkalnsDzircems", "Grīziņkalns", 
    "Ilgciems", "Imanta", "Jugla", "Kengarags", "Kipsala", "KrastaSt", "Latgale", 
    "Mezaparks", "Mezciems", "pardaugava", "Plavnieki", "Purvciems", "Rumbula", 
    "Sampeteris", "Sarkandaugava", "Skirotava", "Teika", "Tornakalns", "Vecaķi", 
    "Vecmilgravis", "Vecriga", "Voleri", "Zasulauks", "Ziepniekkalns", "Zolitude", "Skanste", "Brasa", "Avoti", "Andrejsala", "darzini"
]

nva_file = 'nva_wage_data_riga_filtered.json'  # File containing wage data
output_file = 'AVG_ss_and_nva.json'  # Output file to store averages

# Load NVA wage data
wage_data = load_nva_wage_data(nva_file)

# Calculate average prices per district
district_averages = calculate_avg_price_per_district(districts, wage_data)

# Save the results to a JSON file
save_to_json(district_averages, output_file)

print(f"Average prices saved to {output_file}")
