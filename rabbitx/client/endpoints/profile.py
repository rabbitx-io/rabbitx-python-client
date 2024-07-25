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

        print(resp)

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]