# -*- coding: utf-8 -*-
import os
import re
import json
from copy import deepcopy
from csv import DictReader

from scrapy import Request, FormRequest
from scrapy.spiders import Spider

from .static_data import req_meta, category_urls
from .utils import clean, get_feed, get_sitemap_urls, get_output_file_dir, get_csv_headers, \
    get_csv_feed_file_name, get_today_date, get_last_report_records, get_next_quantity_column, \
    retry_invalid_response


def get_existing_records():
    return {r['product_url'].rstrip('/'): dict(r) for r in get_last_report_records()
            if r and r['product_url'] != 'product_url'}


class BulkReefSupplySpider(Spider):
    name = 'bulkreefsupply_spider'
    base_url = 'https://www.bulkreefsupply.com'
    quantity_url = 'https://www.bulkreefsupply.com/checkout/cart/add'
    sitemap_url = "https://www.bulkreefsupply.com/sitemap/google_sitemap.xml"
    # products_filename = f'{get_output_file_dir()}/bulkreefsupply_products_{}.csv'
    products_filename = get_csv_feed_file_name()
    logs_dir = "logs"
    logs_file_path = f"{logs_dir}/{name}_logs.log"

    quantity_interval = 5

    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    if os.path.exists(logs_file_path):
        os.remove(logs_file_path)

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

    csv_headers = get_csv_headers()

    existing_records = get_existing_records()

    custom_settings = {
        # 'LOG_LEVEL': 'INFO',
        'LOG_FILE': logs_file_path,

        # 'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        # 'FEEDS': get_feed(products_filename, feed_format='csv', fields=get_csv_headers(), overwrite=True),

        "ROTATING_PROXY_LIST_PATH": 'proxies.txt',
        "DOWNLOADER_MIDDLEWARES": {
            'bulkreefsupply.middlewares.BulkreefsupplyDownloaderMiddleware': 543,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        },
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

    qty_headers = {
        'authority': 'www.bulkreefsupply.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.bulkreefsupply.com',
        'pragma': 'no-cache',
        # 'referer': 'https://www.bulkreefsupply.com/radion-xr30-g6-blue-led-light-fixture-ecotech-marine.html',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    quantity_data = {
        'product': '14458',
        'form_key': 'T81MWciVSs6sD7OB',
        'qty': f'{quantity_interval}',
    }

    cookies = {
        'form_key': 'T81MWciVSs6sD7OB',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cookiejar = 0
        self.seen_urls = []
        self.delete_file(self.products_filename)

    def start_requests(self):
        yield Request(self.base_url, callback=self.parse, headers=self.headers)
        yield Request(self.sitemap_url, callback=self.parse_sitemap, headers=self.headers)
        yield from [Request(url=url, callback=self.parse_listings, headers=self.headers) for url in category_urls]

    @retry_invalid_response
    def parse(self, response):
        return self.get_product_requests(response, self.existing_records)

    @retry_invalid_response
    def parse_sitemap(self, response):
        return self.get_product_requests(response, get_sitemap_urls(response)[:])

    @retry_invalid_response
    def parse_listings(self, response):
        css = '.product-item-photo::attr(href), .product.product-item a::attr(href)'
        product_urls = [response.urljoin(url) for url in response.css(css).getall()]
        return self.get_product_requests(response, product_urls)

    @retry_invalid_response
    def parse_details(self, response):
        try:
            item = response.meta['item']
            item.update(self.get_additional_details(response))
            item['date'] = get_today_date()
            item["weight"] = self.get_weight(response)
            item["dimensions"] = self.get_dimensions(response)
            # item["description"] = self.get_description(response)
            # item['main_image_url'] = self.get_main_image(response)
            # item["secondary_image_urls"] = self.get_image_urls(response)
            item["product_url"] = response.url
            item['has_variants'] = False
            # item['variants'] = []
            # item['more_details'] = self.get_additional_details(response)
            # if 'upc' in item['more_details']:
            #     item['upc'] = item['more_details']['upc']

            prod = self.get_product_data(response)

            if 'children' in prod:
                item['has_variants'] = True

                for p in prod['children']:
                    try:
                        it = deepcopy(item)
                        it.update(self.get_product(p))
                        it['product_cart_id'] = self.get_product_cart_id(response, sku=it['product_id'])

                        self.append_cart_request(response, callback='self.parse_quantity', item=it)
                    except Exception as variant_err:
                        self.logger.debug(f"Got Variant Error:\n{variant_err}")
            else:
                item.update(self.get_product(prod))
                item['product_cart_id'] = self.get_product_cart_id(response, sku=item['product_id'])

                self.append_cart_request(response, callback='self.parse_quantity', item=item)
        except Exception as err:
            self.logger.debug(f"Got Error While Parsing Product {response.url}:\n {err}")
            a = 0

        return self.get_next_product_request(response)

    @retry_invalid_response
    def parse_quantity(self, response):
        # If a product quantity reach to the maximum limit
        if response.meta['item']['qty'] > 1000:
            item = response.meta['item']
            item[get_next_quantity_column()] = item.pop('qty')
            yield self.write_to_csv(item)
            yield self.get_next_product_request(response)
            return

        if 'successfully added to cart.' in response.text.lower():
            yield self.get_add_to_cart_quantity_request(response, callback='self.parse_quantity')
            return

        # item = response.meta['item']
        # item[get_next_quantity_column()] = item.pop('qty') - 1
        # yield from self.write_to_csv(item)
        # yield self.get_product_request(response)

        yield self.get_add_to_cart_quantity_request(response, callback='self.parse_qty_reverse', is_qty_add=False)

    @retry_invalid_response
    def parse_qty_reverse(self, response):
        if 'the requested qty is not available' in response.text.lower() and \
                response.meta['item']['reverse_count'] < self.quantity_interval + 1:
            yield self.get_add_to_cart_quantity_request(response, callback='self.parse_qty_reverse', is_qty_add=False)
            return

        item = response.meta['item']
        item[get_next_quantity_column()] = item.pop('qty')
        yield self.write_to_csv(item)
        yield self.get_next_product_request(response)

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
        # item['quantity'] = 1
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
            # if not (key := self.get_key(sel)):
            #     continue
            key = self.get_key(sel)
            if not key:
                continue
            details[key] = clean(sel.css('td.col.data::text').get())

        return details

    def get_key(self, sel):
        return sel.css('th.col.label::text').get('').strip().replace(' ', '_').lower()

    def clean_image_url(self, url):
        code = re.findall(r'cache/(.*?)/', url)[0]
        return url.replace(f'/cache/{code}', '')

    def get_main_image(self, response):
        return self.clean_image_url(response.css('::attr("data-product-image")').get())

    def get_description(self, response):
        return response.css('#description').get()

    def get_dimensions(self, response):
        return clean(response.css('li:contains("Dimensions:") span::text').get()).replace('Dimensions:', '')

    def get_weight(self, response):
        return clean(response.css('li:contains("Weight:") span::text').get()).replace('Weight:', '')

    def get_product_cart_id(self, response, sku):
        # return response.css('::attr(data-product-id)').get('')
        return response.css(f'[data-product-sku="{sku}"]::attr(data-product-id)').get('')

    def get_qty_form_data(self, response, item, is_qty_add=True):
        if is_qty_add:
            item['qty'] += self.quantity_interval
        else:
            item['reverse_count'] += 1
            item['qty'] -= 1

        data = deepcopy(self.quantity_data)
        data['qty'] = str(item['qty'])
        data['product'] = item['product_cart_id']
        return data

    def get_add_to_cart_quantity_request(self, response, callback, is_qty_add=True):
        return self.get_cart_request(response, callback, response.meta['item'], response.meta, is_qty_add)

    def append_cart_request(self, response, callback, item, is_qty_add=True):
        item['reverse_count'] = 0
        item['qty'] = 0

        meta = deepcopy(req_meta)
        meta['item'] = item

        add_to_cart_request = self.get_cart_request(response, callback, item, meta, is_qty_add)

        response.meta['product_requests'].insert(0, add_to_cart_request)

    def get_cart_request(self, response, callback, item, meta, is_qty_add=True):
        self.cookiejar += 1
        meta['cookiejar'] = self.cookiejar
        # response.meta['cookiejar'] = self.cookiejar

        req_headers = deepcopy(self.headers)
        req_headers['referer'] = item['product_url']

        return FormRequest(url=self.quantity_url,
                           # callback=self.parse_quantity,
                           callback=eval(callback),
                           formdata=self.get_qty_form_data(response, item, is_qty_add=is_qty_add),
                           headers=req_headers,
                           cookies=self.cookies,
                           meta=meta,
                           dont_filter=True,
                           )

    def write_to_csv(self, item):
        row = ','.join('"{}"'.format(item.get(h, '')) for h in self.csv_headers) + '\n'
        csv_writer = self.get_csv_writer()
        csv_writer.write(row)
        csv_writer.close()
        return item

    def get_csv_writer(self):
        # file = open(self.output_csv_file_name, mode='w', encoding='utf-8')
        # file.write(','.join(h for h in file_headers) + '\n')
        # return file

        if not os.path.exists(self.products_filename) or len(self.has_records()) < 1:
            file = open(self.products_filename, mode='w', encoding='utf-8')
            file.write(','.join(h for h in self.csv_headers) + '\n')
            return file

        return open(self.products_filename, mode='a', encoding='utf-8')

    def has_records(self):
        if not os.path.exists(self.products_filename):
            return []
        return [r['product_url'] for r in
                DictReader(open(self.products_filename, encoding='utf-8')) if r and r['product_url']]

    def delete_file(self, path):
        if os.path.exists(path):
            # os.remove(path)
            os.rename(path, f"{'/'.join(path.split('/')[:-1])}/previous_report_backup.csv")

    def get_next_product_request(self, response):
        if response.meta['product_requests']:
            req = response.meta['product_requests'].pop(0)
            req.meta['product_requests'] = response.meta['product_requests']
            return req

    def get_product_requests(self, response, product_urls):
        for url in product_urls:
            url = url.rstrip('/')
            if not url or url.count('/') > 3 or not url.endswith('.html') or url in self.seen_urls:
                continue
            self.seen_urls.append(url)

            # if 'blade-smart-led-strip-freshwater-aqua-illumination.html' not in url:  # variants
            # if 'radion-xr30-g6-blue-led-light-fixture-ecotech-marine.html' not in url:
            #     continue

            meta = deepcopy(req_meta)
            meta['item'] = self.existing_records.get(url.rstrip('/'), {})
            # meta['item']['product_url'] = url
            # yield meta['item']

            req = Request(url, callback=self.parse_details, headers=self.headers, meta=meta)

            response.meta.setdefault('product_requests', []).append(req)

        return self.get_next_product_request(response)
