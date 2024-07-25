from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType
from rabbitx.client import OrderStatus
import os
from dotenv import load_dotenv
import argparse

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':

    # Set up argument parser
    parser = argparse.ArgumentParser(description='RabbitX API example')
    parser.add_argument('--testnet', action='store_true', help='Use testnet instead of mainnet')
    parser.add_argument('--exchange', type=str, default='rbx', choices=['rbx', 'bfx'], help='Choose the exchange: rbx (RabbitX) or bfx (Bitfinex)')
    args = parser.parse_args()

    # Use the parsed argument to set testnet
    testnet = args.testnet
    exchange = args.exchange

    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    public_jwt = os.environ['PUBLIC_JWT']
    private_jwt = os.environ['PRIVATE_JWT']

    symbol = 'BTC-USD'
    
    if exchange == 'rbx':
        # Set up client
        if testnet:
            client = Client(api_url=const.TESTNET_URL, api_key=api_key, api_secret=api_secret,public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange) 
        else:
            client = Client(api_url=const.URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
    elif exchange == 'bfx':
        if testnet:
            client = Client(api_url=const.TESTNET_BFX_URL, api_key=api_key, api_secret=api_secret,public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
        else:
            client = Client(api_url=const.BFX_URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)

    client.onboarding.init()

    trades = client.trades.list(market_id="BTC-USD", p_limit=10)
    print(trades)