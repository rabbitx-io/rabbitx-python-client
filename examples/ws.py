from websocket import WebSocketApp

from rabbitx import const
from rabbitx.client import Client, WSClient, WSClientCallback


class TestWebSocketCallback(WSClientCallback):

    def account_init(self, profile_id: int, data, ws: WebSocketApp):
        print('account_init', profile_id, data)

    def account_data(self, profile_id: int, data, ws: WebSocketApp):
        print('account_data', profile_id, data)

    def orderbook_init(self, market_id: str, data, ws: WebSocketApp):
        print('orderbook_init', market_id, data)

    def orderbook_data(self, market_id: str, data, ws: WebSocketApp):
        print('orderbook_data', market_id, data)

    def market_init(self, market_id: str, data, ws: WebSocketApp):
        print('market_init', market_id, data)

    def market_data(self, market_id: str, data, ws: WebSocketApp):
        print('market_data', market_id, data)

    def trade_init(self, market_id: str, data, ws: WebSocketApp):
        print('trade_init', market_id, data)

    def trade_data(self, market_id: str, data, ws: WebSocketApp):
        print('trade_data', market_id, data)


if __name__ == '__main__':
    private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
    client = Client(api_url=const.TESTNET_URL, private_key=private_key)
    client.onboarding.onboarding()

    wsc = WSClient(const.WS_TESTNET_URL, client, TestWebSocketCallback(), ['BTC-USD', 'ETH-USD', 'SOL-USD'])
    wsc.run()
