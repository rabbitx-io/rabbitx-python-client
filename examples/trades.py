from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType
from rabbitx.client import OrderStatus
import os
from dotenv import load_dotenv

load_dotenv('.env')

if __name__ == '__main__':
    private_key = os.environ['PRIVATE_KEY'] # change this to your private key
    symbol = 'BTC-USD'
    testnet=False # change this to False if using on mainnet
    if testnet:
        client = Client(api_url=const.TESTNET_URL, private_key=private_key) 
    else:
        client = Client(api_url=const.URL, private_key=private_key)

    trades = client.trades.list(market_id="BTC-USD", p_limit=10)
    print(trades)