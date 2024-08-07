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
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':

    # Set up argument parser
    parser = argparse.ArgumentParser(description='RabbitX API example')
    parser.add_argument('--testnet', action='store_true', help='Use testnet instead of mainnet')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--exchange', type=str, default='rbx', choices=['rbx', 'bfx'], help='Choose the exchange: rbx (RabbitX) or bfx (Bitfinex)')
    args = parser.parse_args()

    # Use the parsed argument to set testnet
    testnet = args.testnet
    exchange = args.exchange
    debug = args.debug

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
        'BTC-USD',
        float(1),
        OrderSide.LONG,
        float(1),
        OrderType.LIMIT,
    )
    print('\033[92m\n\n\norder creation:\n\033[0m', order_1)
    
    order_2 = client.orders.create(
        'BTC-USD',
        float(80000),
        OrderSide.SHORT,
        float(market['min_order']),
        OrderType.LIMIT,
    )
    print('\033[92m\n\n\norder creation:\n\033[0m', order_2)
    
    orders = client.orders.list(status=OrderStatus.OPEN)
    # orders = client.orders.list(status=OrderStatus.PROCESSING)
    print('\033[92m\n\n\nopen order list:\n\033[0m', json.dumps(orders, indent=4))
    
    deadman = client.deadman.create(timeout=5000)
    print('\033[92m\n\n\ndeadman creation:\n\033[0m', deadman)
    
    deadman_info = client.deadman.get()
    print('\033[92m\n\n\ndeadman info:\n\033[0m', json.dumps(deadman_info, indent=4))
    
    # print('\033[92m\n\n\nsleeping for 7 seconds\n\033[0m')
    # time.sleep(6)
    # print('\033[92m\n\n\nsleeping done\n\033[0m')
    
    client.deadman.remove()
    print('\033[92m\n\n\ndeadman removed\n')

    deadman_info = client.deadman.get()
    print('\033[92m\n\n\ndeadman info:\n\033[0m', json.dumps(deadman_info, indent=4))
    
    # orders = client.orders.list(status=OrderStatus.OPEN)
    # print('\033[92m\n\n\nopen order list:\n\033[0m', json.dumps(orders, indent=4))
    