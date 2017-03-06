from ryan_tools import *
import json
import requests
import time
import sqlite3
import base64
from requests.auth import HTTPBasicAuth
import easygui

base = 'https://ssapi.shipstation.com/'


def download_status_by_order_number( number, user, password ):
    
    global x
    x= requests.get( base + 'Orders?orderNumber=' + number , auth = HTTPBasicAuth(user, password) )
    status = x.status_code
    while status == 429 or status == 500:
        time.sleep( int(x.headers['X-Rate-Limit-Reset']) )
        x= requests.get( base + 'Orders?orderNumber=' + number , auth = HTTPBasicAuth(user, password) )
        status = x.status_code
    if status != 200:
        print(status)
        raise Exception('STATUS RETURNED BY ' + base + ' is ' + str(status))
    try:
        order = x.json()['orders'][0]['orderStatus']
    except IndexError:
        order = 'Not Found'
    return order



    
