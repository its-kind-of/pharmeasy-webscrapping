import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv


class Pharmeasy(scrapy.Spider):
    name = 'pharmeasy'
    base_url = 'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=89&page='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    def __init__(self):
        with open('pharmeasy.csv', 'w') as csv_file:
            csv_file.write('name, slug, manufacturer, price, availability, images\n')

    def start_requests(self):
        # scrape data from infinite scroll
        for page in range(1, 33):
            next_page = self.base_url + str(page)
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        data = ''
        with open('pharmeasy.json', 'r') as json_file:
            #json_file.write(response.text)
            for line in json_file.read():
                data+= line

        data = json.loads(data)
        #print(json.dumps(data, indent=2))

        # data extraction
        for product in data['data']['products']:
            items = {
                'name': product['name'],
                'slug': product['slug'],
                'manufacturer': product['manufacturer'],
                'price': product['salePriceDecimal'],
                'availability': product['productAvailabilityFlags']['isAvailable'],
                'images': ','.join(product['images'])
            }

            #print(json.dumps(items, indent=2))
            #print(items.keys())
            # append results to csv file
            with open('pharmeasy.csv', 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=items.keys())
                writer.writerow(items)

# # run scraper
process = CrawlerProcess()
process.crawl(Pharmeasy)
process.start()

# debug data extraction
# Pharmeasy.parse(Pharmeasy, '')