import enum

from rabbitx.client.endpoint_group import EndpointGroup


class OrderSide(enum.Enum):

    LONG = 'long'
    SHORT = 'short'


class OrderType(enum.Enum):

    MARKET = 'market'
    LIMIT = 'limit'
    STOP_LOSS = 'stop_loss'
    TAKE_PROFIT = 'take_profit'
    STOP_LIMIT = 'stop_limit'
    STOP_MARKET = 'stop_market'


class OrderStatus(enum.Enum):

    PROCESSING = 'processing'
    PLACED = 'placed'
    OPEN = 'open'
    CLOSED = 'closed'
    REJECTED = 'rejected'
    CANCELED = 'canceled'
    CANCELING = 'canceling'
    AMENDING = 'amending'
    CANCELING_ALL = 'cancelingall'

class TimeInForce(enum.Enum):
    FOK = 'fill_or_kill'
    IOC = 'immediate_or_cancel'
    POSTONLY = 'post_only'
    GTC = 'good_till_cancel'
    

class OrderGroup(EndpointGroup):

    def create(
        self,
        market_id: str,
        price: float,
        side: OrderSide,
        size: float,
        type_: OrderType,
        client_order_id: str=None,
        time_in_force: TimeInForce=None,
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
        
        if client_order_id:
            data['client_order_id'] = client_order_id
        
        if time_in_force:
            data['time_in_force'] = time_in_force.value
        
        self.session.sign_request(data)
        resp = self.session.session.post(
            f'{self.session.api_url}/orders',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]

    def amend(
        self,
        order_id: int,
        market_id: str,
        price: float = None,
        size: float = None,
    ):
        data = dict(
            order_id=order_id,
            market_id=market_id,
            method='PUT',
            path='/orders',
        )
        
        if size:
            data['size'] = size
            
        if price:
            data['price'] = price
            
        self.session.sign_request(data)
        resp = self.session.session.put(
            f'{self.session.api_url}/orders',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]

    def cancel(self, 
               order_id: int, 
               market_id: str):
        data = dict(order_id=order_id, market_id=market_id, method='DELETE', path='/orders')
        self.session.sign_request(data)
        resp = self.session.session.delete(
            f'{self.session.api_url}/orders',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result'][0]

    def list(
        self,
        order_id: str=None,
        client_order_id: str=None,
        market_id: str=None,
        status: OrderStatus=None,
        start_time:int=None,
        end_time:int=None,
        p_limit: int=50,
        p_order: str="DESC",
        p_page: int=0
    ):
        data = dict(method='GET', path='/orders')
        self.session.sign_request(data)
        params = dict(p_limit=p_limit, p_order=p_order, p_page=p_page)
        
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
        
        if order_id:
            params['order_id'] = order_id
            
        if client_order_id:
            params['client_order_id'] = client_order_id

        resp = self.session.session.get(
            f'{self.session.api_url}/orders',
            params=params,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result']

    def cancel_all(self):
        data = dict(method='DELETE', path='/orders/cancel_all')
        self.session.sign_request(data)
        resp = self.session.session.delete(
            f'{self.session.api_url}/orders/cancel_all',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        return resp['result']