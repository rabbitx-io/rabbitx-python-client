from websocket import WebSocketApp
from rabbitx import const
from rabbitx.client import Client, WSClient, WSClientCallback
from pprint import pprint
import os
from dotenv import load_dotenv
import argparse

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TestWebSocketCallback(WSClientCallback):

    def account_init(self, profile_id: int, data, ws: WebSocketApp):
        print('\n\n\naccount_init', profile_id)
        pprint(data)

    def account_data(self, profile_id: int, data, ws: WebSocketApp):
        print('\n\n\naccount_update', profile_id)
        pprint(data)

    def orderbook_init(self, market_id: str, data, ws: WebSocketApp):
        print('\n\n\norderbook_init', market_id)
        pprint(data)

    def orderbook_data(self, market_id: str, data, ws: WebSocketApp):
        return
        print('\n\n\norderbook_update', market_id)
        pprint(data)

    def market_init(self, market_id: str, data, ws: WebSocketApp):
        return
        print('\n\n\nmarket_init', market_id)
        pprint(data)

    def market_data(self, market_id: str, data, ws: WebSocketApp):
        return
        print('\n\n\nmarket_update', market_id)
        pprint(data)

    def trade_init(self, market_id: str, data, ws: WebSocketApp):
        return
        print('\n\n\ntrade_init', market_id)
        pprint(data)

    def trade_data(self, market_id: str, data, ws: WebSocketApp):
        print('\n\n\ntrade_update', market_id)
        pprint(data)


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

    if testnet:
        wsc = WSClient(const.WS_TESTNET_URL, client, TestWebSocketCallback(), ['BTC-USD', 'ETH-USD', 'SOL-USD'])
    else:
        wsc = WSClient(const.WS_URL, client, TestWebSocketCallback(), ['BTC-USD'])
    wsc.run()
