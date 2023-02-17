import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod
import pytest
from datetime import datetime

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.TESTNET_URL, private_key=private_key)
    
def test_onboarding():
    result = client.onboarding.onboarding()
    assert result['profile']['profile_type'] == 'trader'
    assert result['profile']['status'] == 'active'