from datetime import datetime
import enum
from rabbitx.client.endpoint_group import EndpointGroup

class OpsType(enum.Enum):

    DEPOSIT = 'deposit'
    FEE = 'fee'
    FUNDING = 'funding'
    PNL = 'pnl'
    WITHDRAWAL = 'withdrawal'

class BalanceGroup(EndpointGroup):
    def list(
        self,
        ops_type=None,
        start_time=None,
        end_time=None,
        p_limit: int=50,
        p_order: str="DESC",
        p_page: int=0
    ):
        data = dict(method='GET', path='/balanceops')
        self.session.sign_request(data)
        params = dict(p_limit=p_limit, p_order=p_order, p_page=p_page)

        if ops_type:
            params['ops_type'] = ops_type
        
        if start_time:
            params['start_time'] = start_time
            
        if end_time:
            params['end_time'] = end_time
        
        resp = self.session.session.get(
            f'{self.session.api_url}/balanceops',
            params=params,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp)

        return resp['result']