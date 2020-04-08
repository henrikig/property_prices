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


# Extract data from JSON lines history file
def extract_history(filename):
    data = []
    # Extract data from price history file
    with open(filename, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


# Reformat list of dates to dict of dates
def dict_from_list(data_list):
    return {list(item.keys())[0]: list(item.values())[0] for item in data_list}


# Get data from specified date
def data_from_date(data, days_ago):
    today = date.today()
    days_ago = today - timedelta(days=days_ago)
    return data.get(str(days_ago))


# Create dict containing today's, last week's and month's data
# OUTPUT: {'Oslo': [today_avg, %_one_day, %_week, %_month], ... }
def trends_analysis(trend_data):
    trends = dict()
    for location in trend_data[0]:
        if location == "Gjennomsnittspris":
            today_price = trend_data[0].get(location)
        else:
            today_price = trend_data[0].get(location)[-1]
        trends[location] = [today_price]

        for date_data in trend_data[1:]:
            if date_data is None:
                trends[location].append("--")
            else:
                if location == "Gjennomsnittspris":
                    change = round((today_price / date_data.get(location) - 1) * 100, 3)
                else:
                    change = round((today_price / date_data.get(location)[-1] - 1) * 100, 3)

                trends[location].append(change)

    return trends


def _format_number(percent):
    if isinstance(percent, float):
        if percent >= 0:
            percent = f'+{percent}'
    return str(percent) + " %"


if __name__ == "__main__":
    price_data = load_json(JSON_FILE, PRICE_DATA)
    price_data = calculate_prices(price_data)

    save_data(price_data, HISTORY_DATA)

    history_data = extract_history(HISTORY_DATA)
    history_data = dict_from_list(history_data)
    days_data = [data_from_date(history_data, 0), data_from_date(history_data, 1),
                 data_from_date(history_data, 7), data_from_date(history_data, 31)]
    trend_data = trends_analysis(days_data)

    # Print counties and price changes
    sep_line = 89 * "-"
    print(f'{"Fylke": <30} {"Kvadratmeterpris": <20} {"Day": <15} {"Week": <15} {"Month": <12}')
    print(sep_line)

    for location, data in trend_data.items():
        if location == "Gjennomsnittspris":
            continue
        f_str = f'{location:<30} kr {"{:,}".format(data[0]).replace(",", " "): <17}'
        for i in range(1, len(data)):
            data[i] = _format_number(data[i])
            f_str += f'{data[i]: <15}'

        print(f_str)

    print(sep_line)
    avg_str = f'{"Gjennomsnittspris":<30} kr {"{:,}".format(trend_data["Gjennomsnittspris"][0]).replace(",", " "): <17}'
    for data in trend_data["Gjennomsnittspris"][1:]:
        avg_str += f'{_format_number(data): <15}'

    print(avg_str)
