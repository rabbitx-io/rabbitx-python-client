from rabbitx.client.endpoint_group import EndpointGroup


class JWTGroup(EndpointGroup):

    def update(self, jwt_token=''):
        data = dict(
            refresh_token=jwt_token,
            is_client=False,
            method='POST',
            path='/jwt',
        )
        self.session.sign_request(data)
        resp = self.session.session.post(
            f'{self.session.api_url}/jwt',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)

        self.session.private_jwt = resp['result'][0]['jwt']

        return resp['result'][0]['jwt']
