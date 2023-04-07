# import requests
#
# from scrapingbee import ScrapingBeeClient
# from static_data import scrapingbee_api_key, proxies
#
#
# def send_request():
#     cart_url = "https://www.bulkreefsupply.com/checkout/cart/add"
#
#     cookies = {
#         'form_key': 'T81MWciVSs6sD7OB',
#     }
#
#     headers = {
#         'authority': 'www.bulkreefsupply.com',
#         'accept': 'application/json, text/javascript, */*; q=0.01',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#         'cache-control': 'no-cache',
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'origin': 'https://www.bulkreefsupply.com',
#         'pragma': 'no-cache',
#         'referer': 'https://www.bulkreefsupply.com/1-4-x-1-4-male-npt-nipple.html',
#         'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#         'x-requested-with': 'XMLHttpRequest',
#     }
#
#     data = {
#         'product': '104',
#         'form_key': 'T81MWciVSs6sD7OB',
#         'qty': '5',
#     }
#
#     # response = requests.post(
#     #     # url='https://app.scrapingbee.com/api/v1/',
#     #     url='https://www.bulkreefsupply.com/checkout/cart/add',
#     #
#     #     params={
#     #         'api_key': scrapingbee_api_key,
#     #         # 'url': 'https://www.bulkreefsupply.com/checkout/cart/add',
#     #         # 'url': 'https://app.scrapingbee.com/api/v1/',
#     #     },
#     #
#     #     cookies=cookies,
#     #     headers=headers,
#     #     data=data
#     # )
#
#     # response = requests.post(
#     #     url="https://app.scrapingbee.com/api/v1",
#     #     # url='https://www.bulkreefsupply.com/checkout/cart/add',
#     #
#     #     params={
#     #         # "url": "https://httpbin.org/anything",
#     #         'url': 'https://www.bulkreefsupply.com/checkout/cart/add',
#     #         "api_key": scrapingbee_api_key,
#     #         'premium_proxy': 'true',
#     #         # 'stealth_proxy': 'true',
#     #     },
#     #
#     #     data=data,
#     #     headers=headers,
#     #     cookies=cookies,
#     #     proxies=proxies,
#     # )
#     # print('Response HTTP Status Code: ', response.status_code)
#     # print('Response HTTP Response Body: ', response.content)
#
#     client = ScrapingBeeClient(api_key=scrapingbee_api_key)
#
#     response = client.post(
#         url=cart_url,
#         data=data,
#         headers=headers,
#         cookies=cookies,
#     )
#
#     print('Response HTTP Status Code: ', response.status_code)
#     print('Response HTTP Response Body: ', response.content)
#
#     a = 0
#
#
# # send_request()
