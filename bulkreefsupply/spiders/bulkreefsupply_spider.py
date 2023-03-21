# -*- coding: utf-8 -*-
import os
import re
import sys
import json
from copy import deepcopy

import requests
from scrapy import Request, FormRequest, Selector
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider

from static_data import today_date, req_meta
from utils import clean, get_feed, get_sitemap_urls

from dotenv import dotenv_values


def get_output_file_dir():
    config = dotenv_values(".env")
    # config = dotenv_values(f"{sys.path[2]}/bulkreefsupply/.env")
    return config['PRODUCTS_FILE_DIR'].rstrip('/')


class BulkReefSupplySpider(Spider):
    name = 'bulkreefsupply_spider'
    base_url = 'https://www.bulkreefsupply.com'
    quantity_url = 'https://www.bulkreefsupply.com/checkout/cart/add'
    sitemap_url = "https://www.bulkreefsupply.com/sitemap/google_sitemap.xml"
    faulty_urls_file_path = f'{get_output_file_dir()}/faulty_urls.csv'
    products_filename = f'{get_output_file_dir()}/bulkreefsupply_products_{today_date}.csv'

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
        'secondary_image_urls', 'quantity', 'product_url',

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

    quantity_interval = 1

    quantity_data = {
        'product': '14458',
        'form_key': 'T81MWciVSs6sD7OB',
        'qty': f'{quantity_interval}',
    }

    cookies = {
        'form_key': 'T81MWciVSs6sD7OB',
    }

    qty_headers = {
        'authority': 'www.bulkreefsupply.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_gcl_au=1.1.9844429.1674677435; _ALGOLIA=anonymous-8ea40c6f-13a3-4485-a1f1-1b26be4b90ab; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; _fbp=fb.1.1674677437586.2018576269; hubspotutk=e4cbb341029ae4fa3b931cd008b8df90; __attentive_id=051b9cf42bd747a79a188528b50e31df; __attentive_cco=1674677441884; tracker_device=4d3164bc-de31-43ed-8014-d49775c4697f; PHPSESSID=4pkb02033le4b5drh9kh4bt3h0; __utmz=81836677.1675149558.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gaexp=GAX1.2.r0-iAi_UQuGZn0yd3K3eJA.19511.1; form_key=T81MWciVSs6sD7OB; __utma=81836677.394847864.1674677435.1677089119.1678981894.4; __utmc=81836677; __hssrc=1; private_content_version=d820e9831944ffefdfcc9fede38248c2; _uetsid=cd3f2880c76d11ed855d6751abdba616; _uetvid=54446bb09cec11edbb334364d84e3f4e; _gid=GA1.2.732808888.1679350993; _ga=GA1.1.394847864.1674677435; _ga_8B3845KDDK=GS1.1.1679350993.19.0.1679350993.60.0.0; section_data_ids=%7B%22cart%22%3A1679350993%2C%22aw-afptc-promo%22%3A1678982329%7D; __hstc=138027311.e4cbb341029ae4fa3b931cd008b8df90.1674677437830.1678981894914.1679350995596.16; __hssc=138027311.1.1679350995596; __attentive_pv=1; __attentive_ss_referrer=ORGANIC; __attentive_dv=1',
        'origin': 'https://www.bulkreefsupply.com',
        'pragma': 'no-cache',
        'referer': 'https://www.bulkreefsupply.com/radion-xr30-g6-blue-led-light-fixture-ecotech-marine.html',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    def parse(self, response):
        for url in get_sitemap_urls(response):
            if not url or url.count('/') > 3 or not url.endswith('.html'):
                continue
            # if 'trate-high-range-colorimeter-hi782-marine-water-hanna-instruments.html' not in url:
            #     continue
            yield Request(url, callback=self.parse_result, headers=self.headers, meta=req_meta)
            return

    def parse_result(self, response):
        product_variants = []

        try:
            item = self.get_additional_details(response)
            item['product_card_id'] = self.get_product_cart_id(response)
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
                    # yield it
                    product_variants.append(it)
            else:
                item.update(self.get_product(prod))
                # yield item
                product_variants.append(item)
        except Exception as err:
            print(err)
            pass
            # self.write_to_csv(response.url)

        response.meta['product_variants'] = product_variants
        response.meta['qty'] = 0
        response.meta.setdefault('reverse_count', 0)

        return self.get_qty_form_request(response, callback='self.parse_quantity')

    def parse_quantity(self, response):
        if 'Successfully added to cart.' in response.text:
            yield self.get_qty_form_request(response, callback='self.parse_quantity')
            return

        for p in response.meta['product_variants']:
            p['quantity'] = response.meta['qty']
            yield p

        # return self.get_qty_form_request(response, callback='self.parse_qty_reverse', is_qty_add=False)

    def parse_qty_reverse(self, response):
        if 'Successfully added to cart.' not in response.text and response.meta['reverse_count'] < 6:
            yield self.get_qty_form_request(response, callback='self.parse_qty_reverse', is_qty_add=False)
            return

        for p in response.meta['product_variants']:
            p['quantity'] = response.meta['qty']
            yield p
        a = 0

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
        item['quantity'] = 1
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
        return clean(response.css('li:contains("Dimensions:") span::text').get()).replace('Dimensions:', '')

    def get_weight(self, response):
        return clean(response.css('li:contains("Weight:") span::text').get()).replace('Weight:', '')

    def get_product_cart_id(self, response):
        return response.css('::attr(data-product-id)').get('')

    def get_qty_form_data(self, response, is_qty_add=True):
        item = response.meta['product_variants'][0]

        if is_qty_add:
            response.meta['qty'] += self.quantity_interval
        else:
            # response.meta.setdefault('reverse_count', 0)
            response.meta['reverse_count'] += 1
            response.meta['qty'] -= 1

        data = deepcopy(self.quantity_data)
        data['qty'] = str(response.meta['qty'])
        data['product'] = item['product_card_id']
        return data

    def get_qty_form_request(self, response, callback, is_qty_add=True):
        return FormRequest(url=self.quantity_url,
                           # callback=self.parse_quantity,
                           callback=eval(callback),
                           formdata=self.get_qty_form_data(response, is_qty_add=is_qty_add),
                           headers=self.qty_headers,
                           cookies=self.cookies,
                           meta=response.meta,
                           dont_filter=True)


def run_spider_via_python_script():
    process = CrawlerProcess()
    process.crawl(BulkReefSupplySpider)
    process.start()


if __name__ == "__main__":
    run_spider_via_python_script()
