import os
import sys
sys.path.append(os.path.abspath('../'))

import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType, OrderStatus
import pytest
from datetime import datetime
from pprint import pprint

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.TESTNET_URL, private_key=private_key)
client.onboarding.onboarding()
market_symbol = 'BTC-USD'

def test_order_create():
    result = client.orders.create(market_id=market_symbol, price=10000, side=OrderSide.LONG, size=1, type_=OrderType.LIMIT)
    assert result['status'] == 'processing'
    
    result = client.orders.create(market_id=market_symbol, price=10, side=OrderSide.LONG, size=1, type_=OrderType.MARKET)
    assert result['status'] == 'processing'
    
def test_order_cancel():
    result = client.orders.create(market_id=market_symbol, price=10000, side=OrderSide.LONG, size=1, type_=OrderType.LIMIT)
    ord_id = result['id']
    result = client.orders.cancel(order_id=ord_id, market_id=market_symbol)
    
    assert result['status'] == 'canceling'
    
def test_order_amend():
    result = client.orders.create(market_id=market_symbol, price=10000, side=OrderSide.LONG, size=1, type_=OrderType.LIMIT)
    ord_id = result['id']
    result = client.orders.amend(order_id=ord_id, market_id=market_symbol, price=10001, size=3)
    
    pprint(result)
    assert result['status'] == 'amending'
    assert result['size'] == '3'
    assert result['price'] == '10001'

def test_order_list():
    now = int(datetime.now().timestamp())
    result = client.orders.list(market_id='BTC-USD')
    result = client.orders.list(status=OrderStatus.OPEN)
    result = client.orders.list(market_id='BTC-USD', start_time=now-1000, end_time=now)
    pprint(result)
    
def test_order_cancel_all():
    result = client.orders.cancel_all()
    pprint(result)