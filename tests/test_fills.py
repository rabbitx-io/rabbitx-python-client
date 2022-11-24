import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod
import pytest
from datetime import datetime

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.DEV_URL, private_key=private_key)
resp = client.onboarding.onboarding()
    
@pytest.mark.skip(reason='not implemented')
def test_fills():
    now = int(datetime.now().timestamp())
    fills = client.fills.list(market_id='BTC-USD', limit=100, offset=0)
