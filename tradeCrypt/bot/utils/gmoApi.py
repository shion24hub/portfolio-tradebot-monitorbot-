import time
from datetime import datetime
import hmac
import hashlib
import requests
from requests.auth import HTTPDigestAuth
import json
import os
import numpy
import pandas
from pprint import pprint

import utils.config as config
import utils.p as p

API_KEY : str = config.API_KEY
SECRET_KEY : str = config.SECRET_KEY
ENDPOINT_PUBLIC : str = config.ENDPOINT_PUBLIC
ENDPOINT_PRIVATE : str = config.ENDPOINT_PRIVATE
LINE_USERNAME : str = p.username
LINE_PASSWORD : str = p.id_list[LINE_USERNAME]

def getStatus() -> str:

    path : str = "/v1/status"
    endpoint : str = ENDPOINT_PUBLIC + path

    res : str = requests.get(endpoint)

    return res

def getPrice(symbol : str) -> str :

    path : str = "/v1/ticker?symbol="
    endpoint : str = ENDPOINT_PUBLIC + path + symbol

    return json.dumps(requests.get(endpoint).json(), indent=2)

def gmoOrder(
    symbol : str,
    side : str,
    executionType : str,
    timeInForce : str,
    price : str,
    losscutPrice : str,
    size : str,
) -> None :

    path : str = "/v1/order"
    endpoint : str = ENDPOINT_PRIVATE + path

    timestamp : str = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
    method : str = "POST"
    reqBody : dict[str, str] = {
        "symbol": symbol,
        "side": side,
        "executionType": executionType,
        "timeInForce": timeInForce,
        "price": price,
        "losscutPrice": losscutPrice,
        "size": size
    }

    text : str = timestamp + method + path + json.dumps(reqBody)
    sign : str = hmac.new(bytes(SECRET_KEY.encode("ascii")), bytes(text.encode("ascii")), hashlib.sha256).hexdigest()

    headers : dict[str, str] = {
        "API-KEY": API_KEY,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }

    #gmoコインに対してのPOST
    order = requests.post(endpoint, headers=headers, data=json.dumps(reqBody))
    order_res = json.dumps(order.json(), indent=2)
    status = -1
    orderId = -1
    if order_res["status"] == 0 :
        status = 0
        orderId = order_res["data"]

    #監視システムに対してのPOST
    url = "url here."
    headers = {"Content-Type" : 'application/json'}
    data = {
        "status" : status,
        "symbol" : symbol,
        "side" : side,
        "executionType" : executionType,
        "timeInForce" : timeInForce,
        "price" : price,
        "losscutPrice" : losscutPrice,
        "size" : size,
    }
    requests.post(
        url=url, 
        auth=HTTPDigestAuth(LINE_USERNAME, LINE_PASSWORD),
        headers=headers,
        json=data,
    )

    #loggingとエラーハンドリングを追記。

def gmoCancel(orderId : int) :

    path : str = "/v1/cancelOrder"
    endpoint : str = ENDPOINT_PRIVATE + path

    timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
    method    = "POST"
    reqBody = {
        "orderId": orderId
    }

    text = timestamp + method + path + json.dumps(reqBody)
    sign = hmac.new(bytes(SECRET_KEY.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

    headers = {
        "API-KEY": API_KEY,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }

    res = requests.post(endpoint + path, headers=headers, data=json.dumps(reqBody))
    print (json.dumps(res.json(), indent=2))