import enum

from rabbitx.client.endpoint_group import EndpointGroup

class DeadmanGroup(EndpointGroup):
    def create(
        self,
        timeout: int,
        market_id: str,
    ):
        params = {
            "timeout": timeout,
            "market_id": market_id,
        }
        data = {
            "method": "POST",
            "path": "/cancel_all_after",
        }
       
        self.session.sign_request(data)
        resp = self.session.session.post(
            f'{self.session.api_url}/cancel_all_after',
            params=params,
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)

        return resp['result'][0]
    
    def remove(self, market_id: str):
        params = {
            "market_id": market_id
        }
        data = dict(
            method='DELETE',
            path='/cancel_all_after',
        )
            
        self.session.sign_request(data)
        resp = self.session.session.delete(
            f'{self.session.api_url}/cancel_all_after',
            params=params,
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)

        return resp['result'][0]
    
    def get(self, market_id: str):
        params = {
            "market_id": market_id
        }

        resp = self.session.session.get(
            f'{self.session.api_url}/cancel_all_after',
            params=params,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)

        return resp['result'][0]
