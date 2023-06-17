from websocket import WebSocketApp

from rabbitx import const
from rabbitx.client import Client, WSClient, WSClientCallback
from pprint import pprint

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
    private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
    client = Client(api_url=const.TESTNET_URL, private_key=private_key)
    client.onboarding.onboarding()

    wsc = WSClient(const.WS_TESTNET_URL, client, TestWebSocketCallback(), ['BTC-USD', 'ETH-USD', 'SOL-USD'])
    wsc.run()
