from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType, TimeInForce
from rabbitx.client import OrderStatus
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    private_key = os.environ['PRIVATE_KEY'] # change this to your private key
    symbol = 'BTC-USD'
    testnet=False # change this to True if using on testnet
    if testnet:
        client = Client(api_url=const.TESTNET_URL, private_key=private_key) 
    else:
        client = Client(api_url=const.URL, private_key=private_key)

    resp = client.markets.list([symbol])
    market = resp[0]
    print(f'\033[92m\n\n\n{symbol} market info:\n\033[0m', market)

    orderbook = client.orderbook.get('BTC-USD')[0]
    print(f'\033[92m\n\n\n{symbol} orderbook:\n\033[0m', orderbook)

    client.onboarding.onboarding()
    
    new_jwt = client.jwt.update(client._jwt)
    print('\033[92m\n\n\nnew jwt:\n\033[0m', new_jwt)
    order_1 = client.orders.create(
        'BTC-USD',
        float(market['index_price']),
        OrderSide.LONG,
        0.002,
        OrderType.LIMIT,
    )
    print('\033[92m\n\n\norder creation:\n\033[0m', order_1)

    order_2 = client.orders.create(
        'BTC-USD',
        float(market['index_price']),
        OrderSide.SHORT,
        0.001,
        OrderType.LIMIT,
    )

    print('\033[92m\n\n\norder creation:\n\033[0m', order_2)
    
    order_3 = client.orders.create(
        'BTC-USD',
        float(market['min_tick']),
        OrderSide.LONG,
        0.001,
        OrderType.LIMIT,
        time_in_force=TimeInForce.POSTONLY,
    )
    
    print('\033[92m\n\n\norder creation:\n\033[0m', order_3)
    
    order_4 = client.orders.create(
        'BTC-USD',
        float(100000),
        OrderSide.LONG,
        0.001,
        OrderType.LIMIT,
        time_in_force=TimeInForce.POSTONLY,
    )
    
    print('\033[92m\n\n\norder creation:\n\033[0m', order_3)
    
    
    client.orders.amend(order_1['id'], symbol, float(market['index_price'])-1, 2)
    client.orders.cancel(order_1['id'], symbol)
    client.orders.cancel(order_2['id'], symbol)
    client.orders.cancel(order_3['id'], symbol)
    client.orders.cancel(order_4['id'], symbol)
      
    orders = client.orders.list(status=OrderStatus.OPEN)
    print('\033[92m\n\n\nopen order list:\n\033[0m', orders)
    
    order_status = client.orders.list(order_id=order_2['id'])
    print('\033[92m\n\n\norder 2 status:\n\033[0m', order_status)
    
    positions = client.positions.list()
    print('\033[92m\n\n\nopen positions list:\n\033[0m', positions)

    fills = client.fills.list()
    print('\033[92m\n\n\nfills:\n\033[0m', fills)

    order_fills = client.fills.list_by_order(order_id=order_2['id'])
    print('\033[92m\n\n\norder fills:\n\033[0m', order_fills)
    
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

