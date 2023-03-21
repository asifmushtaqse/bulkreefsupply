# import requests
#
# cookies = {
#     # '_gcl_au': '1.1.9844429.1674677435',
#     # '_ALGOLIA': 'anonymous-8ea40c6f-13a3-4485-a1f1-1b26be4b90ab',
#     # 'mage-cache-storage': '%7B%7D',
#     # 'mage-cache-storage-section-invalidation': '%7B%7D',
#     # 'mage-cache-sessid': 'true',
#     # 'mage-messages': '',
#     # 'recently_viewed_product': '%7B%7D',
#     # 'recently_viewed_product_previous': '%7B%7D',
#     # 'recently_compared_product': '%7B%7D',
#     # 'recently_compared_product_previous': '%7B%7D',
#     # 'product_data_storage': '%7B%7D',
#     # '_fbp': 'fb.1.1674677437586.2018576269',
#     # 'hubspotutk': 'e4cbb341029ae4fa3b931cd008b8df90',
#     # '__attentive_id': '051b9cf42bd747a79a188528b50e31df',
#     # '__attentive_cco': '1674677441884',
#     # 'tracker_device': '4d3164bc-de31-43ed-8014-d49775c4697f',
#     # 'PHPSESSID': '4pkb02033le4b5drh9kh4bt3h0',
#     # '__utmz': '81836677.1675149558.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
#     # '_gaexp': 'GAX1.2.r0-iAi_UQuGZn0yd3K3eJA.19511.1',
#     'form_key': 'T81MWciVSs6sD7OB',
#     # '__utma': '81836677.394847864.1674677435.1677089119.1678981894.4',
#     # '__utmc': '81836677',
#     # '__hssrc': '1',
#     # 'private_content_version': 'd820e9831944ffefdfcc9fede38248c2',
#     # '_uetsid': 'cd3f2880c76d11ed855d6751abdba616',
#     # '_uetvid': '54446bb09cec11edbb334364d84e3f4e',
#     # '_gid': 'GA1.2.732808888.1679350993',
#     # '_ga': 'GA1.1.394847864.1674677435',
#     # '_ga_8B3845KDDK': 'GS1.1.1679350993.19.0.1679350993.60.0.0',
#     # 'section_data_ids': '%7B%22cart%22%3A1679350993%2C%22aw-afptc-promo%22%3A1678982329%7D',
#     # '__hstc': '138027311.e4cbb341029ae4fa3b931cd008b8df90.1674677437830.1678981894914.1679350995596.16',
#     # '__hssc': '138027311.1.1679350995596',
#     # '__attentive_pv': '1',
#     # '__attentive_ss_referrer': 'ORGANIC',
#     # '__attentive_dv': '1',
# }
#
# headers = {
#     'authority': 'www.bulkreefsupply.com',
#     'accept': 'application/json, text/javascript, */*; q=0.01',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'cache-control': 'no-cache',
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     # 'cookie': '_gcl_au=1.1.9844429.1674677435; _ALGOLIA=anonymous-8ea40c6f-13a3-4485-a1f1-1b26be4b90ab; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; _fbp=fb.1.1674677437586.2018576269; hubspotutk=e4cbb341029ae4fa3b931cd008b8df90; __attentive_id=051b9cf42bd747a79a188528b50e31df; __attentive_cco=1674677441884; tracker_device=4d3164bc-de31-43ed-8014-d49775c4697f; PHPSESSID=4pkb02033le4b5drh9kh4bt3h0; __utmz=81836677.1675149558.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gaexp=GAX1.2.r0-iAi_UQuGZn0yd3K3eJA.19511.1; form_key=T81MWciVSs6sD7OB; __utma=81836677.394847864.1674677435.1677089119.1678981894.4; __utmc=81836677; __hssrc=1; private_content_version=d820e9831944ffefdfcc9fede38248c2; _uetsid=cd3f2880c76d11ed855d6751abdba616; _uetvid=54446bb09cec11edbb334364d84e3f4e; _gid=GA1.2.732808888.1679350993; _ga=GA1.1.394847864.1674677435; _ga_8B3845KDDK=GS1.1.1679350993.19.0.1679350993.60.0.0; section_data_ids=%7B%22cart%22%3A1679350993%2C%22aw-afptc-promo%22%3A1678982329%7D; __hstc=138027311.e4cbb341029ae4fa3b931cd008b8df90.1674677437830.1678981894914.1679350995596.16; __hssc=138027311.1.1679350995596; __attentive_pv=1; __attentive_ss_referrer=ORGANIC; __attentive_dv=1',
#     'origin': 'https://www.bulkreefsupply.com',
#     'pragma': 'no-cache',
#     'referer': 'https://www.bulkreefsupply.com/radion-xr30-g6-blue-led-light-fixture-ecotech-marine.html',
#     'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"macOS"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
# }
#
# data = {
#     'product': '14458',
#     'form_key': 'T81MWciVSs6sD7OB',
#     'qty': '5',
# }
#
# response = requests.post('https://www.bulkreefsupply.com/checkout/cart/add', cookies=cookies, headers=headers, data=data)
# print(response.text)
# a = 0
