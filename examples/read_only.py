# This example tests the following:
# Public endpoints:
# * market information
# * market trades
# * market orderbook
# * market candles
# Private endpoints:
# * account details
# * profile details
# * order placement
# * order cancel
# * order amend
# * account fills
# * account orders
# * account balance history
# * account positions


from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType, TimeInForce
from rabbitx.client import OrderStatus
import time
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    private_jwt = os.environ['PRIVATE_JWT']
                         
    symbol = 'BTC-USD'
    testnet=False # change this to True if using on testnet
    
    # Set up client
    if testnet:
        client = Client(api_url=const.TESTNET_URL,private_jwt=private_jwt) 
    else:
        client = Client(api_url=const.URL, private_jwt=private_jwt)

    # Onboarding is needed for private endpoints
    client.onboarding.init()
# * market information
# * market trades
# * market orderbook
# * market candles
    # Get market information
    resp = client.markets.list([symbol])
    market = resp[0]
    print(f'\033[92m\n\n\n{symbol} market info:\n\033[0m', market)

    # Get market trades
    resp = client.trades.list()    

    # Get Candles Data
    resp = client.candles.list(symbol, timestamp_from=int(time.time()-3600), timestamp_to=int(time.time()), period=CandlePeriod.M1)
    candle = resp[0]
    print(f'\033[92m\n\n\n{symbol} candle:\n\033[0m', candle)

    orderbook = client.orderbook.get('BTC-USD')[0]
    print(f'\033[92m\n\n\n{symbol} orderbook:\n\033[0m', orderbook)
    
    new_jwt = client.jwt.update(client.public_jwt)
    print('\033[92m\n\n\nnew jwt:\n\033[0m', new_jwt)
    
    order_1 = client.orders.create(
        'BTC-USD',
        float(market['min_tick']),
        OrderSide.LONG,
        0.002,
        OrderType.LIMIT,
    )
    print('\033[92m\n\n\norder creation:\n\033[0m', order_1)
    
    order_2 = client.orders.create(
        'BTC-USD',
        float(1e9),
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
    
    order_4 = client.orders.create(
        'BTC-USD',
        float(1e9),
        OrderSide.LONG,
        0.001,
        OrderType.LIMIT,
        time_in_force=TimeInForce.POSTONLY,
    )
    
    print('\033[92m\n\n\norder creation:\n\033[0m', order_3)
    
    client.orders.amend(order_1['id'], symbol, float(market['min_tick']+1), 2)
    client.orders.cancel(order_1['id'], symbol)
    client.orders.cancel(order_2['id'], symbol)
    client.orders.cancel(order_3['id'], symbol)
    client.orders.cancel(order_4['id'], symbol)
    
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
    client.account.validate(client.public_jwt)

    new_leverage = client.account.set_leverage('BTC-USD', 20)
    print('\033[92m\n\n\nnew leverage:\n\033[0m', new_leverage)

    candles = client.candles.list(
        'BTC-USD',
        client.current_timestamp - 10,
        client.current_timestamp + 10,
        CandlePeriod.M1,
    )
    print('\033[92m\n\n\ncandles:\n\033[0m', candles)

