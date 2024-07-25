from rabbitx.client.endpoint_group import EndpointGroup


class OrderBookGroup(EndpointGroup):

    def get(self, market_id: str):
        data = dict(method='GET', path='markets/orderbook')
        params = dict(market_id=market_id)

        resp = self.session.session.get(
            f'{self.session.api_url}/markets/orderbook',
            params=params,
            headers=self.session.headers,
        ).json()

        if 'error' in resp:
            raise Exception(resp['error'])

        return resp['result']
