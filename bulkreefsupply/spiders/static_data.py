from datetime import datetime

today_date = datetime.now().strftime('%d%b%Y')
# api_url_t = 'http://api.scraperapi.com/?api_key=1de9f864d61b3a2b366a2049ddd728b8&url={}&keep_headers=true'

handle_httpstatus_list = [
    400, 401, 402, 403, 404, 405, 406, 407, 409,
    500, 501, 502, 503, 504, 505, 506, 507, 509,
]

req_meta = {
    # 'dont_merge_cookies': True,
    'handle_httpstatus_list': handle_httpstatus_list,
    # "proxy": f"http://scraperapi:cc919ced7076a6c05b56a89e345d1266@proxy-server.scraperapi.com:8001"
}

csv_headers = [
    'date', 'product_id', 'product_name', 'upc', 'vendor', 'sku', 'price', 'in_stock',
    'has_variants', 'product_url', 'product_cart_id',
    #  'main_image_url', 'secondary_image_urls', 'quantity', 'description',

    # More information fields
    # 'fluorescent_bulb_wattage', 'maximum_system_volume', 'control_type', 'aquarium_type',
    # 'compatible_with_controllers', 'included_mounting', 'wattage', 'optional_mounts',
    # 'ml_per_minute', 'short_name_for_grouped_product', 'media_capacity', 'filter_dimensions', 'main_ingredient',
    # 'skimmer_body_types', 'bulb_color/temperature', 'system_size', 'variable_speed', 'power_cord_length',
    # 'pvc_connection_type', 'additive_type', 'max._light_coverage_(width)', 'max._light_coverage_(length)',
    # 'adhesive_type', 'out_of_stock_message', 'micron_rating', 'manuals', 'recommended_tank_size',
    # 'tubing_inside_diameter', 'aquarium_size', 'reactor_placement', 'lighting_type', 'system_type', 'color',
    # 'max_head_height', 'duty_rating', 'warranty', 'alarms', 'number_of_leds', 'dimensions', 'weight'
]
