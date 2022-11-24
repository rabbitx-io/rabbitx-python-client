from rabbitx.client.endpoint_group import EndpointGroup


class FillGroup(EndpointGroup):

    def list(
        self,
        timestamp_from: int,
        timestamp_to: int,
        offset: int = 0,
        limit: int = 100,
        market_id: list[str] = None,
        order_id: list[int] = None,
    ):
        data = dict(method='GET', path='/fills')
        self.session.sign_request(data)
        params = dict(offset=offset, limit=limit, timestampFrom=timestamp_from, timestampTo=timestamp_to)

        if market_id:
            params['marketID'] = ','.join(market_id)

        if order_id:
            params['orderID'] = ','.join(map(str, order_id))

        resp = self.session.session.get(
            f'{self.session.api_url}/fills',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
