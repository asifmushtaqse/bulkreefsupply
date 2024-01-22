import json
import os
import re
import sys
import time
from copy import deepcopy
from csv import DictReader, field_size_limit
from datetime import datetime
from html import unescape

from dotenv import dotenv_values

from .static_data import csv_headers, scrapingbee_proxy_url, scrapingbee_premium_proxy_url, \
    scrapingbee_stealth_proxy_url, PRODUCTS_FILE_DIR


def clean(text):
    if not text:
        return ''

    text = re.sub(u'"', u"\u201C", unescape(text or ''))
    text = re.sub(u"'", u"\u2018", text)

    if text and isinstance(text, str):
        for c in ['\r\n', '\n\r', u'\n', u'\r', u'\t', u'\xa0']:
            text = text.replace(c, ' ')
        return re.sub(' +', ' ', text).strip()

    return text


def get_feed(uri, feed_format='csv', fields=None, indent=4, overwrite=False):
    return {
        uri: {
            'format': feed_format,
            'encoding': 'utf8',
            'fields': fields,
            'indent': indent,
            'overwrite': overwrite
        }
    }


def retry_invalid_response(callback):
    def wrapper(spider, response):
        if response.status >= 400:
            if response.status == 404:
                spider.logger.info('Page not found.')

                # If Sitemap URL is not working the extract product links by crawling categories pages.
                if spider.sitemap_url in response.url:
                    return spider.get_categories_requests()

                return spider.get_next_product_request(response)

            retry_times = response.meta.get('retry_times', 0)
            if retry_times < 3:
                time.sleep(2)
                response.meta['retry_times'] = retry_times + 1
                return response.request.replace(dont_filter=True, meta=response.meta)

            spider.logger.info("Dropped after 3 retries. url: {}".format(response.url))
            response.meta.pop('retry_times', None)
            return spider.get_next_product_request(response)

        return callback(spider, response)

    return wrapper


def get_actual_url(response):
    if isinstance(response, str):
        # return response.split('url=')[-1].split('&')[0]
        return response.split('url=')[-1].split('.html')[0] + '.html'

    # return response.url.split('url=')[-1].split('&')[0]
    return response.url.split('url=')[-1].split('.html')[0] + '.html'


def get_proxy_url(url, is_premium=False, is_stealth=False):
    if is_premium:
        return scrapingbee_premium_proxy_url.format(url)
    if is_stealth:
        return scrapingbee_stealth_proxy_url.format(url)

    return scrapingbee_proxy_url.format(url)


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def get_sitemap_urls(response):
    return re.findall('<loc>(.*)</loc>', response.text)


def get_json_file_records(filename):
    # return json.load(open(filename, encoding='utf-8'))
    return json.loads(open(filename, encoding='utf-8').read() or '[]')


def get_jl_records(filename):
    if not os.path.exists(filename):
        return []
    # return json.loads("[" + ",".join(open(filename, encoding='utf-8').readlines()) + "]" or '[]')
    return [eval(r.replace(',{', '{')) for r in open(filename, encoding='utf-8').readlines() if r]


def get_output_file_dir():
    # config = dotenv_values(".env")
    # config = dotenv_values(f"{sys.path[2]}/bulkreefsupply/.env")
    # return config['PRODUCTS_FILE_DIR'].rstrip('/')
    return PRODUCTS_FILE_DIR.rstrip('/')


def get_filename_t(is_scrape_daily=False):
    if is_scrape_daily:
        return get_output_file_dir() + '/brs_daily_products_{f_no}.csv'
    return get_output_file_dir() + '/bulkreefsupply_products_{f_no}.csv'


def get_csv_feed_file_name(is_scrape_daily=False):
    last_created_file_no = get_last_created_file_no(is_scrape_daily)

    if should_create_new_file(is_scrape_daily):
        return get_filename_t(is_scrape_daily).format(f_no=last_created_file_no + 1)

    return get_filename_t(is_scrape_daily).format(f_no=last_created_file_no)


def get_report_file_name(is_scrape_daily):
    last_file_no = get_last_created_file_no(is_scrape_daily)
    return get_filename_t().format(f_no=last_file_no)


def get_last_created_file_no(is_scrape_daily):
    files_numbers = get_output_file_numbers(is_scrape_daily)

    if not files_numbers:
        return 0

    return max(files_numbers)


def get_last_report_records(is_scrape_daily=False):
    file_name = get_filename_t(is_scrape_daily).format(f_no=get_last_created_file_no(is_scrape_daily))
    return get_csv_records(file_name)


def get_csv_records(filepath):
    if not os.path.exists(filepath):
        return []
    return [dict(r) for r in DictReader(open(filepath, encoding='utf-8')) if r]


def should_create_new_file(is_scrape_daily):
    records = get_last_report_records(is_scrape_daily)

    if not records:
        return True

    str_dates = list({k.replace('quantity_', '') for k, val in records[0].items()
                      if val and 'quantity_' in k and k != val})
    if not str_dates:
        return True
    days_diff = (datetime.now() - convert_to_datetime(get_old_date(str_dates))).days

    if days_diff > 60:
        return True

    return False


def convert_to_datetime(str_date):
    return datetime.strptime(str_date, get_date_format())


def get_date_format():
    # return '%d-%m-%Y'
    return '%d%b%Y'


def get_today_date():
    return datetime.now().strftime(get_date_format())


def get_old_date(str_dates):
    str_dates.sort(key=lambda date: datetime.strptime(date, get_date_format()))
    return str_dates[0]


def get_output_file_numbers(is_scrape_daily):
    files = []
    output_files_dir = get_output_file_dir()

    create_dir(get_output_file_dir())

    for file_path in os.listdir(output_files_dir):
        if '.csv' not in file_path:
            continue
        file_path = output_files_dir + '/' + file_path
        files.append(file_path)

    # return [int(f_no) for f in files if 'bulkreefsupply_products_' in f and
    #         (f_no := f.replace('.csv', '').split('_')[-1].strip()) and f_no.isdigit()]
    if is_scrape_daily:
        return [int(get_file_no(f)) for f in files if 'brs_daily_products' in f and get_file_no(f).isdigit()]

    return [int(get_file_no(f)) for f in files if 'bulkreefsupply_products_' in f and get_file_no(f).isdigit()]


def get_file_no(file_name):
    return file_name.replace('.csv', '').split('_')[-1].strip()


def get_next_quantity_column():
    return f'quantity_{get_today_date()}'


def get_csv_headers(is_scrape_daily=False):
    header_cols = deepcopy(csv_headers)

    records = get_last_report_records(is_scrape_daily)

    if not records or should_create_new_file(is_scrape_daily):
        header_cols.append(get_next_quantity_column())
        return header_cols

    qty_columns = []

    for k, v in records[0].items():
        if 'quantity_' in k and k not in qty_columns:
            qty_columns.append(k)

    header_cols.extend(qty_columns)

    if get_next_quantity_column() not in header_cols:
        header_cols.append(get_next_quantity_column())

    return header_cols


def increase_column_size_limit():
    maxInt = sys.maxsize

    while True:
        try:
            field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

# records = get_json_file_records('./output/bulkreefsupply_products.json')
# keys = set()
#
# for r in records:
#     keys.update(list(r['more_details'].keys()))
#
#
# print(len(keys))
# print(keys)
