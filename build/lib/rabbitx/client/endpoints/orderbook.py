from rabbitx.client.endpoint_group import EndpointGroup


class OrderBookGroup(EndpointGroup):

    def get(self, market_id: str, depth: int = 10):
        data = dict(method='GET', path='/orderbook')
        params = dict(marketID=market_id, depth=depth)

        resp = self.session.session.get(
            f'{self.session.api_url}/orderbook',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
