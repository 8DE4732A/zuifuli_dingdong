import requests
import winsound
import time
import json

#配置 cookies 和 uid 和 经纬度 
#订单默认使用获取的第一个地址
#cookies
cookies = {'DDXQSESSID': ''}
#uid
uid = ''
#longitude
longitude = ''
#latitude
latitude = ''


station_id = ''
address_id = ''



headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type': 'application/x-www-form-urlencoded',
    'ddmc-api-version': '9.25.1',
    'ddmc-app-client-id': '3',
    'ddmc-build-version': '2.40.0',
    'ddmc-channel': 'undefined',
    'ddmc-device-id': 'undefined',
    'ddmc-latitude': latitude,
    'ddmc-longitude': longitude,
    'ddmc-os-version': 'undefined',
    'ddmc-station-id': station_id,
    'ddmc-uid': uid,
    'Origin': 'https://zuifuli.m.ddxq.mobi',
    'Connection': 'keep-alive',
    'Referer': 'https://zuifuli.m.ddxq.mobi/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

def get_location():
    params = {
        'uid': uid,
        'longitude': longitude,
        'latitude': latitude,
        'station_id': station_id,
        'city_number': '0101',
        'api_version': '9.25.1',
        'app_version': '2.40.0',
        'applet_source': '',
        'app_client_id': '3',
        'h5_source': 'zuifuli',
        'sharer_uid': '',
        's_id': '',
        'openid': '',
        'source_type': '5',
    }
    r = requests.get('https://sunquan.api.ddxq.mobi/api/v1/user/address/', headers=headers, params=params, cookies=cookies)
    # print(r.json())
    return r.json()['data']['valid_address'][0]

def get_products():
    print("获取商品列表....")
    r = requests.get('https://maicai.api.ddxq.mobi/cart/index?uid=' + uid + '&longitude=' + longitude + '&latitude=' + latitude + '&station_id=' + station_id + '&city_number=&api_version=9.25.1&app_version=2.40.0&applet_source=&app_client_id=3&h5_source=zuifuli&sharer_uid=&s_id=&openid=&is_load=1&ab_config=%7B%22key_gift_size%22:true,%22key_onion%22:%22C%22%7D', headers=headers, cookies=cookies)
    for product in r.json()['data']['order_product_list']:
        print(product['product_name'])
    return r.json()['data']

def check_time(products):
    print("检查配送资源....")
    data = {
        'uid': uid,
        'longitude': longitude,
        'latitude': latitude,
        'station_id': station_id,
        'city_number': '0101',
        'api_version': '9.25.1',
        'app_version': '2.40.0',
        'applet_source': '',
        'app_client_id': '3',
        'h5_source': 'zuifuli',
        'sharer_uid': '',
        's_id': '',
        'openid': '',
        'address_id': address_id,
        'products': json.dumps(products,ensure_ascii=False),
    }
    r = requests.post('https://maicai.api.ddxq.mobi/order/getReserveTime', headers=headers, cookies=cookies, data=data)
    # print(r.json())
    return r.json()

def check_order(products: list):
    print("检查订单....")
    product_param = []
    for product in products:
        product_param.append({
            "id": product['id'],
            "category_path": product['category_path'],
            "count": product['count'],
            "price": product['price'],
            "total_money": product['total_price'],
            "instant_rebate_money":"0.00",
            "activity_id":"",
            "conditions_num":"",
            "product_type":0,
            "sizes":[],
            "type": product['type'],
            "total_origin_money": product['total_origin_price'],
            "price_type":0,
            "batch_type":-1
        })
    data = {
        'uid': '',
        'longitude': longitude,
        'latitude': latitude,
        'station_id': station_id,
        'city_number': '0101',
        'api_version': '9.25.1',
        'app_version': '2.40.0',
        'applet_source': '',
        'app_client_id': '3',
        'h5_source': 'zuifuli',
        'sharer_uid': '',
        's_id': '',
        'openid': '',
        'address_id': address_id,
        'user_ticket_id': 'default',
        'is_use_point': '0',
        'is_use_balance': '0',
        'is_buy_vip': '0',
        'products': json.dumps(product_param, ensure_ascii=False),
        'check_order_type': '0',
        'showData': 'true',
    }
    # print("data", data)
    r = requests.post('https://maicai.api.ddxq.mobi/order/checkOrder', headers=headers, cookies=cookies, data=data)
    # print(r.json())
    return r.json()

def add_order(order, products, newProducts, haveTimes):
    print("添加订单....")
    print('order', order)
    param_order = {
        "reserved_time_start": haveTimes[0]['start_timestamp'],
        "reserved_time_end": haveTimes[0]['end_timestamp'],
        "price":order['total_money'],
        "freight_discount_money":order['freight_discount_money'],
        "freight_money":order['freight_money'],
        "note":"",
        "product_type":1,
        "order_product_list_sign":newProducts["sign"],
        "address_id":address_id,
        "pay_type":16,
        "products": products,
        "vip_money":"",
        "vip_buy_user_ticket_id":"",
    }
    data = {
        'uid': uid,
        'longitude': longitude,
        'latitude': latitude,
        'station_id': station_id,
        'city_number': '',
        'api_version': '9.25.1',
        'app_version': '2.40.0',
        'applet_source': '',
        'app_client_id': '3',
        'h5_source': 'zuifuli',
        'sharer_uid': '',
        's_id': '',
        'openid': '',
        'order': json.dumps(param_order),
        'soon_arrival': '0',
        'showMsg': 'true',
        'ab_config': '{"key_gift_size":true,"key_onion":"C"}',
        'eta_trace_id': '',
    }
    print('add order param', data)
    r = requests.post('https://maicai.api.ddxq.mobi/order/addNewOrder', headers=headers, cookies=cookies, data=data)
    print('add order result', r.json())

if __name__ == '__main__':
    address = get_location()
    print(address)
    station_id = address['station_id'] 
    address_id = address['id'] 

    products = get_products()
    # print(json.dumps(products, indent=4, ensure_ascii=False))
    loop = 0
    while True:
        loop += 1
        try:
            if loop % 20 == 0:
                products = get_products()
            result = check_time(products['order_product_list'])
            if result['success']:
                have_times = [one for one in result['data']['time'][0]['times'] if one['textMsg'] != '已约满']
                if have_times:
                    print("有配送資源了.....", have_times)
                    winsound.Beep(600, 1000)
                    check_result = check_order(products['new_order_product_list'][0]['products'])
                    # 下订单
                    add_result = add_order(check_result['data']['order'], products['order_product_list'], products['new_order_product_list'][0], have_times)
                    if add_result['code'] == 0:
                        print('下单成功.............')
                        break
                    else:
                        products = get_products(address)
        except Exception as e:
            print(e)
            products = get_products(address)
        time.sleep(1)
    
