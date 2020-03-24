import json

JSON_FILE = "properties.json"

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
}


with open(JSON_FILE) as f:
    properties = json.load(f)
    for property in properties:
        price_data[property['location']][0] += property['price']
        price_data[property['location']][1] += property['size']
        price_data[property['location']][2] += 1


for location, data in price_data.items():
    price_per_sqm = int(data[0] / data[1])
    price_data[location].append(price_per_sqm)

price_data = {k: v for k, v in sorted(price_data.items(), key=lambda item: item[1][3], reverse=True)}

sep_line = 60*"-"

print(f'{"Fylke": <30} Kvadratmeterpris')
print(sep_line)

for location, data in price_data.items():
    print(f'{location:<30} kr {"{:,}".format(data[3]).replace(",", " ")}')






