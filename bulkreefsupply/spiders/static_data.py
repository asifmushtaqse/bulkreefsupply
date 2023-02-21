from datetime import datetime

today_date = datetime.now().strftime('%d%b%Y')
# api_url_t = 'http://api.scraperapi.com/?api_key=1de9f864d61b3a2b366a2049ddd728b8&url={}&keep_headers=true'

handle_httpstatus_list = [
    400, 401, 402, 403, 404, 405, 406, 407, 409,
    500, 501, 502, 503, 504, 505, 506, 507, 509,
]

req_meta = {
    'handle_httpstatus_list': handle_httpstatus_list,
    # "proxy": f"http://scraperapi:cc919ced7076a6c05b56a89e345d1266@proxy-server.scraperapi.com:8001"
}
