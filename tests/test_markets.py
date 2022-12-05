import os
import sys
sys.path.append(os.path.abspath('../'))

import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod
import pytest
from datetime import datetime

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.DEV_URL, private_key=private_key)
resp = client.onboarding.onboarding()


def test_market():
    markets = client.markets.list()
    assert len(markets) > 0

def test_single_market():
    symbol = 'BTC-USD'
    markets = client.markets.list([symbol])
    print(markets)
    assert len(markets) == 1
    assert markets[0]['id'] == symbol
    
def test_candles():
    now = int(datetime.now().timestamp())
    candles = client.candles.list(market_id='BTC-USD', timestamp_from=1, timestamp_to=now, period=CandlePeriod.M15)
    assert len(candles)> 0

def test_market_trades():
    symbol = 'BTC-USD'
    trades = client.trades.list(market_id=symbol, limit=100)
    assert len(trades) > 0
    assert trades[0]['market_id'] == symbol
    
def test_market_orderbook():
    symbol ='BTC-USD'
    orderbook = client.orderbook.get(symbol)
    assert len(orderbook) > 0
    assert orderbook[0]['market_id'] == symbol