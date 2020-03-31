from datetime import date, timedelta
import json

HISTORY_DATA = "price_history.jl"

history_data = []

# Extract data from price history file
with open(HISTORY_DATA, 'r') as f:
    for line in f:
        history_data.append(json.loads(line))

# Reformat data to dict of dates
history_data = {list(item.keys())[0]: list(item.values())[0] for item in history_data}

# Get today's date, as well as last week and last month and associated data
today = date.today()
week_delta, month_delta = timedelta(weeks=1), timedelta(days=31)
one_week_ago, one_month_ago = today - week_delta, today - month_delta
today = history_data.get(str(today))
one_week_ago = history_data.get(str(one_week_ago))
one_month_ago = history_data.get(str(one_month_ago))


# Create dict containing today's, last week's and month's data
# OUTPUT: {'Oslo': [today_avg, %_week, %_month], ... }
trends = dict()
for location in today:
    if location == "Gjennomsnittspris":
        continue
    today_price = today[location][-1]
    if one_week_ago:
        week_price = one_week_ago[location][-1]
    else:
        week_price = 0
    if one_month_ago:
        month_price = one_month_ago[location][-1]
    else:
        month_price = 0

    try:
        week_change = round((today_price/week_price-1)*100, 3)
    except ZeroDivisionError:
        week_change = "--"
    try:
        month_change = round((today_price/month_price-1)*100, 3)
    except ZeroDivisionError:
        month_change = "--"

    trends[location] = [today_price, week_change, month_change]


# Print counties and price changes
sep_line = 73*"-"
print(f'{"Fylke": <30} {"Kvadratmeterpris": <20} {"Week": <15} {"Month": <12}')
print(sep_line)

for location, data in trends.items():
    if location == "Gjennomsnittspris":
        continue
    if isinstance(data[1], float):
        if data[1] >= 0:
            data[1] = f'+{data[1]}'
    if isinstance(data[2], float):
        if data[2] >= 0:
            data[2] = f'+{data[2]}'
    data[1], data[2] = str(data[1]) + " %", str(data[2]) + " %"
    print(f'{location:<30} kr {"{:,}".format(data[0]).replace(",", " "): <17} {data[1]: <15} {data[2]: <12}')


print(sep_line)
print(f'{"Gjennomsnittspris":<30} kr {"{:,}".format(today["Gjennomsnittspris"]).replace(",", " ")}')
