from rabbitx.client.endpoint_group import EndpointGroup


class AccountGroup(EndpointGroup):

    def get(self):
        data = dict(method='GET', path='/account')
        self.session.sign_request(data)

        resp = self.session.session.get(
            f'{self.session.api_url}/account',
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]

    def validate(self, jwt: str) -> bool:
        data = dict(method='GET', path='/account/validate')
        self.session.sign_request(data)
        params = dict(jwt=jwt)

        resp = self.session.session.get(
            f'{self.session.api_url}/account/validate',
            params=params,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['success']

    def set_leverage(self, market_id: str, leverage: int):
        """_summary_

        Args:
            market_id (str): market id
            leverage (int): Must be one of integer from 1-20

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        data = dict(
            market_id=market_id,
            leverage=leverage,
            method='PUT',
            path='/account/leverage',
        )
        self.session.sign_request(data)
        resp = self.session.session.put(
            f'{self.session.api_url}/account/leverage',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]