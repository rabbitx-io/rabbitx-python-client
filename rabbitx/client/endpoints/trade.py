from datetime import datetime

from rabbitx.client.endpoint_group import EndpointGroup


class TradeGroup(EndpointGroup):

    def list(
        self,
        market_id:str,
        **kwargs
    ):
        params = dict(market_id=market_id, **kwargs)

        resp = self.session.session.get(
            f'{self.session.api_url}/markets/trades',
            params=params,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)
        
        return resp['result']