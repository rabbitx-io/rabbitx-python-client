from datetime import datetime

from rabbitx.client.endpoint_group import EndpointGroup


class TradeGroup(EndpointGroup):

    def list(
        self,
        market_id: str,
        limit:int = 100
    ):
        params = dict(market_id=market_id)

        params['limit'] = limit

        resp = self.session.session.get(
            f'{self.session.api_url}/markets/trades',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
