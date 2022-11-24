import rabbitx
from rabbitx import const
from rabbitx.client import Client, CandlePeriod
import pytest
from datetime import datetime

private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
client = Client(api_url=const.DEV_URL, private_key=private_key)
resp = client.onboarding.onboarding()

def test_account():
    result = client.account.get()
    assert len(result) > 0
    assert result[0]['status'] == 'active'