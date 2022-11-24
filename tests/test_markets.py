import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod
import pytest
from datetime import datetime

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.DEV_URL, private_key=private_key)
    

def test_market():
    markets = client.markets.list()
    assert len(markets) > 0

@pytest.mark.skip(reason='not implemented')
def test_single_market():
    markets = client.markets.list(['BTC-USD'])
    assert len(markets) == 1
    
def test_candles():
    now = int(datetime.now().timestamp())
    resp = client.onboarding.onboarding()
    candles = client.candles.list(market_id='BTC-USD', timestamp_from=1, timestamp_to=now, period=CandlePeriod.M15)
    assert len(candles)> 0
