import concurrent.futures
import json
import threading
import time
from random import random

import requests

#配置 cookies 和 uid 和 经纬度 
#默认使用第一个地址
#cookies
cookies = {'DDXQSESSID': ''}
#uid
uid = ''
#longitude
longitude = ''
#latitude
latitude = ''

BARK_ID = ''


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
    # print(threading.current_thread().name, r.json())
    return r.json()['data']['valid_address'][0]

def get_products():
    print(threading.current_thread().name, "获取商品列表....")
    r = requests.get('https://maicai.api.ddxq.mobi/cart/index?uid=' + uid + '&longitude=' + longitude + '&latitude=' + latitude + '&station_id=' + station_id + '&city_number=&api_version=9.25.1&app_version=2.40.0&applet_source=&app_client_id=3&h5_source=zuifuli&sharer_uid=&s_id=&openid=&is_load=1&ab_config=%7B%22key_gift_size%22:true,%22key_onion%22:%22C%22%7D', headers=headers, cookies=cookies)
    if not r.json()['success']:
        print(threading.current_thread().name, 'products', r.json())
    for product in r.json()['data']['order_product_list']:
        print(threading.current_thread().name, product['product_name'])
    return r.json()['data']

success_count = 0
fail_count = 0
def check_time(products):
    print(threading.current_thread().name, threading.current_thread().name, "检查配送资源....")
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
    if r.json()['success']:
        return [one for one in r.json()['data']['time'][0]['times'] if one['textMsg'] != '已约满']
    else:
        print(r.text)
        return []

def check_time_multi(products):
    print(threading.current_thread().name, "检查配送资源....")
    products_param = []
    for product in products:
        products_param.append({
            "count": product['count'],
            "id": product["id"],
            "instant_rebate_money": product["instant_rebate_money"],
            "origin_price": product["origin_price"],
            "price": product["price"],
            "total_money": product["total_price"],
            "total_origin_money": product["total_origin_price"]
        })

    headers = {
        'Host': 'maicai.api.ddxq.mobi',
        'Connection': 'keep-alive',
        'content-type': 'application/x-www-form-urlencoded',
        'ddmc-city-number': '0101',
        'ddmc-build-version': '2.82.0',
        'ddmc-station-id': station_id,
        'ddmc-channel': 'applet',
        'ddmc-os-version': '[object Undefined]',
        'ddmc-app-client-id': '4',
        'ddmc-longitude': longitude,
        'ddmc-latitude': latitude,
        'ddmc-api-version': '9.49.2',
        'ddmc-uid': uid,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123c) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx1e113254eda17715/422/page-frame.html',
    }

    data = {
        'uid': uid,
        'longitude': longitude,
        'latitude': latitude,
        'station_id': station_id,
        'city_number': '0101',
        "app_clinet_id": "4",
        "channel": "applet",
        'api_version': '9.49.2',
        'app_version': '2.82.0',
        'applet_source': '',
        'app_client_id': '3',
        'h5_source': '',
        'sharer_uid': '',
        'isBridge': 'false',
        's_id': '',
        'openid': '',
        'device_token': '',
        'group_config_id': '',
        'address_id': address_id,
        'products': json.dumps([products_param,], ensure_ascii=False),
        'nars': '',
        'sesi': ''
    }
    r = requests.post('https://maicai.api.ddxq.mobi/order/getMultiReserveTime', headers=headers, cookies=cookies, data=data)
    if r.json()['success']:
        print(r.json())
        print([one for one in r.json()['data'][0]['time'][0]['times'] if one['textMsg'] != '已约满' and one['select_msg'] != '自动尝试可用时段'])
        return [one for one in r.json()['data'][0]['time'][0]['times'] if one['textMsg'] != '已约满' and one['select_msg'] != '自动尝试可用时段']
    else:
        print(r.text)


