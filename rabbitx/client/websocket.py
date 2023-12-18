import json

from websocket import WebSocketApp
import rel

from rabbitx.client import ClientSession


class WSClientCallback:

    def account_init(self, profile_id: int, data, ws: WebSocketApp):
        raise NotImplementedError

    def account_data(self, profile_id: int, data, ws: WebSocketApp):
        raise NotImplementedError

    def orderbook_init(self, market_id: str, data, ws: WebSocketApp):
        raise NotImplementedError

    def orderbook_data(self, market_id: str, data, ws: WebSocketApp):
        raise NotImplementedError

    def market_init(self, market_id: str, data, ws: WebSocketApp):
        raise NotImplementedError

    def market_data(self, market_id: str, data, ws: WebSocketApp):
        raise NotImplementedError

    def trade_init(self, market_id: str, data, ws: WebSocketApp):
        raise NotImplementedError

    def trade_data(self, market_id: str, data, ws: WebSocketApp):
        raise NotImplementedError


class WSClient:

    app: WebSocketApp
    session: ClientSession
    callback: WSClientCallback
    market_ids: list[str]

    def __init__(
        self,
        url: str,
        session: ClientSession,
        callback: WSClientCallback,
        market_ids: list[str] = None,
    ):
        self.session = session
        self.callback = callback
        self.market_ids = market_ids or []
        self._id_to_channel = {}
        self.app = WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def run(self):
        assert self.session.public_jwt

        self.app.run_forever(dispatcher=rel)
        rel.signal(2, rel.abort)
        rel.dispatch()

    def on_open(self, ws: WebSocketApp):
        channels = [f'account@{self.session.profile_id}']

        for market_id in self.market_ids:
            channels.append(f'orderbook:{market_id}')
            channels.append(f'trade:{market_id}')
            channels.append(f'market:{market_id}')

        channels = list(set(channels))
        data = dict(connect=dict(token=self.session.public_jwt, name='js'), id=1)
        ws.send(json.dumps(data))

        for idx, ch in enumerate(channels):
            data = dict(subscribe=dict(channel=ch, name='js'), id=idx + 1)
            self._id_to_channel[idx + 1] = ch
            ws.send(json.dumps(data))

    def on_message(self, ws: WebSocketApp, message: str):
        for line in message.split('\n'):
            try:
                data: dict = json.loads(line)
            except Exception as e:
                print(u'\u001b[31m ~~~ EXCEPTION ~~~')
                print(e)
                print(message, u'u\u001b[0m')
                return
            # ping
            if data == {}:
                ws.send(json.dumps({}))
                return

            # initial message
            if subscribe := data.get('subscribe', None):
                if data.get('id') == 1:
                    return

                channel = self._id_to_channel.get(data['id'])

                if not channel:
                    return

                initial_data = subscribe['data']

                if channel.startswith('account'):
                    *_, profile_id = channel.split('@')
                    self.callback.account_init(profile_id, initial_data, ws)

                if channel.startswith('orderbook'):
                    *_, market_id = channel.split(':')
                    self.callback.orderbook_init(market_id, initial_data, ws)

                if channel.startswith('market'):
                    *_, market_id = channel.split(':')
                    self.callback.market_init(market_id, initial_data, ws)

                if channel.startswith('trade'):
                    *_, market_id = channel.split(':')
                    self.callback.trade_init(market_id, initial_data, ws)

            if push := data.get('push', None):
                if 'epoch' in push and 'recoverable' in push:
                    return

                channel = push['channel']
                channel_data = push['pub']['data']

                if channel.startswith('account'):
                    *_, profile_id = channel.split('@')
                    self.callback.account_data(profile_id, channel_data, ws)

                if channel.startswith('orderbook'):
                    *_, market_id = channel.split(':')
                    self.callback.orderbook_data(market_id, channel_data, ws)

                if channel.startswith('market'):
                    *_, market_id = channel.split(':')
                    self.callback.market_data(market_id, channel_data, ws)

                if channel.startswith('trade'):
                    *_, market_id = channel.split(':')
                    self.callback.trade_data(market_id, channel_data, ws)

    def on_error(self, ws: WebSocketApp, error):
        raise error

    def on_close(self, ws: WebSocketApp, close_status_code: int, close_msg: str):
        ...
