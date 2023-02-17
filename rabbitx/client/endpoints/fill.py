from rabbitx.client.endpoint_group import EndpointGroup


class FillGroup(EndpointGroup):

    def list(
        self,
        market_id: list[str] = None,
        start_time: int=None,
        end_time: int=None,
    ):
        data = dict(method='GET', path='/fills')
        self.session.sign_request(data)
        params = dict()

        if market_id:
            params['marketID'] = ','.join(market_id)

        if start_time:
            params['start_time'] = start_time
            
        if end_time:
            params['end_time'] = end_time
        
        resp = self.session.session.get(
            f'{self.session.api_url}/fills',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']

    def list_by_order(self, order_id:str):

        data = dict(method='GET', path='/fills/order')
        self.session.sign_request(data)
        params = dict(order_id=order_id)
        
        resp = self.session.session.get(
            f'{self.session.api_url}/fills/order',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']