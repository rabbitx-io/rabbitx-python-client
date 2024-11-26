from rabbitx.client.endpoint_group import EndpointGroup


class MarketGroup(EndpointGroup):

    def list(self, market_id: list[str] = None):
        params = dict()

        if market_id:
            params['market_id'] = ','.join(market_id)

        resp = self.session.session.get(
            f'{self.session.api_url}/markets',
            params=params,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)

        return resp['result']