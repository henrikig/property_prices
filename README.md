# property_prices
Web scraper for collecting properties from finn.no and analysing prices using scrapy

## Program Flow

- [x] Gather property data from Finn using Scrapy
- [x] Store in JSON-file
- [x] Extract data from JSON for analysis
- [x] Analyse prices per sqm
- [x] Store location specific data for each date - JSONLines? CSV?
- [x] Extract data by date for analysis
- [x] Compare todays data with yesterday, week, month and potentially year
- [ ] Send report through email
- [ ] Schedule daily data gathering with crontab


## Running the script

```
scrapy crawl properties -o properties.json && python3 trends.py
```
