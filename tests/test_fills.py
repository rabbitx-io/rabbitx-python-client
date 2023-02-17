import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod
import pytest
from datetime import datetime

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.TESTNET_URL, private_key=private_key)
resp = client.onboarding.onboarding()
    
def test_fills():
    now = int(datetime.now().timestamp())
    fills = client.fills.list()
    fills = client.fills.list(market_id='BTC-USD')
    fills = client.fills.list(start_time=now-100)
    fills = client.fills.list(start_time=now-100, end_time=now)