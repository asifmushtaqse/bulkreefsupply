# -*- coding: utf-8 -*-
import os
import re
import json
from copy import deepcopy

from scrapy import Request
from scrapy.spiders import Spider

from ..static_data import today_date, req_meta
from ..utils import clean, get_feed, get_sitemap_urls


class BulkReefSupplySpider(Spider):
    name = 'bulkreefsupply_spider'
    base_url = 'https://www.bulkreefsupply.com'
    faulty_urls_file_path = f'../output/faulty_urls.csv'
    products_filename = f'../output/bulkreefsupply_products_{today_date}.csv'
    sitemap_url = "https://www.bulkreefsupply.com/sitemap/google_sitemap.xml"

    start_urls = [
        sitemap_url,
    ]

    # sitemap_urls = [
    #     sitemap_url,
    # ]
    #
    # sitemap_rules = [
    #     ('.html', 'parse'),
    # ]

    handle_httpstatus_list = [
        400, 401, 402, 403, 404, 405, 406, 407, 409,
        500, 501, 502, 503, 504, 505, 506, 507, 509,
    ]

    csv_headers = [
        'product_id', 'product_name', 'upc', 'vendor', 'sku', 'price',
        'in_stock', 'description', 'has_variants', 'main_image_url',
        'secondary_image_urls', 'product_url',

        # More information fields
        'fluorescent_bulb_wattage', 'maximum_system_volume', 'control_type', 'aquarium_type',
        'compatible_with_controllers', 'included_mounting', 'wattage', 'optional_mounts',
        'ml_per_minute', 'short_name_for_grouped_product', 'media_capacity', 'filter_dimensions', 'main_ingredient',
        'skimmer_body_types', 'bulb_color/temperature', 'system_size', 'variable_speed', 'power_cord_length',
        'pvc_connection_type', 'additive_type', 'max._light_coverage_(width)', 'max._light_coverage_(length)',
        'adhesive_type', 'out_of_stock_message', 'micron_rating', 'manuals', 'recommended_tank_size',
        'tubing_inside_diameter', 'aquarium_size', 'reactor_placement', 'lighting_type', 'system_type', 'color',
        'max_head_height', 'duty_rating', 'warranty', 'alarms', 'number_of_leds', 'dimensions', 'weight'
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'FEEDS': get_feed(products_filename, feed_format='csv', fields=csv_headers, overwrite=True),
    }

    headers = {
        'authority': 'www.bulkreefsupply.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    def parse(self, response):
        for url in get_sitemap_urls(response):
            if not url or url.count('/') > 3 or not url.endswith('.html'):
                continue
            # if 'trate-high-range-colorimeter-hi782-marine-water-hanna-instruments.html' not in url:
            #     continue
            yield Request(url, callback=self.parse_result, headers=self.headers, meta=req_meta)

    def parse_result(self, response):
        try:
            item = self.get_additional_details(response)
            item["weight"] = self.get_weight(response)
            item["dimensions"] = self.get_dimensions(response)
            item["description"] = self.get_description(response)
            item["description"] = self.get_description(response)
            item['main_image_url'] = self.get_main_image(response)
            item["secondary_image_urls"] = self.get_image_urls(response)
            # item['more_details'] = self.get_additional_details(response)
            # if 'upc' in item['more_details']:
            #     item['upc'] = item['more_details']['upc']
            item["product_url"] = response.url
            item['has_variants'] = False
            # item['variants'] = []

            prod = self.get_product_data(response)

            if 'children' in prod:
                item['has_variants'] = True

                for p in prod['children']:
                    it = deepcopy(item)
                    it.update(self.get_product(p))
                    yield it
            else:
                item.update(self.get_product(prod))
                yield item
        except Exception as err:
            pass
            # print(err)
            # self.write_to_csv(response.url)

    def get_product_data(self, response):
        prod = json.loads(response.css('[type="application/ld+json"]::text')[1].get())
        return prod

    def get_product(self, prod):
        item = {}
        item['product_id'] = prod['productID']
        item["product_name"] = prod['name']
        item["vendor"] = prod['brand']
        item["sku"] = prod['sku']
        item["price"] = prod['offers']['price']
        # item["description"] = prod['description']
        item['in_stock'] = 'instock' in prod['offers']['availability'].lower()
        return item

    def get_title(self, response):
        return clean(response.css('.product_title::text').get())

    def get_regular_price(self, response):
        return clean(response.css('.summary.entry-summary .price del bdi::text').get()) or self.get_sale_price(response)

    def get_sale_price(self, response):
        return clean(response.css('.summary.entry-summary .price bdi::text').getall()[-1])

    def get_image_urls(self, response):
        try:
            raw = [raw for raw in response.css('[type="text/x-magento-init"]::text').getall()
                   if 'mage/gallery/gallery' in raw and 'thumbs' in raw]

            raw = json.loads(raw[0])
            data = raw.get('[data-gallery-role=gallery-placeholder]', {}).get('mage/gallery/gallery', {}).get('data',
                                                                                                              {})
            return ", ".join([self.clean_image_url(r['thumb'][0]) for r in data])

        except Exception as image_err:
            print(image_err)

        return ", ".join([self.clean_image_url(response.css('::attr("data-product-image")').get())])

    def get_additional_details(self, response):
        details = {}

        for sel in response.css('#product-attribute-specs-table tbody tr'):
            if not (key := self.get_key(sel)):
                continue
            details[key] = clean(sel.css('td.col.data::text').get())

        return details

    def get_key(self, sel):
        return sel.css('th.col.label::text').get('').strip().replace(' ', '_').lower()

    def clean_image_url(self, url):
        code = re.findall(r'cache/(.*?)/', url)[0]
        return url.replace(f'/cache/{code}', '')

    def write_to_csv(self, url):
        csv_writer = self.get_csv_writer()
        csv_writer.write(url + '\n')
        csv_writer.close()
        print("URL = " + url)

    def get_csv_writer(self):
        if not os.path.exists(self.faulty_urls_file_path):
            file = open(self.faulty_urls_file_path, mode='w', encoding='utf-8')
            file.write(','.join(h for h in ['url']) + '\n')
            return file
        return open(self.faulty_urls_file_path, mode='a', encoding='utf-8')

    def get_main_image(self, response):
        return self.clean_image_url(response.css('::attr("data-product-image")').get())

    def get_description(self, response):
        return response.css('#description').get()

    def get_dimensions(self, response):
        return clean(response.css('li:contains("Dimensions:") span::text').get())

    def get_weight(self, response):
        return clean(response.css('li:contains("Weight:") span::text').get())
