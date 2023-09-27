from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType, TimeInForce
from rabbitx.client import OrderStatus
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    public_jwt = os.environ['PUBLIC_JWT']
    private_jwt = os.environ['PRIVATE_JWT']
                         
    symbol = 'BTC-USD'
    testnet=False # change this to True if using on testnet
    if testnet:
        client = Client(api_url=const.TESTNET_URL, api_key=api_key, api_secret=api_secret,jwt=public_jwt) 
    else:
        client = Client(api_url=const.URL, api_key=api_key, api_secret=api_secret, jwt=public_jwt)

    client.onboarding.init()

    resp = client.markets.list([symbol])
    market = resp[0]
    print(f'\033[92m\n\n\n{symbol} market info:\n\033[0m', market)

    orderbook = client.orderbook.get('BTC-USD')[0]
    print(f'\033[92m\n\n\n{symbol} orderbook:\n\033[0m', orderbook)
    
    new_jwt = client.jwt.update(client._jwt)
    print('\033[92m\n\n\nnew jwt:\n\033[0m', new_jwt)
    
    order_1 = client.orders.create(
        'BTC-USD',
        1,
        OrderSide.LONG,
        0.002,
        OrderType.LIMIT,
    )
    print('\033[92m\n\n\norder creation:\n\033[0m', order_1)
    
    orders = client.orders.list(status=OrderStatus.OPEN)
    print('\033[92m\n\n\nopen order list:\n\033[0m', orders)
    
    positions = client.positions.list()
    print('\033[92m\n\n\nopen positions list:\n\033[0m', positions)

    fills = client.fills.list()
    print('\033[92m\n\n\nfills:\n\033[0m', fills)

    account = client.account.get()
    print('\033[92m\n\n\naccount:\n\033[0m', account)
    
    profile = client.profile.get()
    print('\033[92m\n\n\nprofile:\n\033[0m', profile)
    
    balance_history = client.balance.list(p_limit=100)
    print('\033[92m\n\n\nbalance history:\n\033[0m', balance_history)
    
    funding_payments = client.balance.list(ops_type='funding', p_limit=100)
    print('\033[92m\n\n\nfunding payments:\n\033[0m', funding_payments)
    
    # check jwt is valid or not (for stage env)
    client.account.validate(client._jwt)

    new_leverage = client.account.set_leverage('BTC-USD', 20)
    print('\033[92m\n\n\nnew leverage:\n\033[0m', new_leverage)

    candles = client.candles.list(
        'BTC-USD',
        client.current_timestamp - 10,
        client.current_timestamp + 10,
        CandlePeriod.M1,
    )
    print('\033[92m\n\n\ncandles:\n\033[0m', candles)

