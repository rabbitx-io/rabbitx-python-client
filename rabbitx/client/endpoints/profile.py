from datetime import datetime
from rabbitx.client.endpoint_group import EndpointGroup

class ProfileGroup(EndpointGroup):
    def get(self):
        data = dict(method='GET', path='/profile')
        self.session.sign_request(data)

        resp = self.session.session.get(
            f'{self.session.api_url}/profile',
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result'][0]