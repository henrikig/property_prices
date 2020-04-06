import json
from datetime import date, timedelta
from properties.constants import PRICE_DATA

JSON_FILE = "properties.json"
HISTORY_DATA = "price_history.jl"


# Load JSON-file with properties and return calculated totals
def load_json(filename, location_list):
    with open(filename) as f:
        properties = json.load(f)
        for property in properties:
            location_list[property['location']][0] += property['price']
            location_list[property['location']][1] += property['size']
            location_list[property['location']][2] += 1
    return location_list


# Calculate price per square meter for each location as well as for all properties
# OUTPUT: location_list = {'county': [total_price, total_sqms, num_listings, sqm_price], ...}
def calculate_prices(location_list):
    total = [0, 0]
    for location, data in location_list.items():
        price_per_sqm = int(data[0] / data[1])
        location_list[location].append(price_per_sqm)
        total[0] += data[0]
        total[1] += data[1]
    avg_price = int(total[0] / total[1])

    # Sort price data based on average price per square meter highest to lowest
    location_list = {k: v for k, v in sorted(price_data.items(), key=lambda item: item[1][3], reverse=True)}
    # Add average price
    location_list["Gjennomsnittspris"] = avg_price

    return location_list


# Print counties and belonging square meter prices
def print_locations(location_list):
    sep_line = 60*"-"
    print(f'{"Fylke": <30} Kvadratmeterpris')
    print(sep_line)

    for location, data in location_list.items():
        if location == "Gjennomsnittspris":
            continue
        print(f'{location:<30} kr {"{:,}".format(data[3]).replace(",", " ")}')

    print(sep_line)
    print(f'{"Gjennomsnittspris":<30} kr {"{:,}".format(location_list["Gjennomsnittspris"]).replace(",", " ")}')


# {"2020-03-24": {"Oslo": [total_price, total_sqms, num_listings, sqm_price]...}}
def save_data(price_data, output_file):
    today = date.today()
    today_data = {str(today): price_data}

    with open(output_file, "a+") as price_file:
        data = json.dumps(today_data)
        price_file.write(data + "\n")


if __name__ == "__main__":
    price_data = load_json(JSON_FILE, PRICE_DATA)
    price_data = calculate_prices(price_data)
    print_locations(price_data)

    save_data(price_data, HISTORY_DATA)






