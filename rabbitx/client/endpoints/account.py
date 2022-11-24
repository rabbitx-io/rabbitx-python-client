from rabbitx.client.endpoint_group import EndpointGroup


class AccountGroup(EndpointGroup):

    def get(self):
        data = dict(method='GET', path='/account')
        self.session.sign_request(data)

        resp = self.session.session.get(
            f'{self.session.api_url}/account',
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']

    def validate(self, jwt: str) -> bool:
        data = dict(method='GET', path='/account/validate')
        self.session.sign_request(data)
        params = dict(jwt=jwt)

        resp = self.session.session.get(
            f'{self.session.api_url}/account/validate',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['success']

    def set_leverage(self, market_id: str, leverage: float):
        data = dict(
            marketID=market_id,
            leverage=leverage,
            method='POST',
            path='/account/leverage',
        )
        self.session.sign_request(data)
        resp = self.session.session.post(
            f'{self.session.api_url}/account/leverage',
            json=data,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result'][0]
