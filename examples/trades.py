from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType
from rabbitx.client import OrderStatus
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    public_jwt = os.environ['PUBLIC_JWT']
    private_jwt = os.environ['PRIVATE_JWT']
    refresh_token = os.environ['REFRESH_TOKEN']
    symbol = 'BTC-USD'
    testnet=False # change this to True if using on testnet
    if testnet:
        client = Client(api_url=const.TESTNET_URL, api_key=api_key, api_secret=api_secret,jwt=public_jwt) 
    else:
        client = Client(api_url=const.URL, api_key=api_key, api_secret=api_secret, jwt=public_jwt)

    client.onboarding.init()

    trades = client.trades.list(market_id="BTC-USD", p_limit=10)
    print(trades)