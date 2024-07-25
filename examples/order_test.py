from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType, TimeInForce
from rabbitx.client import OrderStatus
import json
from dotenv import load_dotenv
import argparse
import os

load_dotenv()

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
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    public_jwt = os.environ['PUBLIC_JWT']
    private_jwt = os.environ['PRIVATE_JWT']

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

    order_1 = client.orders.create(
        symbol,
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
    