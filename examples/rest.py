# This example tests the following:
# Public endpoints:
# * market information
# * market trades
# * market trades with pagination
# * market orderbook
# * market candles
# * market candles with pagination
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
import argparse
import json
import time
import os
from dotenv import load_dotenv
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':

    # Set up argument parser
    parser = argparse.ArgumentParser(description='RabbitX API example')
    parser.add_argument('--testnet', action='store_true', help='Use testnet instead of mainnet')
    parser.add_argument('--exchange', type=str, default='rbx', choices=['rbx', 'bfx'], help='Choose the exchange: rbx (RabbitX) or bfx (Bitfinex)')
    args = parser.parse_args()

    # Use the parsed argument to set testnet
    testnet = args.testnet
    exchange = args.exchange

    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    
    # Read the apiKey.json exported from RabbitX during api key creation
    api_key_file = 'apiKey.json'
    if os.path.exists(api_key_file):
        with open(api_key_file, 'r') as file:
            api_data = json.load(file)
            # Extract the required information
            api_key = api_data['key']
            api_secret = api_data['secret']
            private_jwt = api_data['privateJwt']
            public_jwt = api_data['publicJwt']
            private_jwt = api_data['privateJwt']    
    else:
        # Load from .env environment variables if apiKey.json is not found
        api_key = os.environ.get('API_KEY')
        api_secret = os.environ.get('API_SECRET')
        public_jwt = os.environ.get('PUBLIC_JWT')
        private_jwt = os.environ.get('PRIVATE_JWT')

        if not all([api_key, api_secret, public_jwt, private_jwt]):
            print("Error: Required environment variables are not set.")
            exit(1)

    symbol = 'BTC-USD'
    
    if exchange == 'rbx':
        # Set up client
        if testnet:
            client = Client(api_url=const.TESTNET_URL, api_key=api_key, api_secret=api_secret,public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange) 
        else:
            client = Client(api_url=const.URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
    elif exchange == 'bfx':
        if testnet:
            client = Client(api_url=const.TESTNET_BFX_URL, api_key=api_key, api_secret=api_secret,public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
        else:
            client = Client(api_url=const.BFX_URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)

    # Onboarding is needed for private endpoints
    client.onboarding.init()

    # Get market information
    resp = client.markets.list([symbol])
    market = resp[0]
    print(f'\033[92m\n\n\n{symbol} market info:\n\033[0m', json.dumps(market, indent=4))

    # Get market trades
    resp = client.trades.list(market_id='BTC-USD', p_limit=1)
    print(f'\033[92m\n\n\n{symbol} trades:\n\033[0m', json.dumps(resp, indent=4))

    # Get market orderbook
    orderbook = client.orderbook.get('BTC-USD')[0]
    print(f'\033[92m\n\n\n{symbol} orderbook:\n\033[0m', orderbook)

    # Get Candles Data
    resp = client.candles.list(symbol, timestamp_from=int(time.time()-3600), timestamp_to=int(time.time()), period=CandlePeriod.M1)
    candle = resp[0]
    print(f'\033[92m\n\n\n{symbol} candle:\n\033[0m', candle)
            
    account = client.account.get()
    print('\033[92m\n\n\naccount:\n\033[0m', account)
        
    profile = client.profile.get()
    print('\033[92m\n\n\nprofile:\n\033[0m', json.dumps(profile, indent=4))
    
    new_jwt = client.jwt.update(client.private_jwt)
    print('\033[92m\n\n\nnew jwt:\n\033[0m', new_jwt)
   
    order_1 = client.orders.create(
        'BTC-USD',
        float(market['min_tick']),
        OrderSide.LONG,
        0.0001,
        OrderType.LIMIT,
    )
    print('\033[92m\n\n\norder creation:\n\033[0m', order_1)
    
    order_2 = client.orders.create(
        'BTC-USD',
        float(1e9),
        OrderSide.SHORT,
        0.0001,
        OrderType.LIMIT,
    )

    print('\033[92m\n\n\norder creation:\n\033[0m', order_2)
    
    order_3 = client.orders.create(
        'BTC-USD',
        float(market['min_tick']),
        OrderSide.LONG,
        0.0001,
        OrderType.LIMIT,
        time_in_force=TimeInForce.POSTONLY,
    )
    
    order_4 = client.orders.create(
        'BTC-USD',
        float(market['best_bid']),
        OrderSide.LONG,
        0.0001,
        OrderType.LIMIT,
        time_in_force=TimeInForce.POSTONLY,
    )
    
    print('\033[92m\n\n\norder creation:\n\033[0m', order_3)
    
    # Amend order price and size together
    client.orders.amend(order_1['id'], symbol, price=float(market['min_tick'])*2, size=float(market['min_order'])*2)
    # Amend order price
    client.orders.amend(order_1['id'], symbol, price=float(market['min_tick'])*3)
    client.orders.cancel(order_1['id'], symbol)
    client.orders.cancel(order_2['id'], symbol)
    client.orders.cancel(order_3['id'], symbol)
    client.orders.cancel(order_4['id'], symbol)
    
    orders = client.orders.list(status=OrderStatus.OPEN)
    print('\033[92m\n\n\nopen order list:\n\033[0m', json.dumps(orders, indent=4))
    
    positions = client.positions.list()
    print('\033[92m\n\n\nopen positions list:\n\033[0m', json.dumps(positions, indent=4))

    fills = client.fills.list(p_limit=1)
    print('\033[92m\n\n\nfills:\n\033[0m', json.dumps(fills, indent=4))

    balance_history = client.balance.list(p_limit=4)
    print('\033[92m\n\n\nbalance history:\n\033[0m', json.dumps(balance_history, indent=4))
    
    funding_payments = client.balance.list(ops_type='funding', p_limit=1)
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

