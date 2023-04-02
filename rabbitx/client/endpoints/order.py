import enum

from rabbitx.client.endpoint_group import EndpointGroup


class OrderSide(enum.Enum):

    LONG = 'long'
    SHORT = 'short'


class OrderType(enum.Enum):

    MARKET = 'market'
    LIMIT = 'limit'


class OrderStatus(enum.Enum):

    PROCESSING = 'processing'
    OPEN = 'open'
    CLOSED = 'closed'
    REJECTED = 'rejected'
    CANCELED = 'canceled'
    CANCELING = 'canceling'
    AMENDING = 'amending'
    CANCELING_ALL = 'cancelingall'


class OrderGroup(EndpointGroup):

    def create(
        self,
        market_id: str,
        price: float,
        side: OrderSide,
        size: float,
        type_: OrderType,
    ):
        data = dict(
            market_id=market_id,
            price=price,
            side=side.value,
            size=size,
            type=type_.value,
            method='POST',
            path='/orders',
        )
        self.session.sign_request(data)
        resp = self.session.session.post(
            f'{self.session.api_url}/orders',
            json=data,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result'][0]

    def amend(
        self,
        order_id: int,
        market_id: str,
        price: float,
        size: float,
    ):
        data = dict(
            order_id=order_id,
            market_id=market_id,
            price=price,
            size=size,
            method='PUT',
            path='/orders',
        )
        self.session.sign_request(data)
        resp = self.session.session.put(
            f'{self.session.api_url}/orders',
            json=data,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result'][0]

    def cancel(self, order_id: int, market_id: str):
        data = dict(order_id=order_id, market_id=market_id, method='DELETE', path='/orders')
        self.session.sign_request(data)
        resp = self.session.session.delete(
            f'{self.session.api_url}/orders',
            json=data,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result'][0]

    def list(
        self,
        order_id: str=None,
        market_id: str=None,
        status: OrderStatus=None,
        start_time:int=None,
        end_time:int=None, 
    ):
        data = dict(method='GET', path='/orders')
        self.session.sign_request(data)
        params = dict()
        
        if order_id:
            params['order_id'] = order_id
        
        if market_id:
            params['market_id'] = market_id

        if status:
            params['status'] = status.value
        
        if start_time:
            params['start_time'] = start_time
        
        if end_time:
            params['end_time'] = end_time

        resp = self.session.session.get(
            f'{self.session.api_url}/orders',
            params=params,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']

    def cancel_all(self):
        data = dict(method='DELETE', path='/orders/cancel_all')
        self.session.sign_request(data)
        resp = self.session.session.delete(
            f'{self.session.api_url}/orders/cancel_all',
            json=data,
            headers=self.session.headers,
        ).json()

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
