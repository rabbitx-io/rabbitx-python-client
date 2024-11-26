from rabbitx.client.endpoint_group import EndpointGroup


class PositionGroup(EndpointGroup):

    def list(self):
        data = dict(method='GET', path='/positions')
        self.session.sign_request(data)

        resp = self.session.session.get(
            f'{self.session.api_url}/positions',
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)

        return resp['result']