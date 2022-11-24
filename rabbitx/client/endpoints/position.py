from rabbitx.client.endpoint_group import EndpointGroup


class PositionGroup(EndpointGroup):

    def list(self, market_id: list[str] = None):
        market_id = ','.join(market_id or [])
        data = dict(method='GET', path='/positions')
        self.session.sign_request(data)
        params = dict(marketID=market_id,)

        resp = self.session.session.get(
            f'{self.session.api_url}/positions',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
