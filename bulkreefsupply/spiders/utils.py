import json
import os
import re
import time


def clean(text):
    if not text:
        return ''

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
                return

            retry_times = response.meta.get('retry_times', 0)
            if retry_times < 3:
                time.sleep(3)
                response.meta['retry_times'] = retry_times + 1
                return response.request.replace(dont_filter=True, meta=response.meta)

            spider.logger.info("Dropped after 3 retries. url: {}".format(response.url))
            response.meta.pop('retry_times', None)
            return

        return callback(spider, response)

    return wrapper


def get_sitemap_urls(response):
    return re.findall('<loc>(.*)</loc>', response.text)


def get_json_file_records(filename):
    # return json.load(open(filename, encoding='utf-8'))
    return json.loads(open(filename, encoding='utf-8').read() or '[]')


def get_jl_records(filename):
    if not os.path.exists(filename):
        return []
    return json.loads("[" + ",".join(open(filename, encoding='utf-8').readlines()) + "]" or '[]')


# records = get_json_file_records('./output/bulkreefsupply_products.json')
# keys = set()
#
# for r in records:
#     keys.update(list(r['more_details'].keys()))
#
#
# print(len(keys))
# print(keys)
