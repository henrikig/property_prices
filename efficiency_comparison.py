import time
import json
import csv

JSON_FILE = "properties.json"
CSV_FILE = "properties.csv"

start_time = time.time()
counter = 0
with open(JSON_FILE) as f:
    properties = json.load(f)
    for property in properties:
        counter += 1


end_time = time.time()
print("JSON count:", counter)
print(f'JSON: Time elapsed - {(end_time-start_time)}')

start_time = time.time()
counter = 0
with open(CSV_FILE, newline="") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        counter += 1

end_time = time.time()
print("JSON count:", counter)
print(f'CSV: Time elapsed - {(end_time-start_time)}')
