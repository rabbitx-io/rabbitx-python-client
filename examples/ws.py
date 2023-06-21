from websocket import WebSocketApp

from rabbitx import const
from rabbitx.client import Client, WSClient, WSClientCallback
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv('./.env')

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
        print('\n\n\norderbook_update', market_id)
        pprint(data)

    def market_init(self, market_id: str, data, ws: WebSocketApp):
        print('\n\n\nmarket_init', market_id)
        pprint(data)

    def market_data(self, market_id: str, data, ws: WebSocketApp):
        print('\n\n\nmarket_update', market_id)
        pprint(data)

    def trade_init(self, market_id: str, data, ws: WebSocketApp):
        print('\n\n\ntrade_init', market_id)
        pprint(data)

    def trade_data(self, market_id: str, data, ws: WebSocketApp):
        print('\n\n\ntrade_update', market_id)
        pprint(data)


if __name__ == '__main__':
    private_key = os.environ['PRIVATE_KEY'] # change this to your private key
    testnet=True # change this to False if using on mainnet
    if testnet:
        client = Client(api_url=const.TESTNET_URL, private_key=private_key) 
    else:
        client = Client(api_url=const.URL, private_key=private_key)
    client.onboarding.onboarding()

    if testnet:
        wsc = WSClient(const.WS_TESTNET_URL, client, TestWebSocketCallback(), ['BTC-USD', 'ETH-USD', 'SOL-USD'])
    else:
        wsc = WSClient(const.WS_URL, client, TestWebSocketCallback(), ['BTC-USD', 'ETH-USD', 'SOL-USD'])
    wsc.run()
