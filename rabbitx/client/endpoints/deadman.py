import enum

from rabbitx.client.endpoint_group import EndpointGroup
    

class DeadmanGroup(EndpointGroup):

    def create(
        self,
        timeout: int,
    ):
        data = dict(
            timeout=timeout,
            method='POST',
            path='/cancel_all_after',
        )
       
        self.session.sign_request(data)
        resp = self.session.session.post(
            f'{self.session.api_url}/cancel_all_after',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]

    def remove(self):
        data = dict(
            method='DELETE',
            path='/cancel_all_after',
        )
            
        self.session.sign_request(data)
        resp = self.session.session.delete(
            f'{self.session.api_url}/cancel_all_after',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]

    def get(self):
        data = dict(method='GET', path='/cancel_all_after')
        self.session.sign_request(data)

        resp = self.session.session.get(
            f'{self.session.api_url}/cancel_all_after',
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result']
