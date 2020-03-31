import json
from datetime import date

JSON_FILE = "properties.json"
OUTPUT_FILE = "price_history.jl"

# price_data = {'county': [total_price, total_sqms, num_listings], ...}
price_data = {
    'Agder': [0, 0, 0],
    'Innlandet': [0, 0, 0],
    'Moere og Romsdal': [0, 0, 0],
    'Nordland': [0, 0, 0],
    'Oslo': [0, 0, 0],
    'Rogaland': [0, 0, 0],
    'Svalbard': [0, 0, 0],
    'Troms og Finnmark': [0, 0, 0],
    'Troendelag': [0, 0, 0],
    'Vestfold og Telemark': [0, 0, 0],
    'Vestland': [0, 0, 0],
    'Viken': [0, 0, 0],
    'Ny i dag': [0, 0, 0],
}

# Load file including JSON-object with all properties and calculate totals
with open(JSON_FILE) as f:
    properties = json.load(f)
    for property in properties:
        price_data[property['location']][0] += property['price']
        price_data[property['location']][1] += property['size']
        price_data[property['location']][2] += 1

# Calculate price per square meter and add to dictionary, and calculate average price per sqm
# price_data = {'county': [total_price, total_sqms, num_listings, sqm_price], ...}
total = [0, 0]
for location, data in price_data.items():
    price_per_sqm = int(data[0] / data[1])
    price_data[location].append(price_per_sqm)
    total[0] += data[0]
    total[1] += data[1]
avg_price = int(total[0] / total[1])

# Sort price data based on average price per square meter highest to lowest
price_data = {k: v for k, v in sorted(price_data.items(), key=lambda item: item[1][3], reverse=True)}
# Add average price for later use
price_data["Gjennomsnittspris"] = avg_price


# Print counties and belonging square meter prices
sep_line = 60*"-"
print(f'{"Fylke": <30} Kvadratmeterpris')
print(sep_line)

for location, data in price_data.items():
    if location == "Gjennomsnittspris":
        continue
    print(f'{location:<30} kr {"{:,}".format(data[3]).replace(",", " ")}')


print(sep_line)
print(f'{"Gjennomsnittspris":<30} kr {"{:,}".format(avg_price).replace(",", " ")}')


# [
# {"19-03-2020": {"county": "Oslo"}}
def save_data(price_data, output_file):
    today = date.today()
    today_data = {str(today): price_data}

    with open(output_file, "a+") as price_file:
        data = json.dumps(today_data)
        price_file.write(data + "\n")


save_data(price_data, OUTPUT_FILE)






