import json

# Specify the filename
input_filename = 'nva_wage_data_riga_filtered.json'  # Replace with the correct path to your file

# Open the file with UTF-8 encoding to handle Latvian characters
with open(input_filename, 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# Now you can process the data as needed, for example, calculating the averages as per your original task

# For example, you can proceed with the logic for calculating the averages
districts = [
    "Avoti", "Āgenskalns", "Berģi/Bukulti","Bišumuiža/Katlakalns", "Bolderāja", "Brasa","Centrs","Čiekurkalns","Daugavgrīva","Dārzciems", "Dārziņi","Dzirciems jeb dzegužkalns","Grīziņkalns","Iļģuciems","Imanta", "Jugla","Ķengarags","Ķīpsala","Latgale (Maskavas forštate)","Mežaparks","Mežciems","Andrejsala","Pļavnieki","Purvciems", "Rumbula", "Sarkandaugava","Skanste","Šampēteris/Pleskonade","Šķirotava","Teika","Torņakalns","Vecmīlgrāvis/Mīlgrāvis","Vecrīga","Ziepniekkalns/Atgāzne","Zolitūde"
]

# Assuming the data format has the structure where each district has an associated list of values
averages = {}
for district in districts:
    if district in data:
        values = data[district]
        avg_value = sum(values) / len(values)  # Calculate average
        averages[district] = round(avg_value, 2)  # Round the average to 2 decimal places

# Write the output to a new JSON file with averages
output_filename = 'AVG_NVA_vakances.json'
with open(output_filename, 'w', encoding='utf-8') as outfile:
    json.dump(averages, outfile, ensure_ascii=False, indent=4)

print("Averages have been calculated and saved to AVG_NVA_vakances.json")
