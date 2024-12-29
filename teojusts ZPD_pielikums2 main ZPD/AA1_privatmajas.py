import requests
from lxml import html
import json
import os
import re

# Output directory for the scraped data
output_dir = 'real_estate_data'
os.makedirs(output_dir, exist_ok=True)

# Function to scrape data
def scrape_prices(base_url, total_pages, output_filename):
    one_time_purchase = []
    monthly = []
    daily = []

    for page_number in range(1, total_pages + 1):
        url = base_url.format(page_number)
        print(f"Scraping URL: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            listings_xpath = '//tr[@id]'  # XPath for listings
            listings_elements = tree.xpath(listings_xpath)

            for listing in listings_elements:
                try:
                    # Extract size of the house
                    size_element = listing.xpath('./td[5]/text() | ./td[5]/b/text()')
                    size_text = size_element[0].strip() if size_element else ""
                    size_value = float(re.sub(r'[^\d.]', '', size_text)) if size_text else None

                    # Extract total price
                    total_price_element = listing.xpath('./td[9]/text() | ./td[9]/b/text()')
                    total_price_text = total_price_element[0].strip() if total_price_element else ""
                    total_price_value = float(re.sub(r'[^\d.]', '', total_price_text)) if total_price_text else None

                    # Skip entries if size or total price is missing
                    if not size_value or not total_price_value:
                        continue

                    # Calculate price per square meter
                    price_per_m2_value = round(total_price_value / size_value, 2) if size_value > 0 else None

                    # Create a data dictionary
                    data_entry = {
                        "Price_per_m²": price_per_m2_value,
                        "Price": total_price_value,
                        "m²": size_value
                    }

                    # Skip monthly or daily listings
                    if "/mēn." in total_price_text:
                        monthly.append(data_entry)
                    elif "dienā" in total_price_text:
                        daily.append(data_entry)
                    else:
                        one_time_purchase.append(data_entry)

                except ValueError as e:
                    print(f"Error processing listing: {e}")

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    # Save the results to a JSON file
    data = {
        "one_time_purchase": one_time_purchase,
        "monthly": monthly,
        "daily": daily
    }

    with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {output_filename}")

locations = [
    {"name": "centre", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/centre/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/centre/page{}.html", "pages": 1},
    {"name": "agenskalns", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/agenskalns/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/agenskalns/page{}.html", "pages": 1},
    {"name": "bergi", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/bergi/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/bergi/page{}.html", "pages": 1},
    {"name": "bierini", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/bierini/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/bierini/page{}.html", "pages": 1},
    {"name": "bolderaya", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/bolderaya/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/bolderaya/page{}.html", "pages": 1},
    {"name": "bukulti", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/bukulti/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/bukulti/page{}.html", "pages": 1},
    {"name": "chiekurkalns", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/chiekurkalns/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/chiekurkalns/page{}.html", "pages": 1},
    {"name": "darzciems", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/darzciems/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/darzciems/page{}.html", "pages": 1},
    {"name": "darzini", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/darzini/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/darzini/page{}.html", "pages": 1},
    {"name": "vecaki", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/vecaki/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/vecaki/page{}.html", "pages": 1},
    {"name": "beberbeki", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/beberbeki/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/beberbeki/page{}.html", "pages": 1},
    {"name": "dreilini", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/dreilini/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/dreilini/page{}.html", "pages": 1},
    {"name": "jaunciems", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/jaunciems/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/jaunciems/page{}.html", "pages": 1},
    {"name": "trisciems", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/trisciems/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/trisciems/page{}.html", "pages": 1},
    {"name": "kleisti", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/kleisti/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/kleisti/page{}.html", "pages": 1},
    {"name": "vecdaugava", "url": "https://www.ss.lv/lv/real-estate/homes-summer-residences/riga/vecdaugava/page{}.html", "archive_url": "https://www.ss.lv/lv/archive/real-estate/homes-summer-residences/riga/vecdaugava/page{}.html", "pages": 1}
]

# Scrape data for each location
for location in locations:
    scrape_prices(location["url"], location["pages"], f"{location['name']}_prices.json")
    scrape_prices(location["archive_url"], location["pages"], f"archive_{location['name']}_prices.json")
