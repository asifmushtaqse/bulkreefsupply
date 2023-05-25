# -*- coding: utf-8 -*-

from csv import DictReader

from scrapy.spiders import Spider

from bulkreefsupply.spiders.utils import clean, get_feed, get_csv_headers


class ParseCSVSpider(Spider):
    name = 'parse_csv_spider'
    products_filename = "../output/bulkreefsupply_products_new.csv"

    start_urls = [
        "http://quotes.toscrape.com/",
    ]

    handle_httpstatus_list = [
        400, 401, 402, 403, 404, 405, 406, 407, 409,
        500, 501, 502, 503, 504, 505, 506, 507, 509,
    ]

    csv_headers = get_csv_headers()

    custom_settings = {
        'FEEDS': get_feed(products_filename, feed_format='csv', fields=csv_headers, overwrite=True),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response):
        products = {r['product_id']: dict(r) for r in
                    DictReader(open('../backup/bulkreefsupply_products_1.csv'))}

        for item in DictReader(open('../output/bulkreefsupply_products_1.csv')):
            item['quantity_10Apr2023'] = products.get(item['product_id'], {}).get('quantity_10Apr2023')
            item['quantity_13Apr2023'] = products.get(item['product_id'], {}).get('quantity_13Apr2023')
            item['quantity_28Apr2023'] = products.get(item['product_id'], {}).get('quantity_28Apr2023')
            yield item