def check_order(products: list):
    print(threading.current_thread().name, "检查订单....")
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
    # print(threading.current_thread().name, "data", data)
    r = requests.post('https://maicai.api.ddxq.mobi/order/checkOrder', headers=headers, cookies=cookies, data=data)
    print(threading.current_thread().name, r.json())
    return r.json()

def add_order(order, products, newProducts, haveTimes):
    print(threading.current_thread().name, "添加订单....")
    # print(threading.current_thread().name, 'order', order)

    # if len(haveTimes) > 1:
    #     haveTimes[0] = haveTimes[len(haveTimes) - 1]
    
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
        # "pay_type": 2,
        "products": products,
        "vip_money":"",
        "vip_buy_user_ticket_id":"",
    }
    print("价格", order['total_money'])
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
    # print(threading.current_thread().name, 'add order param', data)
    r = requests.post('https://maicai.api.ddxq.mobi/order/addNewOrder', headers=headers, cookies=cookies, data=data)
    print(threading.current_thread().name, 'add order result', r.json())
    return r.json()

finished = False

def main(s):
    if s:
        time.sleep(s * 0.4)
    address = get_location()
    print(threading.current_thread().name, address)
    global station_id
    station_id = address['station_id'] 
    global address_id
    address_id = address['id'] 

    products = {}
    # print(threading.current_thread().name, json.dumps(products, indent=4, ensure_ascii=False))
    loop = -1
    global finished
    while not finished:
        loop += 1
        try:
            if loop % 50 == 0:
                products = get_products()
            have_times = check_time_multi(products['order_product_list'])
            print(threading.current_thread().name, "检查时间结果", have_times)
            if have_times:
                print(threading.current_thread().name, "有配送資源了", have_times)
                print(threading.current_thread().name, '已有配送资源......')
                check_result = check_order(products['new_order_product_list'][0]['products'])
                # 下订单
                add_result = add_order(check_result['data']['order'], products['order_product_list'], products['new_order_product_list'][0], have_times)
                if add_result['code'] == 0:
                    print(threading.current_thread().name, '下单成功.............')
                    finished = True
                    for _ in range(20):
                        if BARK_ID != '':
                            requests.get('https://api.day.app/%s/%s'% (BARK_ID, '下单成功'))
                            requests.get('https://api.day.app/%s/推送铃声?sound=minuet'%BARK_ID)
                        time.sleep(1)
                    break
                else:
                    products = get_products()
            else:
                have_times = [{"start_timestamp": 1680123600, 'end_timestamp': 1680188400}]
                #自动时间段
                if loop % 100000 == 0:
                    print("自动时间处理", have_times)
                    check_result = check_order(products['new_order_product_list'][0]['products'])
                    # 下订单
                    add_result = add_order(check_result['data']['order'], products['order_product_list'], products['new_order_product_list'][0], have_times)
                    if add_result['code'] == 0:
                        print(threading.current_thread().name, '下单成功.............')
                        finished = True
                        for _ in range(20):
                            if BARK_ID != '':
                                requests.get('https://api.day.app/%s/%s'% (BARK_ID, '下单成功'))
                                requests.get('https://api.day.app/%s/推送铃声?sound=minuet'%BARK_ID)
                            time.sleep(1)
                        break
                    else:
                        products = get_products()

        except Exception as e:
            print(threading.current_thread().name, '异常', e)
            try:
                products = get_products()
            except Exception as ex:
                print(threading.current_thread().name, ex)
        print('loop', loop)
        time.sleep(1)


if __name__ == '__main__':
    workers = 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_url = {executor.submit(main, index): index for index in range(workers)}
        done, not_done = concurrent.futures.wait(future_to_url.keys(), timeout=0)
        try:
            while not_done:
                freshly_done, not_done = concurrent.futures.wait(not_done, timeout=1)
                done |= freshly_done
        except KeyboardInterrupt:
            finished = True
            _ = concurrent.futures.wait(not_done, timeout=None)
