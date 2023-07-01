from datetime import datetime

from rabbitx.client.endpoint_group import EndpointGroup


class TradeGroup(EndpointGroup):

    def list(
        self,
        market_id:str,
        start_time:int=None,
        end_time:int=None,
        p_limit: int=50,
        p_order: str="DESC",
        p_page: int=0
        **kwargs
    ):
        params = dict(p_limit=p_limit, p_order=p_order, p_page=p_page, **kwargs)

        if start_time:
            params['start_time'] = start_time

        if end_time:
            params['end_time'] = end_time

        resp = self.session.session.get(
            f'{self.session.api_url}/markets/trades',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)
        
        return resp
