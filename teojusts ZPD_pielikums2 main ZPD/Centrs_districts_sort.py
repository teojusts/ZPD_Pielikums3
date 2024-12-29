import json
import os

# Define district streets for classification
district_streets = {
    "Avoti": ['Avotu ', 'Augusta Deglava ', 'Matīsa ', 'Satekles ', 'Valmieras ', "Artilērijas ", "Bruņinieku ", "Lāčplēša", "Visvalža", 
              "Ernesta Birznieka-Upīša ", "Stabu ", "Vagonu ","Ģertrūdes ", "Kurbada", "Ādmiņu", "Mūrnieku", 
              "Zaķu", "Pļavas", "Lienes", "Krāsotāju", "Sparģeļu", "Vagonu", "Strenču", "Narvas", "Suntažu", "Rūjienas"],
    'Centrs2': ['Brīvības ', 'Brīvības bulvāris', 'Krišjāņa Barona ', 'Kr. Valdemāra ', "Dzirnavu ", "Elizabetes ", "Jaņa Rozentāla laukums", 
               "Skolas ", "Satekles", "Pļavu", "Alfrēda Kalniņa", "Pērses", "Stabu", "Skolas", "Zaļā", "Antonijas", "Ganu", "Alberta", 
               'Lāčplēša ', 'Marijas ', 'Merķeļa ', 'Raiņa bulvāris', "Alberta ", "Baznīcas ", "Blaumaņa ", "Bruņinieku ", "Jeruzalemes ", 
               "Tērbatas", "Akas", "Radio", "Daines", "Martas", "Zaubes", "Annas", "Arhitektu", "Inžinieru", "Palīdzības", "Akas", "Šarlotes", 
               "Maiznīcas", "Kalpaka bulvāris", "Matīsa ", "Nikolaja Rēriha ", "Pērses ", "Stabu ", "Tērbatas ", "Zaļā ", "Ģertrūdes ", 
               "Stacijas laukums", "Pērses", "Sakaru "," Vilandes", "Valkas", "Veru", "Hanzas", "Vidus", "Veru", "Mednieku", "Ganu", 
               "Lenču", "Jura Alunāna", "Andreja Pumpura", "Tomsona", "Alojas", "Nītaures", "Aristida Briāna", "Zaubes", "Emiļa Melngaiļa"],
    'Skanste': ['Duntes ', 'Ganību dambis', 'Grostonas ', 'Skanstes ', 'Sporta ', "Vesetas", 'Vesetas ', "Hanzas ", "Mālpils", "Grostonas", 
                "Roberta Hirša", "Gustava Kluča", "Mihaila Tāla", "Martas Staņas", "Aleksandra Laimes", "Lapeņu", "Lapeņu 7", 
                "Vilhelma Ostvalda", "Jāņa Dikmaņa", "Arēnas", "Laktas"],
    'Brasa': ['Brīvības ', 'Cēsu ', 'Kr. Valdemāra ', 'Miera ', 'Senču ', 'Zirņu ', "Hospitāļu ", "Invalīdu ", "Klijānu ", "Ēveles", 
              "Jāņa Daliņa", "Vesetas", "Mēness ", "Kazarmu", "Ieroču", "Kareivju", "Lejas", "Upes", "Klusā", "Lāču iela", "Straumas", 
              "Laktas", "Kaspara", "Etnas", "Indrānu", "Silmaču"],
    'Andrejsala': ['Eksporta ', 'Ganību dambis', 'Katrīnas dambis', 'Lugažu ', 'Pētersalas ', "Andrejostas", "Kaķasēkļa", "Mazā Vējzaķsala",
                   "Pulkveža Brieža", "Mastu ", "Mihaila Tāla ", "Ausekļa", "Katrīnas", "Rūpniecības", "Alūksnes", "Vēžu", "Ūmeo", 
                   "Sermaliņu", "Lugažu", "Piena", "Mazā Piena", "Ilzenes"]
}

# Function to classify addresses into the appropriate district
def classify_addresses(listings, district_streets):
    district_results = {
        "Centrs2": [],
        "Avoti": [],
        "Skanste": [],
        "Brasa": [],
        "Andrejsala": []
    }

    # Go through each listing and classify by street name
    for listing in listings:
        address = listing.get('Address', '')  # Ensure we use the correct key 'Address'
        
        for district, streets in district_streets.items():
            for street in streets:
                if address.startswith(street):
                    district_results[district].append(listing)
                    break
    
    return district_results

# Function to load and combine both JSON files
def load_and_classify():
    # Full path to the JSON files
    active_listings_path = r'C:\Users\mache\Documents\Teo Justs VSC\dzivoklu_data\Centrs_prices.json'
    archived_listings_path = r'C:\Users\mache\Documents\Teo Justs VSC\dzivoklu_data\archive_Centrs_prices.json'

    
    # Load the two JSON files (active and archived listings)
    try:
        with open(active_listings_path, 'r', encoding='utf-8') as file:
            active_data = json.load(file)
        active_listings = active_data.get('one_time_purchase', [])  # Access the list inside 'one_time_purchase'
        print(f"Active Listings Length: {len(active_listings)}")  # Debug print
    except FileNotFoundError:
        print(f"Error: {active_listings_path} not found.")
        return
    
    try:
        with open(archived_listings_path, 'r', encoding='utf-8') as file:
            archived_data = json.load(file)
        archived_listings = archived_data.get('one_time_purchase', [])  # Access the list inside 'one_time_purchase'
        print(f"Archived Listings Length: {len(archived_listings)}")  # Debug print
    except FileNotFoundError:
        print(f"Error: {archived_listings_path} not found.")
        return

    # Combine both active and archived listings
    all_listings = active_listings + archived_listings
    
    # Classify all listings into their respective districts
    classified_listings = classify_addresses(all_listings, district_streets)
    
    # Save the classified listings into separate district files
    for district, listings in classified_listings.items():
        output_path = fr'C:\Users\mache\Documents\Teo Justs VSC\dzivoklu_data\{district}_prices.json'
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(listings, file, ensure_ascii=False, indent=4)

# Run the function to load, classify, and save the listings
load_and_classify()
