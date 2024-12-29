import json

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
        address = listing.get('address', '')  # Ensure we use the correct key 'address'
        
        for district, streets in district_streets.items():
            for street in streets:
                if address.startswith(street):
                    district_results[district].append(listing)
                    break
    
    return district_results

# Function to load and classify addresses from the JSON file
def load_and_classify():
    # Full path to the JSON file (update this to your actual file path)
    centrs_json_path = 'centrs_vakances.json'
    
    # Load the JSON file
    try:
        with open(centrs_json_path, 'r', encoding='utf-8') as file:
            listings = json.load(file)
        print(f"Listings Length: {len(listings)}")  # Debug print
    except FileNotFoundError:
        print(f"Error: {centrs_json_path} not found.")
        return

    # Classify the listings into districts
    classified_listings = classify_addresses(listings, district_streets)
    
    # Save the classified listings into separate district files
    for district, listings in classified_listings.items():
        output_path = f'{district}_vakances.json'
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(listings, file, ensure_ascii=False, indent=4)

# Run the function to load, classify, and save the listings
load_and_classify()
