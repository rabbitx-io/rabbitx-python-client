from websocket import WebSocketApp
from rabbitx import const
from rabbitx.client import Client, WSClient, WSClientCallback
from pprint import pprint
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TestWebSocketCallback(WSClientCallback):

    def account_init(self, profile_id: int, data, ws: WebSocketApp):
        print('\n\n\naccount_init', profile_id)
        pprint(data)

    def account_data(self, profile_id: int, data, ws: WebSocketApp):
        print('\n\n\naccount_update', profile_id)
        pprint(data)

    def orderbook_init(self, market_id: str, data, ws: WebSocketApp):
        return
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
        return
        print('\n\n\ntrade_update', market_id)
        pprint(data)


if __name__ == '__main__':
    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    public_jwt = os.environ['PUBLIC_JWT']
    private_jwt = os.environ['PRIVATE_JWT']
    refresh_token = os.environ['REFRESH_TOKEN']
    private_key = os.environ['PRIVATE_KEY']
    
    testnet=False # change this to False if using on mainnet
    if testnet:
        client = Client(api_url=const.TESTNET_URL, api_key=api_key, api_secret=api_secret, jwt=private_jwt) 
    else:
        client = Client(api_url=const.URL, api_key=api_key, api_secret=api_secret, jwt=private_jwt, private_key=private_key)

    client.onboarding.onboarding()
    client.profile_id = 19

    if testnet:
        wsc = WSClient(const.WS_TESTNET_URL, client, TestWebSocketCallback(), ['BTC-USD', 'ETH-USD', 'SOL-USD'])
    else:
        wsc = WSClient(const.WS_URL, client, TestWebSocketCallback(), ['BTC-USD'])
    wsc.run()
