from datetime import datetime
from rabbitx.client.endpoint_group import EndpointGroup

class OpsType(enum.Enum):

    DEPOSIT = 'deposit'
    FEE = 'fee'
    FUNDING = 'funding'
    PNL = 'pnl'
    WITHDRAWAL = 'withdrawal'

class BalanceGroup(EndpointGroup):
    def list(self, ops_type=None, start_time=None, end_time=None):
        data = dict(method='GET', path='/balanceops')
        self.session.sign_request(data)
        params = dict()

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

        if err := resp['error']:
            raise Exception(err)

        return resp['result']
