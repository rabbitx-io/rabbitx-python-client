from datetime import datetime

from rabbitx.client.endpoint_group import EndpointGroup


class TradeGroup(EndpointGroup):

    def list(
        self,
        market_id: str,
        timestamp_from: int = None,
        timestamp_to: int = None,
    ):
        params = dict(marketID=market_id)

        if not all([timestamp_from, timestamp_to]):
            timestamp_from = int(datetime.utcnow().timestamp()) - 3600 * 24
            timestamp_to = int(datetime.utcnow().timestamp())

        params['timestampFrom'] = timestamp_from
        params['timestampTo'] = timestamp_to

        resp = self.session.session.get(
            f'{self.session.api_url}/trades',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
