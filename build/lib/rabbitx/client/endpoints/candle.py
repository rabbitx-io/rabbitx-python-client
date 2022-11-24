import enum

from rabbitx.client.endpoint_group import EndpointGroup


class CandlePeriod(enum.Enum):

    M1 = '1'
    M5 = '5'
    M15 = '15'
    M30 = '30'
    M60 = '60'
    M240 = '240'
    M1440 = '1440'


class CandleGroup(EndpointGroup):

    def list(
        self,
        market_id: str,
        timestamp_from: int,
        timestamp_to: int,
        period: CandlePeriod = CandlePeriod.M1,
    ):
        data = dict(method='GET', path='/candles')
        self.session.sign_request(data)
        params = dict(
            market_id=market_id,
            timestamp_from=timestamp_from,
            timestamp_to=timestamp_to,
            period=period.value,
        )

        resp = self.session.session.get(
            f'{self.session.api_url}/candles',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
