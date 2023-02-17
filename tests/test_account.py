import os
import sys
sys.path.append(os.path.abspath('../'))

import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod
import pytest
from datetime import datetime

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.TESTNET_URL, private_key=private_key)
resp = client.onboarding.onboarding()

def test_account():
    result = client.account.get()
    assert len(result) > 0
    assert result['status'] == 'active'
    
def test_set_leverage():
    result = client.account.set_leverage(market_id="BTC-USD", leverage=20)
    assert result['leverage']['BTC-USD']=='20'
    
if __name__ =='__main__':
    test_account()
    test_set_leverage()
